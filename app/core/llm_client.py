"""
Provider-agnostic LLM client using the OpenAI-compatible chat API.
Supports:
  - Local Ollama  (http://localhost:11434/v1)
  - Groq, Together, OpenRouter (base_url + api_key + model)

Features:
  - Structured JSON output with Pydantic validation
  - Automatic JSON repair and retry (max 3 attempts)
  - Clear error messages for common failure modes
  - Timeout handling
"""

from __future__ import annotations

import json
import logging
import re
import time
from typing import Any, Type, TypeVar

try:
    import keyring
except ImportError:
    keyring = None

try:
    from openai import OpenAI, APIConnectionError, APITimeoutError, AuthenticationError
except ImportError:
    OpenAI = None
    APIConnectionError = Exception  # type: ignore
    APITimeoutError = Exception     # type: ignore
    AuthenticationError = Exception # type: ignore
from pydantic import BaseModel, ValidationError

try:
    from json_repair import repair_json  # type: ignore
    HAS_REPAIR = True
except ImportError:
    HAS_REPAIR = False

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)

KEYRING_SERVICE = "JobTailor"
_IN_MEMORY_KEYS: dict[str, str] = {}


def get_api_key(provider: str) -> str:
    """Retrieve API key from system keyring or fallback memory."""
    if keyring:
        try:
            key = keyring.get_password(KEYRING_SERVICE, provider)
            if key:
                return key
        except Exception:
            pass
    return _IN_MEMORY_KEYS.get(provider, "")


def set_api_key(provider: str, key: str) -> None:
    """Store API key in system keyring or fallback memory."""
    if keyring:
        try:
            keyring.set_password(KEYRING_SERVICE, provider, key)
            return
        except Exception:
            pass
    _IN_MEMORY_KEYS[provider] = key


def delete_api_key(provider: str) -> None:
    """Remove API key."""
    if keyring:
        try:
            keyring.delete_password(KEYRING_SERVICE, provider)
        except Exception:
            pass
    _IN_MEMORY_KEYS.pop(provider, None)


class LLMCallRecord:
    """Records a single LLM call for display in the Log tab."""

    def __init__(
        self,
        step: str,
        prompt: str,
        response: str,
        model: str,
        duration_s: float,
        attempts: int,
        success: bool,
        error: str = "",
    ):
        self.step = step
        self.prompt = prompt
        self.response = response
        self.model = model
        self.duration_s = duration_s
        self.attempts = attempts
        self.success = success
        self.error = error

    def to_log_text(self) -> str:
        status = "✓ SUCCESS" if self.success else "✗ FAILED"
        return (
            f"{'='*60}\n"
            f"STEP: {self.step}  |  MODEL: {self.model}  |  {status}\n"
            f"Duration: {self.duration_s:.1f}s  |  Attempts: {self.attempts}\n"
            f"{'─'*60}\n"
            f"PROMPT:\n{self.prompt}\n"
            f"{'─'*60}\n"
            f"RESPONSE:\n{self.response}\n"
            + (f"ERROR: {self.error}\n" if self.error else "")
            + f"{'='*60}\n"
        )


