"""Document ingestion package for tilde."""

from tilde.ingest.extractor import extract_profile_updates
from tilde.ingest.loader import load_document
from tilde.ingest.skill_extractor import extract_from_skill

__all__ = ["load_document", "extract_profile_updates", "extract_from_skill"]
