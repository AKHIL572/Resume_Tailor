# JobTailor

**JobTailor** is a desktop application built with Python 3.11+ and PySide6 that analyzes job descriptions, determines an evidence-based application verdict, extracts contacts, creates tailored outreach emails, and generates single-page ATS-optimized LaTeX resumes compiled to PDF.

---

## Quick Start (How to Run)

### 1. Prerequisites
- **Python 3.11+** installed on your system.
- **LLM Access** (one of the following):
  - **Local Ollama** (recommended for full privacy): [Download Ollama](https://ollama.com/) and run:
    ```bash
    ollama run llama3.1:8b
    # or for higher reasoning: ollama run llama3.3:70b
    ```
  - **Cloud APIs**: Groq, Together AI, or OpenRouter (enter your API key in Settings).
- **LaTeX Compiler** (for compiling PDF resumes):
  - **Tectonic** (recommended lightweight single-binary engine):
    ```powershell
    winget install tectonic
    ```
  - *Or* **MiKTeX** / **TeX Live** (pdflatex on your PATH).

---

### 2. Environment Setup & Installation

Open PowerShell in the project directory:

```powershell
cd "C:\Users\venut\OneDrive\Desktop\Resume Tailor"

# 1. Create a virtual environment
python -m venv venv

# 2. Activate virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# (If script execution is disabled in PowerShell, run: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass)

# 3. Install dependencies
pip install -r requirements.txt
```

---

### 3. Launch the Application

```powershell
python -m app.main
```

---

## First-Run Guide & Workflow

On initial launch, JobTailor automatically initializes your user data directory under:
`%LOCALAPPDATA%\JobTailor\JobTailor`
and seeds your:
- **Master Profile** (`profile/master_profile.md`)
- **LaTeX Template** (`templates/resume_template.tex`)
- **Editable Rule Prompts** (`rules/01_source_of_truth.md` through `rules/07_final_review.md`)
- **Contact Details** (`profile/contact.json`)
- **Layout & Application Config** (`config/settings.json`, `config/layout_config.json`)

### Workflow:
1. **Settings Tab**:
   - Verify provider: `ollama` (default endpoint `http://localhost:11434/v1`) or choose `groq` / `openrouter` / `together`.
   - Click **"Test Connection"** to verify communication with the LLM.
   - Verify that Tectonic or pdflatex is detected.
2. **New Job Tab**:
   - Paste any Job Description (JD) into the large text area.
   - Click **"Analyze & Tailor"**.
   - Watch the live progress steps:
     1. `Analyzing JD` $\rightarrow$ Extracts roles, salary, tech stack, and separates requirements (Must-have vs Preferred).
     2. `Genuineness Check` $\rightarrow$ Flags risk indicators (unrealistic pay, WhatsApp-only, free mail domains).
     3. `Fit & Verdict` $\rightarrow$ Calculates fit against your 15 cataloged projects. (If `DON'T APPLY` or `STRONGLY DON'T APPLY`, execution safely halts here).
     4. `How to Apply & Email` $\rightarrow$ Extracts contact email and generates a concise outreach email.
     5. `Resume Generation` $\rightarrow$ Tailors summary, skills (4-5 categories), experience (4 bullets), and 2-3 prioritized projects from your pool of 13 eligible projects (Project 1 excluded, Project 6 reserved for internship experience).
     6. `Compile & Validate` $\rightarrow$ Compiles via Tectonic and validates single-page fit, single-line bullets, and 85-100% line fill.
     7. `Fixer Loop` $\rightarrow$ If line wrapping or metric issues occur, the LLM refines the text until it passes.
   - Switch between result tabs: **Verdict**, **Job Details**, **Genuineness**, **How to Apply**, **Email**, **Resume (PDF Viewer)**, **LaTeX**, and **Log**.
3. **History Tab**:
   - Search through previous applications, view past verdicts, and export generated `.tex`, `.pdf`, and analysis files.
4. **Master Profile Tab**:
   - View/edit your profile. Click **"Parse Check"** anytime to verify project exclusions and leadership count.
5. **Rules Tab**:
   - Edit any of the 7 rules independently in markdown with per-file **"Reset to Default"**.

---

## Building a Standalone Executable

To produce a single, self-contained Windows executable with app icon:

```powershell
pip install pyinstaller
pyinstaller build/pyinstaller.spec
```

The resulting binary will be created in `dist/JobTailor.exe`.
You can right-click `dist/JobTailor.exe` $\rightarrow$ **Send to** $\rightarrow$ **Desktop (create shortcut)**.

---

## Layout Configuration & `combo_overrides`

Layout parameters live in `%LOCALAPPDATA%\JobTailor\JobTailor\config\layout_config.json`:

```json
{
  "page_count": 1,
  "summary_lines": [3, 4],
  "experience_bullets": 4,
  "skills_categories_default": 4,
  "skills_categories_when_two_projects_or_qa_role": 5,
  "projects_default": 3,
  "bullets_per_project": {
    "2_projects": 4,
    "3_projects": 3
  },
  "leadership_max_positions": 2,
  "leadership_bullets_per_position": 1,
  "certifications": [1, 2],
  "line_fill_min": 0.85,
  "line_fill_max": 1.00,
  "max_fix_rounds": 5,
  "unused_space_threshold_mm": 15.0,
  "combo_overrides": [
    {
      "condition": "include_leadership_and_two_projects",
      "projects_count": 2,
      "bullets_per_project": 3,
      "skills_categories": 4
    }
  ]
}
```

---

## Troubleshooting

- **Ollama not running**: Ensure the Ollama service is active. Run `ollama list` in terminal.
- **LaTeX compilation fails**: Ensure `tectonic` is installed and reachable via PATH, or specify its exact path in the **Settings** page.
- **Bullet line wrapping**: The app's automated `fixer.py` sends the exact overflow character delta back to the LLM to shorten the bullet while retaining facts.
- **Model too small**: Models under 7B parameters may occasionally struggle with JSON formatting. Use `llama3.1:8b` or cloud providers (Groq/OpenRouter with `llama-3.3-70b-versatile`).

---

## Assumptions & Design Defaults
1. **Project 1 Exclusion**: `Project 1` (House Price Analysis) is always excluded from the projects section across all prompts.
2. **Internship Assignment**: `Project 6` (Credit Risk Prediction) is exclusively assigned to the Experience section as your internship project.
3. **Dynamic Portfolio Linking**: For QA or developer roles, the header portfolio link defaults to your QA portfolio (`akhil-tv-qa-portfolio.vercel.app`); for data/analytical roles, it defaults to your primary portfolio (`akhil-tv-portfolio.vercel.app`).
4. **Local Secrets**: Cloud API keys are securely stored in Windows Credential Locker using the `keyring` library, never in plaintext.
