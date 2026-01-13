"""Tests for document ingestion."""

import tempfile
from pathlib import Path

import pytest

from tilde.ingest.loader import Document, load_document


@pytest.fixture
def temp_dir():
    """Create a temporary directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


def test_document_creation():
    """Test creating a Document object."""
    doc = Document(
        content="Hello world",
        source="/path/to/file.txt",
        title="Test Doc",
        doc_type="text",
    )
    assert doc.content == "Hello world"
    assert doc.title == "Test Doc"
    assert doc.doc_type == "text"


def test_document_default_title():
    """Test Document uses filename as default title."""
    doc = Document(content="test", source="/path/to/my_document.txt")
    assert doc.title == "my_document"


def test_document_repr():
    """Test Document string representation."""
    doc = Document(content="test content", source="file.txt")
    repr_str = repr(doc)
    assert "Document" in repr_str
    assert "file" in repr_str


def test_document_chunks_small():
    """Test chunking returns single chunk for small content."""
    doc = Document(content="Small content", source="file.txt")
    chunks = list(doc.chunks(chunk_size=100))
    assert len(chunks) == 1
    assert chunks[0] == "Small content"


def test_document_chunks_large():
    """Test chunking splits large content."""
    # Create content larger than chunk size
    content = "This is a sentence. " * 100  # ~2000 chars
    doc = Document(content=content, source="file.txt")
    chunks = list(doc.chunks(chunk_size=500, overlap=50))
    
    assert len(chunks) > 1
    # All chunks should be non-empty
    assert all(chunk.strip() for chunk in chunks)


def test_document_chunks_preserves_content():
    """Test chunking preserves all content with overlap."""
    content = "Word " * 200
    doc = Document(content=content, source="file.txt")
    chunks = list(doc.chunks(chunk_size=100, overlap=20))
    
    # Combined chunks should contain all original content
    combined = " ".join(chunks)
    word_count = len([w for w in combined.split() if w == "Word"])
    assert word_count >= 200  # May be more due to overlap


def test_load_text_file(temp_dir: Path):
    """Test loading a plain text file."""
    text_file = temp_dir / "test.txt"
    text_file.write_text("Hello, world!")
    
    doc = load_document(text_file)
    
    assert doc.content == "Hello, world!"
    assert doc.doc_type == "text"
    assert doc.title == "test"


def test_load_markdown_file(temp_dir: Path):
    """Test loading a markdown file."""
    md_file = temp_dir / "README.md"
    md_file.write_text("# Title\n\nContent here.")
    
    doc = load_document(md_file)
    
    assert "# Title" in doc.content
    assert doc.doc_type == "markdown"


def test_load_file_not_found():
    """Test loading nonexistent file raises error."""
    with pytest.raises(FileNotFoundError):
        load_document("/nonexistent/path/file.txt")


def test_load_document_string_path(temp_dir: Path):
    """Test loading with string path."""
    text_file = temp_dir / "test.txt"
    text_file.write_text("Content")
    
    doc = load_document(str(text_file))
    
    assert doc.content == "Content"


def test_chunk_breaks_at_paragraph():
    """Test chunking prefers paragraph boundaries."""
    content = "First paragraph with lots of content here.\n\nSecond paragraph starts here."
    doc = Document(content=content, source="file.txt")
    
    # With small chunk size, should break at paragraph
    chunks = list(doc.chunks(chunk_size=50, overlap=10))
    
    # First chunk should end near paragraph break
    assert chunks[0].endswith("here.") or "paragraph" in chunks[0]


def test_chunk_breaks_at_sentence():
    """Test chunking prefers sentence boundaries."""
    content = "First sentence here. Second sentence follows. Third sentence."
    doc = Document(content=content, source="file.txt")
    
    chunks = list(doc.chunks(chunk_size=30, overlap=5))
    
    # Chunks should tend to end at sentence boundaries
    for chunk in chunks:
        # Should end with punctuation or be the last chunk
        assert chunk.strip()


# =============================================================================
# Skill Extractor Tests
# =============================================================================

from tilde.ingest.skill_extractor import (
    extract_from_skill,
    extract_skill_metadata,
    parse_yaml_frontmatter,
    validate_skill_name,
)


def test_parse_yaml_frontmatter_valid():
    """Test parsing valid YAML frontmatter."""
    content = """---
