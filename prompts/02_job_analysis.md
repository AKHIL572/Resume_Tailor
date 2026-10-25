# PASTE MY INSTRUCTIONS FOR THIS SECTION BELOW THIS LINE
# ─────────────────────────────────────────────────────────────────────────────
# DEFAULT: Job Analysis Rules
# ─────────────────────────────────────────────────────────────────────────────

## Job Description Analysis Instructions

Extract the following fields from the job description:

- **company**: The hiring company name. Leave blank if truly anonymous.
- **job_title**: The exact job title as stated.
- **location**: City, state/country, remote/hybrid/onsite.
- **employment_type**: Full-time, part-time, contract, internship, etc.
- **salary**: Any salary, range, or compensation information stated.
- **experience_requirement**: Years of experience required/preferred.
- **education_requirement**: Degree requirements.
- **technical_requirements**: All technical skills, tools, frameworks, languages mentioned.
- **responsibilities**: What the candidate will do.
- **domain_industry**: The business domain (e.g., fintech, healthcare, e-commerce, SaaS).
- **other_requirements**: Visa, travel, clearance, certifications, soft skills, etc.
- **emails_in_jd**: All email addresses found in the posting.

## Requirement Classification

Split all requirements into four categories:

- **must_have**: Explicitly required, non-negotiable (e.g., "required," "must have," "minimum").
- **preferred**: Explicitly optional or preferred (e.g., "nice to have," "preferred," "a plus").
- **responsibilities**: What the role involves day-to-day.
- **domain_context**: Background context about the company, team, or product.

When in doubt between must_have and preferred, use context. If the JD says "5+ years" but for a mid-level role, classify it as must_have with a note.
