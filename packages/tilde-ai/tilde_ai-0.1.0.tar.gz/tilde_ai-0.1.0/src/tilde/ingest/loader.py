"""Document loader for various file formats."""

from pathlib import Path
from typing import Iterator


class Document:
    """A loaded document with content and metadata."""

    def __init__(
        self,
        content: str,
        source: str,
        title: str | None = None,
        doc_type: str = "text",
    ):
        self.content = content
        self.source = source
        self.title = title or Path(source).stem
        self.doc_type = doc_type

    def __repr__(self) -> str:
        return f"Document(title={self.title!r}, type={self.doc_type}, len={len(self.content)})"

    def chunks(self, chunk_size: int = 4000, overlap: int = 200) -> Iterator[str]:
        """Split content into overlapping chunks for LLM processing."""
        if len(self.content) <= chunk_size:
            yield self.content
            return

        start = 0
        while start < len(self.content):
            end = start + chunk_size
            chunk = self.content[start:end]
            
            # Try to break at paragraph or sentence boundary
            if end < len(self.content):
                # Look for paragraph break
                para_break = chunk.rfind("\n\n")
                if para_break > chunk_size // 2:
                    chunk = chunk[:para_break]
                    end = start + para_break
                else:
                    # Look for sentence break
                    for punct in [". ", "! ", "? ", ".\n"]:
                        sent_break = chunk.rfind(punct)
                        if sent_break > chunk_size // 2:
                            chunk = chunk[:sent_break + 1]
                            end = start + sent_break + 1
                            break
            
            yield chunk.strip()
            start = end - overlap


def load_text_file(path: Path) -> Document:
    """Load a plain text or markdown file."""
    content = path.read_text(encoding="utf-8")
    doc_type = "markdown" if path.suffix.lower() in [".md", ".markdown"] else "text"
    return Document(content=content, source=str(path), doc_type=doc_type)


def load_pdf_file(path: Path) -> Document:
    """Load a PDF file (requires pypdf)."""
    try:
        from pypdf import PdfReader
    except ImportError:
        raise ImportError("pypdf is required for PDF loading. Install with: uv add pypdf")

    reader = PdfReader(path)
    content_parts = []
    
    for page in reader.pages:
        text = page.extract_text()
        if text:
            content_parts.append(text)
    
    content = "\n\n".join(content_parts)
    return Document(content=content, source=str(path), doc_type="pdf")


def load_epub_file(path: Path) -> Document:
    """Load an EPUB file (requires ebooklib and beautifulsoup4)."""
    try:
        import ebooklib
        from bs4 import BeautifulSoup
        from ebooklib import epub
    except ImportError:
        raise ImportError(
            "ebooklib and beautifulsoup4 are required for EPUB loading. "
            "Install with: uv add ebooklib beautifulsoup4"
        )

    book = epub.read_epub(path)
    content_parts = []
    title = book.get_metadata("DC", "title")
    title_str = title[0][0] if title else None

    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_content(), "html.parser")
            text = soup.get_text(separator="\n", strip=True)
            if text:
                content_parts.append(text)

    content = "\n\n".join(content_parts)
    return Document(content=content, source=str(path), title=title_str, doc_type="epub")


def load_document(path: str | Path) -> Document:
    """Load a document from file, auto-detecting format.
    
    Supported formats:
    - .txt, .md, .markdown — Plain text/Markdown
    - .pdf — PDF (requires pypdf)
    - .epub — EPUB (requires ebooklib, beautifulsoup4)
    """
    path = Path(path)
    
    if not path.exists():
        raise FileNotFoundError(f"Document not found: {path}")

    suffix = path.suffix.lower()
    
    if suffix in [".txt", ".md", ".markdown", ".rst"]:
        return load_text_file(path)
    elif suffix == ".pdf":
        return load_pdf_file(path)
    elif suffix == ".epub":
        return load_epub_file(path)
    else:
        # Try as text
        try:
            return load_text_file(path)
        except UnicodeDecodeError:
            raise ValueError(f"Unsupported document format: {suffix}")