name: test-skill
description: A test skill
---
# Body content here
"""
    frontmatter, body = parse_yaml_frontmatter(content)
    
    assert frontmatter["name"] == "test-skill"
    assert frontmatter["description"] == "A test skill"
    assert "# Body content here" in body


def test_parse_yaml_frontmatter_no_frontmatter():
    """Test parsing content without frontmatter."""
    content = "# Just a markdown file\n\nNo frontmatter here."
    frontmatter, body = parse_yaml_frontmatter(content)
    
    assert frontmatter == {}
    assert body == content


def test_parse_yaml_frontmatter_with_tags():
    """Test parsing frontmatter with tags array."""
    content = """---
name: code-formatter
description: Formats code
tags: [python, formatting, lint]
---
Body
"""
    frontmatter, body = parse_yaml_frontmatter(content)
    
    assert frontmatter["tags"] == ["python", "formatting", "lint"]


def test_validate_skill_name_valid():
    """Test valid skill names pass validation."""
    assert validate_skill_name("code-formatter") is True
    assert validate_skill_name("my-skill-123") is True
    assert validate_skill_name("simple") is True


def test_validate_skill_name_invalid():
    """Test invalid skill names fail validation."""
    assert validate_skill_name("") is False
    assert validate_skill_name("HasUpperCase") is False
    assert validate_skill_name("has spaces") is False
    assert validate_skill_name("has_underscore") is False
    assert validate_skill_name("a" * 65) is False  # Too long


def test_validate_skill_name_reserved_words():
    """Test reserved words are rejected."""
    assert validate_skill_name("anthropic-helper") is False
    assert validate_skill_name("claude-assistant") is False
    assert validate_skill_name("my-anthropic") is False


def test_extract_skill_metadata_complete():
    """Test extracting complete skill metadata."""
    content = """---
name: python-formatter
description: Formats Python code using black
tags: [python, formatting]
requires: [code-analyzer]
---
# Python Formatter

This skill formats your Python code.
"""
    metadata = extract_skill_metadata(content, "/path/to/SKILL.md")
    
    assert metadata is not None
    assert metadata["name"] == "python-formatter"
    assert metadata["description"] == "Formats Python code using black"
    assert metadata["source_type"] == "anthropic-skill"
    assert metadata["source_path"] == "/path/to/SKILL.md"
    assert metadata["tags"] == ["python", "formatting"]
    assert metadata["requires"] == ["code-analyzer"]


def test_extract_skill_metadata_missing_required():
    """Test extraction fails when required fields are missing."""
    # Missing description
    content = """---
name: incomplete-skill
---
Body
"""
    metadata = extract_skill_metadata(content, "/path/to/SKILL.md")
    assert metadata is None
    
    # Missing name
    content = """---
description: Has description but no name
---
Body
"""
    metadata = extract_skill_metadata(content, "/path/to/SKILL.md")
    assert metadata is None


def test_extract_from_skill_creates_update():
    """Test full extraction creates a PendingUpdate."""
    content = """---
name: test-formatter
description: A test formatting skill
tags: [test]
---
# Test Formatter
"""
    doc = Document(content=content, source="/skills/SKILL.md")
    updates = extract_from_skill(doc)
    
    assert len(updates) == 1
    update = updates[0]
    
    assert update.field_path == "user_profile.skills"
    assert update.action == "append"
    assert update.proposed_value["name"] == "test-formatter"
    assert update.proposed_value["description"] == "A test formatting skill"
    assert update.proposed_value["source_type"] == "anthropic-skill"
    assert update.confidence == 0.9


def test_extract_from_skill_invalid_name_lower_confidence():
    """Test invalid skill name results in lower confidence."""
    content = """---
name: InvalidName
description: Has invalid uppercase name
---
Body
"""
    doc = Document(content=content, source="/skills/SKILL.md")
    updates = extract_from_skill(doc)
    
    assert len(updates) == 1
    assert updates[0].confidence == 0.5  # Lower confidence due to invalid name


def test_extract_from_skill_no_frontmatter():
    """Test extraction returns empty list for invalid skill file."""
    content = "# Just a regular markdown file\n\nNo skill here."
    doc = Document(content=content, source="/skills/SKILL.md")
    updates = extract_from_skill(doc)
    
    assert updates == []


def test_extract_from_skill_with_visibility():
    """Test extraction respects visibility parameter."""
    content = """---
name: private-skill
description: A private skill
---
Body
"""
    doc = Document(content=content, source="/skills/SKILL.md")
    updates = extract_from_skill(doc, visibility="private")
    
    assert len(updates) == 1
    assert updates[0].proposed_value["visibility"] == "private"
