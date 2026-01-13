"""LLM-based profile extraction from documents."""

import json
from typing import Any

from tilde.config import call_llm
from tilde.ingest.loader import Document
from tilde.updates import PendingUpdate


EXTRACTION_PROMPT = """You are analyzing a document to extract information relevant to a professional profile.

Document Title: {title}
Document Type: {doc_type}

<document_chunk>
{content}
</document_chunk>

Based on this content, extract information that would be useful for a professional profile. Look for:

1. **Mental Models & Frameworks**: Key reasoning approaches, decision-making frameworks, or principles
2. **Domain Vocabulary**: Important terms, concepts, or specialized language
3. **Best Practices**: Recommended approaches, methodologies, or techniques
4. **Anti-Patterns**: Things to avoid, common mistakes, or warnings
5. **Insights**: Key takeaways or lessons learned

For each piece of information you extract, specify:
- `field_path`: Where it should go in the profile (e.g., "user_profile.domain_knowledge.domains.finance")
- `action`: "set" to replace, "append" to add to a list
- `value`: The extracted information
- `confidence`: 0.0-1.0 how confident you are this is accurate and useful

Respond with a JSON array of updates. Example:
```json
[
  {{
    "field_path": "user_profile.domain_knowledge.books_learned",
    "action": "append",
    "value": {{"title": "{title}", "insights": ["Key insight 1", "Key insight 2"]}},
    "confidence": 0.8
  }},
  {{
    "field_path": "user_profile.domain_knowledge.domains.{topic}",
    "action": "set",
    "value": "Summary of domain expertise from this document",
    "confidence": 0.7
  }}
]
```

If no relevant information can be extracted, return an empty array: []

IMPORTANT: Only extract information that would genuinely help an AI assistant understand the user's expertise and preferences. Be selective and focus on high-value insights."""



def _parse_llm_response(response: str) -> list[dict[str, Any]]:
    """Parse the LLM response to extract updates."""
    # Find JSON array in response
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
    
    # Parse JSON
    try:
        updates = json.loads(response)
        if isinstance(updates, list):
            return updates
        return []
    except json.JSONDecodeError:
        return []


def extract_profile_updates(
    document: Document,
    topic: str | None = None,
    model: str | None = None,
    max_chunks: int = 5,
) -> list[PendingUpdate]:
    """Extract profile updates from a document using an LLM.
    
    Args:
        document: The loaded document to process
        topic: Optional topic hint (e.g., "finance", "programming")
        model: LLM model to use
        max_chunks: Maximum number of chunks to process (for large documents)
    
    Returns:
        List of PendingUpdate objects ready to be added to the approval queue
    """
    topic = topic or document.title.lower().replace(" ", "_")[:30]
    all_updates: list[PendingUpdate] = []
    seen_values: set[str] = set()  # Deduplicate
    
    chunks = list(document.chunks())
    if len(chunks) > max_chunks:
        # Sample evenly from the document
        step = len(chunks) // max_chunks
        chunks = chunks[::step][:max_chunks]
    
    for chunk in chunks:
        prompt = EXTRACTION_PROMPT.format(
            title=document.title,
            doc_type=document.doc_type,
            content=chunk,
            topic=topic,
        )
        
        try:
            response = call_llm(prompt, model)
            updates_data = _parse_llm_response(response)
            
            for data in updates_data:
                # Create a unique key for deduplication
                value_key = f"{data.get('field_path')}:{json.dumps(data.get('value'), sort_keys=True)}"
                if value_key in seen_values:
                    continue
                seen_values.add(value_key)
                
                update = PendingUpdate(
                    field_path=data.get("field_path", ""),
                    action=data.get("action", "set"),
                    proposed_value=data.get("value"),
                    reason=f"Extracted from document: {document.title}",
                    source_agent="tilde-ingest",
                    confidence=float(data.get("confidence", 0.5)),
                )
                all_updates.append(update)
                
        except Exception as e:
            # Log but continue processing other chunks
            import logging
            logging.warning(f"Error processing chunk: {e}")
            continue
    
    return all_updates


def ingest_document(
    path: str,
    topic: str | None = None,
    model: str | None = None,
    auto_approve_threshold: float | None = None,
) -> list[str]:
    """Convenience function to ingest a document and queue updates.
    
    Args:
        path: Path to the document
        topic: Optional topic hint
        model: LLM model to use
        auto_approve_threshold: If set, auto-approve updates with confidence >= this value
    
    Returns:
        List of update IDs that were created
    """
    from tilde.ingest.loader import load_document
    from tilde.updates import get_update_queue
    
    document = load_document(path)
    updates = extract_profile_updates(document, topic, model)
    
    queue = get_update_queue()
    update_ids = []
    
    for update in updates:
        update_id = queue.propose(
            field_path=update.field_path,
            proposed_value=update.proposed_value,
            action=update.action,
            reason=update.reason,
            source_agent=update.source_agent,
            confidence=update.confidence,
        )
        update_ids.append(update_id)
        
        # Auto-approve if above threshold
        if auto_approve_threshold is not None and update.confidence >= auto_approve_threshold:
            queue.approve(update_id)
    
    return update_ids
