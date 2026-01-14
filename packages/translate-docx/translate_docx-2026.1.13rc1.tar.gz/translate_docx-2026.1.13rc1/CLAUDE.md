# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**docx-parser** is a Python-based DOCX parser and rebuilder that extracts structured data from Word documents and enables content translation while preserving formatting.

### Core Architecture

The project follows a three-phase pipeline:

1. **Extraction Phase** - Parse DOCX files into structured dataclass objects
   - Extract metadata: line numbering, page offsets, formatting information
   - Split document into sections based on bold headers
   - Identify and extract superscripts (citations/references)
   - Preserve formatting attributes (bold, italic, fonts, colors, etc.)

2. **Transformation Phase** - Manipulate the structured data
   - Translate text content while preserving structure
   - Modify metadata if needed
   - Update references and citations

3. **Rebuild Phase** - Reconstruct DOCX files from dataclass objects
   - Recreate document with same layout, page offsets, line numbering
   - Restore all formatting (headers, bold text, superscripts)
   - Maintain original document structure exactly

### Data Model

The extraction process creates dataclass objects with:
- Document-level metadata (page offsets, line numbering configuration)
- Section objects containing:
  - Header text (bold header that defined the section)
  - Body paragraphs with formatting attributes
  - Embedded superscripts (citations/references)
  - Position/offset information for reconstruction

## Repository Structure

- `user_data/` - Test/sample DOCX files (e.g., `input_example.docx`), ignored by git to avoid committing large files
- `src/` - Python source code (to be created)
- `tests/` - Unit tests (to be created)

## Common Development Commands

```bash
# Install dependencies
pip install python-docx

# Run tests
pytest

# Run single test
pytest tests/test_file.py::test_function

# Run linting
flake8 src/ tests/

# Format code
black src/ tests/
```

## Key Dependencies

- `python-docx` - DOCX file parsing and creation
- `dataclasses` - Built-in Python module for structured data

## Development Notes

- The `user_data/` directory stores test documents and is intentionally ignored by git
- Use `input_example.docx` as reference for testing parsing functionality
- Extraction and rebuild should be lossless - a document parsed and immediately rebuilt should be identical to the original
- Pay special attention to preserving exact formatting attributes and positional information during the round-trip
