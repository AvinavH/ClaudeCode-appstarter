import os
import shutil
import pytest
from pathlib import Path
from tools.document import binary_document_to_markdown, document_path_to_markdown


class TestBinaryDocumentToMarkdown:
    # Define fixture paths
    FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
    DOCX_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.docx")
    PDF_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.pdf")

    def test_fixture_files_exist(self):
        """Verify test fixtures exist."""
        assert os.path.exists(self.DOCX_FIXTURE), (
            f"DOCX fixture not found at {self.DOCX_FIXTURE}"
        )
        assert os.path.exists(self.PDF_FIXTURE), (
            f"PDF fixture not found at {self.PDF_FIXTURE}"
        )

    def test_binary_document_to_markdown_with_docx(self):
        """Test converting a DOCX document to markdown."""
        # Read binary content from the fixture
        with open(self.DOCX_FIXTURE, "rb") as f:
            docx_data = f.read()

        # Call function
        result = binary_document_to_markdown(docx_data, "docx")

        # Basic assertions to check the conversion was successful
        assert isinstance(result, str)
        assert len(result) > 0
        # Check for typical markdown formatting - this will depend on your actual test file
        assert "#" in result or "-" in result or "*" in result

    def test_binary_document_to_markdown_with_pdf(self):
        """Test converting a PDF document to markdown."""
        # Read binary content from the fixture
        with open(self.PDF_FIXTURE, "rb") as f:
            pdf_data = f.read()

        # Call function
        result = binary_document_to_markdown(pdf_data, "pdf")

        # Basic assertions to check the conversion was successful
        assert isinstance(result, str)
        assert len(result) > 0
        # Check for typical markdown formatting - this will depend on your actual test file
        assert "#" in result or "-" in result or "*" in result


class TestDocumentPathToMarkdown:
    FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
    DOCX_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.docx")
    PDF_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.pdf")

    def test_with_docx(self) -> None:
        result = document_path_to_markdown(self.DOCX_FIXTURE)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_with_pdf(self) -> None:
        result = document_path_to_markdown(self.PDF_FIXTURE)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_uppercase_pdf_extension(self, tmp_path: Path) -> None:
        dest = tmp_path / "doc.PDF"
        shutil.copy(self.PDF_FIXTURE, dest)
        result = document_path_to_markdown(str(dest))
        assert isinstance(result, str)
        assert len(result) > 0

    def test_uppercase_docx_extension(self, tmp_path: Path) -> None:
        dest = tmp_path / "doc.DOCX"
        shutil.copy(self.DOCX_FIXTURE, dest)
        result = document_path_to_markdown(str(dest))
        assert isinstance(result, str)
        assert len(result) > 0

    def test_content_matches_binary_conversion(self) -> None:
        with open(self.PDF_FIXTURE, "rb") as f:
            pdf_bytes = f.read()
        expected = binary_document_to_markdown(pdf_bytes, "pdf")
        result = document_path_to_markdown(self.PDF_FIXTURE)
        assert result == expected

    def test_file_not_found(self) -> None:
        with pytest.raises(FileNotFoundError):
            document_path_to_markdown("/nonexistent/path/file.pdf")

    def test_unsupported_extension(self) -> None:
        with pytest.raises(ValueError):
            document_path_to_markdown(os.path.join(self.FIXTURES_DIR, "file.txt"))

    def test_unsupported_extension_xlsx(self) -> None:
        with pytest.raises(ValueError):
            document_path_to_markdown("/some/path/file.xlsx")

    def test_unsupported_extension_png(self) -> None:
        with pytest.raises(ValueError):
            document_path_to_markdown("/some/path/file.png")

    def test_no_extension_raises_value_error(self) -> None:
        with pytest.raises(ValueError):
            document_path_to_markdown("/some/path/noextension")

    def test_relative_path(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        shutil.copy(self.PDF_FIXTURE, tmp_path / "mcp_docs.pdf")
        monkeypatch.chdir(tmp_path)
        result = document_path_to_markdown("mcp_docs.pdf")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_path_with_spaces(self, tmp_path: Path) -> None:
        dest = tmp_path / "my document file.pdf"
        shutil.copy(self.PDF_FIXTURE, dest)
        result = document_path_to_markdown(str(dest))
        assert isinstance(result, str)
        assert len(result) > 0

    def test_returns_string(self) -> None:
        result = document_path_to_markdown(self.PDF_FIXTURE)
        assert isinstance(result, str)
