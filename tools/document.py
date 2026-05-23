from markitdown import MarkItDown, StreamInfo
from io import BytesIO
from pathlib import Path

from pydantic import Field

SUPPORTED_EXTENSIONS = {"pdf", "docx"}


def binary_document_to_markdown(binary_data: bytes, file_type: str) -> str:
    """Converts binary document data to markdown-formatted text."""
    md = MarkItDown()
    file_obj = BytesIO(binary_data)
    stream_info = StreamInfo(extension=file_type)
    result = md.convert(file_obj, stream_info=stream_info)
    return result.text_content


def document_path_to_markdown(
    file_path: str = Field(description="Absolute or relative path to a PDF or DOCX file to convert"),
) -> str:
    """Convert a PDF or DOCX file on disk to markdown-formatted text.

    Reads the file at the given path, detects its type from the extension,
    and returns the full document content as a markdown string.

    When to use:
    - When you have a local file path to a document and need its content as markdown
    - For PDF and DOCX files only

    When NOT to use:
    - When you already have the file's binary content (use binary_document_to_markdown instead)
    - For file formats other than PDF and DOCX

    Examples:
    >>> document_path_to_markdown("/docs/report.pdf")
    "# Report Title\\n\\nContent..."
    >>> document_path_to_markdown("/docs/report.docx")
    "# Report Title\\n\\nContent..."
    """
    path = Path(file_path)
    ext = path.suffix.lstrip(".").lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type '.{ext}'. Must be one of: {SUPPORTED_EXTENSIONS}")
    if not path.exists():
        raise FileNotFoundError(f"No file found at: {file_path}")
    return binary_document_to_markdown(path.read_bytes(), ext)
