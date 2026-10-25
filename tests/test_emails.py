"""Unit tests for email extraction and classification."""

import pytest
from app.core.apply_finder import extract_emails, _classify_email
from app.models.schemas import EmailClassification


def test_extract_emails_regex():
    sample_jd = """
    Please send your CV to careers@techcorp.io or contact hr.team@gmail.com.
    You can also reach out to john.doe@company.org for inquiries.
    """
    emails = extract_emails(sample_jd)
    addresses = [e.address for e in emails]
    assert "careers@techcorp.io" in addresses
    assert "hr.team@gmail.com" in addresses
    assert "john.doe@company.org" in addresses


def test_classify_email_domain():
    corp_info = _classify_email("careers@stripe.com")
    assert corp_info.classification == EmailClassification.COMPANY
    assert corp_info.is_legitimate is True
    assert corp_info.domain == "stripe.com"

    free_info = _classify_email("recruiter123@gmail.com")
    assert free_info.classification == EmailClassification.FREE_PROVIDER
    assert free_info.is_legitimate is False

    yahoo_info = _classify_email("jobs@yahoo.co.in")
    assert yahoo_info.classification == EmailClassification.FREE_PROVIDER
    assert yahoo_info.is_legitimate is False
