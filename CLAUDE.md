# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Create virtual environment
uv venv

# Install package in development mode (with all dependencies)
uv pip install -e .

# Run the MCP server
uv run main.py

# Run all tests
uv run pytest

# Run a single test file
uv run pytest tests/test_document.py

# Run a single test by name
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown::test_binary_document_to_markdown_with_docx
```

## Architecture

This is an MCP (Model Context Protocol) server that exposes Python functions as tools consumable by AI assistants.

**Entry point:** [main.py](main.py) creates a `FastMCP` instance and registers tools by passing functions to `mcp.tool()()`. The server runs via `mcp.run()`.

**Tool implementations** live in [tools/](tools/) as plain Python functions. They are imported into `main.py` and registered there. The `tools/` package currently has:
- [tools/math.py](tools/math.py) — `add()`, the reference example of a well-formed tool
- [tools/document.py](tools/document.py) — `binary_document_to_markdown()`, wraps `markitdown` to convert DOCX/PDF binary data to markdown text

**Tests** in [tests/](tests/) import tool functions directly and test them as ordinary Python — no MCP layer involved. Fixtures (`.docx`, `.pdf`) are in [tests/fixtures/](tests/fixtures/).

## Defining MCP Tools

Tools are plain Python functions registered with `mcp.tool()()` in `main.py`:

```python
# main.py
from tools.my_module import my_function
mcp.tool()(my_function)
```

Use `Field` from pydantic for parameter descriptions — these become the tool's parameter schema exposed to the AI:

```python
from pydantic import Field

def my_tool(
    param1: str = Field(description="Detailed description of this parameter"),
    param2: int = Field(description="Explain what this parameter does"),
) -> ReturnType:
    """One-line summary.

    Detailed explanation of functionality.

    When to use:
    - Scenario A
    - Scenario B

    When NOT to use:
    - Scenario C

    Examples:
    >>> my_tool("foo", 42)
    "expected output"
    """
    # implementation
```

The docstring becomes the tool's description — write it for an AI consumer, not a human developer. Explain intent, constraints, and edge cases explicitly. See [tools/math.py](tools/math.py) for the canonical pattern.
