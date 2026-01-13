"""Resume-specific extraction using LLM."""

import json
from typing import Any

from tilde.config import call_llm
from tilde.ingest.loader import Document
from tilde.updates import PendingUpdate


RESUME_EXTRACTION_PROMPT = """You are analyzing a resume/CV to extract structured profile data.

Document:
<resume>
{content}
</resume>

Extract ALL of the following if present:

1. **Identity**: name, role/title, years of experience
2. **Experience**: each job with company, role, dates (YYYY-MM format), highlights, technologies
3. **Education**: each degree with institution, field, graduation year, honors
4. **Projects**: personal/open-source projects with descriptions
5. **Publications**: papers, patents, articles with venue and year
6. **Tech Stack**: programming languages, frameworks, tools
7. **Knowledge Domains**: areas of expertise (e.g., "distributed systems", "ML/AI")

Respond with a JSON object matching this schema:
```json
{{
  "identity": {{
    "name": "string",
    "role": "string",
    "years_experience": number or null
  }},
  "experience": [
    {{
      "company": "string",
      "role": "string",
      "start_date": "YYYY-MM or null",
      "end_date": "YYYY-MM or null (null=current)",
      "highlights": ["string"],
      "technologies": ["string"]
    }}
  ],
  "education": [
    {{
      "institution": "string",
      "degree": "string or null",
      "field": "string or null",
      "graduation_year": number or null,
      "highlights": ["string"]
    }}
  ],
  "projects": [
    {{
      "name": "string",
      "description": "string or null",
      "url": "string or null",
      "technologies": ["string"],
      "highlights": ["string"]
    }}
  ],
  "publications": [
    {{
      "title": "string",
      "venue": "string or null",
      "year": number or null,
      "url": "string or null",
      "authors": ["string"]
    }}
  ],
  "tech_stack": {{
    "languages": ["string"],
    "frameworks": ["string"],
    "tools": ["string"]
  }},
  "domains": {{
    "domain_name": "description"
  }},
  "confidence": 0.0-1.0
}}
```

IMPORTANT: 
- Extract real data from the resume, don't invent anything
- Use ISO date format (YYYY-MM) for dates
- Set confidence 0.0-1.0 based on how clearly the info was stated
- If a section is not present, use empty arrays/objects
"""



def _parse_resume_response(response: str) -> dict[str, Any]:
    """Parse the LLM response to extract resume data."""
    response = response.strip()

    # Try to extract JSON from markdown code block
    if "```json" in response:
        start = response.find("```json") + 7
        end = response.find("```", start)
        if end > start:
            response = response[start:end].strip()
    elif "```" in response:
        start = response.find("```") + 3
        end = response.find("```", start)
        if end > start:
            response = response[start:end].strip()

    try:
        data = json.loads(response)
        if isinstance(data, dict):
            return data
        return {}
    except json.JSONDecodeError:
        return {}


def extract_from_resume(
    document: Document,
    model: str | None = None,
) -> list[PendingUpdate]:
    """Extract profile updates from a resume using LLM.

    Args:
        document: The loaded resume document
        model: LLM model to use

    Returns:
        List of PendingUpdate objects ready to be added to the approval queue
    """
    prompt = RESUME_EXTRACTION_PROMPT.format(content=document.content)

    try:
        response = call_llm(prompt, model)
        data = _parse_resume_response(response)
    except Exception as e:
        import logging
        logging.warning(f"Error extracting from resume: {e}")
        return []

    if not data:
        return []

    updates: list[PendingUpdate] = []
    confidence = float(data.get("confidence", 0.7))

    # Identity updates
    if identity := data.get("identity"):
        if name := identity.get("name"):
            updates.append(PendingUpdate(
                field_path="user_profile.identity.name",
                action="set",
                proposed_value=name,
                reason=f"Extracted from resume: {document.title}",
                source_agent="tilde-resume-ingest",
                confidence=confidence,
            ))
        if role := identity.get("role"):
            updates.append(PendingUpdate(
                field_path="user_profile.identity.role",
                action="set",
                proposed_value=role,
                reason=f"Extracted from resume: {document.title}",
                source_agent="tilde-resume-ingest",
                confidence=confidence,
            ))
        if years := identity.get("years_experience"):
            updates.append(PendingUpdate(
                field_path="user_profile.identity.years_experience",
                action="set",
                proposed_value=years,
                reason=f"Extracted from resume: {document.title}",
                source_agent="tilde-resume-ingest",
                confidence=confidence,
            ))

    # Experience updates
    if experience := data.get("experience"):
        for exp in experience:
            updates.append(PendingUpdate(
                field_path="user_profile.experience",
                action="append",
                proposed_value=exp,
                reason=f"Work experience at {exp.get('company', 'Unknown')}",
                source_agent="tilde-resume-ingest",
                confidence=confidence,
            ))

    # Education updates
    if education := data.get("education"):
        for edu in education:
            updates.append(PendingUpdate(
                field_path="user_profile.education",
                action="append",
                proposed_value=edu,
                reason=f"Education at {edu.get('institution', 'Unknown')}",
                source_agent="tilde-resume-ingest",
                confidence=confidence,
            ))

    # Projects updates
    if projects := data.get("projects"):
        for proj in projects:
            updates.append(PendingUpdate(
                field_path="user_profile.projects",
                action="append",
                proposed_value=proj,
                reason=f"Project: {proj.get('name', 'Unknown')}",
                source_agent="tilde-resume-ingest",
                confidence=confidence,
            ))

    # Publications updates
    if publications := data.get("publications"):
        for pub in publications:
            updates.append(PendingUpdate(
                field_path="user_profile.publications",
                action="append",
                proposed_value=pub,
                reason=f"Publication: {pub.get('title', 'Unknown')}",
                source_agent="tilde-resume-ingest",
                confidence=confidence,
            ))

    # Tech stack updates
    if tech_stack := data.get("tech_stack"):
        if languages := tech_stack.get("languages"):
            for lang in languages:
                updates.append(PendingUpdate(
                    field_path="user_profile.tech_stack.languages",
                    action="append",
                    proposed_value=lang,
                    reason=f"Programming language from resume",
                    source_agent="tilde-resume-ingest",
                    confidence=confidence,
                ))
        if frameworks := tech_stack.get("frameworks"):
            for fw in frameworks:
                updates.append(PendingUpdate(
                    field_path="user_profile.tech_stack.languages",
                    action="append",
                    proposed_value=fw,
                    reason=f"Framework from resume",
                    source_agent="tilde-resume-ingest",
                    confidence=confidence,
                ))
        if tools := tech_stack.get("tools"):
            for tool in tools:
                updates.append(PendingUpdate(
                    field_path="user_profile.tech_stack.languages",
                    action="append",
                    proposed_value=tool,
                    reason=f"Tool from resume",
                    source_agent="tilde-resume-ingest",
                    confidence=confidence,
                ))

    # Domain knowledge updates
    if domains := data.get("domains"):
        for domain_name, description in domains.items():
            updates.append(PendingUpdate(
                field_path=f"user_profile.knowledge.domains.{domain_name}",
                action="set",
                proposed_value=description,
                reason=f"Domain expertise from resume",
                source_agent="tilde-resume-ingest",
                confidence=confidence,
            ))

    return updates