class LLMClient:
    """
    Provider-agnostic wrapper around the OpenAI-compatible chat completion API.
    Instantiate once per pipeline run with the current config.
    """

    def __init__(
        self,
        provider: str = "ollama",
        base_url: str = "http://localhost:11434/v1",
        model: str = "llama3.1:8b",
        api_key: str = "",
        temperature: float = 0.3,
        timeout: float = 120.0,
        max_retries: int = 3,
    ):
        self.provider = provider
        self.model = model
        self.temperature = temperature
        self.max_retries = max_retries
        self.log_records: list[LLMCallRecord] = []

        # Ollama doesn't need a real key but the client requires a non-empty string
        resolved_key = api_key or (get_api_key(provider) if provider != "ollama" else "ollama")
        if not resolved_key:
            resolved_key = "no-key"

        self._client = OpenAI(
            api_key=resolved_key,
            base_url=base_url,
            timeout=timeout,
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def chat(
        self,
        step: str,
        messages: list[dict[str, str]],
    ) -> str:
        """Send a chat request and return the raw response text."""
        start = time.time()
        last_error = ""
        for attempt in range(1, self.max_retries + 1):
            try:
                resp = self._client.chat.completions.create(
                    model=self.model,
                    messages=messages,  # type: ignore[arg-type]
                    temperature=self.temperature,
                )
                text = resp.choices[0].message.content or ""
                duration = time.time() - start
                self._record(step, messages, text, duration, attempt, True)
                logger.debug("LLM [%s] attempt %d OK (%.1fs)", step, attempt, duration)
                return text
            except APIConnectionError as exc:
                last_error = (
                    f"Cannot connect to {self.provider}. "
                    f"Is the server running? ({exc})"
                )
            except APITimeoutError:
                last_error = f"Request timed out (attempt {attempt})"
            except AuthenticationError:
                last_error = f"Invalid API key for provider '{self.provider}'"
                break  # No point retrying auth failures
            except Exception as exc:
                last_error = str(exc)
            logger.warning("LLM [%s] attempt %d failed: %s", step, attempt, last_error)
            if attempt < self.max_retries:
                time.sleep(1.5 * attempt)

        duration = time.time() - start
        prompt_text = _messages_to_text(messages)
        self._record(step, messages, "", duration, self.max_retries, False, last_error)
        raise RuntimeError(f"LLM call '{step}' failed after {self.max_retries} attempts: {last_error}")

    def chat_json(
        self,
        step: str,
        messages: list[dict[str, str]],
        schema: Type[T],
    ) -> T:
        """
        Send a chat request expecting JSON, parse + validate with Pydantic.
        Retries on invalid JSON with an error message injected into context.
        """
        msgs = list(messages)
        last_error = ""

        for attempt in range(1, self.max_retries + 1):
            raw = self.chat(f"{step}[json_attempt_{attempt}]", msgs)
            extracted = _extract_json(raw)

            try:
                data = json.loads(extracted)
                result = schema.model_validate(data)
                return result
            except json.JSONDecodeError as exc:
                last_error = f"JSON parse error: {exc}"
                # Try JSON repair
                if HAS_REPAIR:
                    try:
                        repaired = repair_json(extracted)
                        data = json.loads(repaired)
                        result = schema.model_validate(data)
                        logger.info("LLM [%s] JSON repaired on attempt %d", step, attempt)
                        return result
                    except Exception:
                        pass
            except ValidationError as exc:
                last_error = f"Schema validation failed: {exc.errors()}"

            if attempt < self.max_retries:
                # Feed the error back to the LLM
                correction_msg = {
                    "role": "user",
                    "content": (
                        f"Your previous response was not valid JSON matching the required schema.\n"
                        f"Error: {last_error}\n"
                        f"Schema: {schema.model_json_schema()}\n"
                        f"Return ONLY a valid JSON object. No markdown, no explanation."
                    ),
                }
                msgs = msgs + [{"role": "assistant", "content": raw}, correction_msg]

        raise RuntimeError(
            f"LLM call '{step}' could not produce valid JSON after {self.max_retries} attempts. "
            f"Last error: {last_error}"
        )

    def test_connection(self) -> tuple[bool, str]:
        """Test connectivity. Returns (ok, message)."""
        try:
            resp = self._client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Reply with the single word: OK"}],
                temperature=0,
                max_tokens=5,
            )
            text = (resp.choices[0].message.content or "").strip()
            return True, f"Connected. Model replied: {text!r}"
        except APIConnectionError as exc:
            return False, f"Connection failed: {exc}"
        except AuthenticationError:
            return False, "Authentication failed – check your API key."
        except Exception as exc:
            return False, f"Error: {exc}"

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _record(
        self,
        step: str,
        messages: list[dict],
        response: str,
        duration: float,
        attempts: int,
        success: bool,
        error: str = "",
    ) -> None:
        record = LLMCallRecord(
            step=step,
            prompt=_messages_to_text(messages),
            response=response,
            model=self.model,
            duration_s=duration,
            attempts=attempts,
            success=success,
            error=error,
        )
        self.log_records.append(record)


def _extract_json(text: str) -> str:
    """Strip markdown code fences and return the JSON content."""
    text = text.strip()
    # Remove ```json ... ``` or ``` ... ```
    fence = re.match(r"```(?:json)?\s*([\s\S]*?)```", text)
    if fence:
        return fence.group(1).strip()
    # Remove trailing commas before } or ]
    text = re.sub(r",\s*([}\]])", r"\1", text)
    return text


def _messages_to_text(messages: list[dict]) -> str:
    """Convert messages list to a human-readable string for logging."""
    parts = []
    for m in messages:
        role = m.get("role", "?").upper()
        content = m.get("content", "")
        parts.append(f"[{role}]\n{content}")
    return "\n\n".join(parts)
