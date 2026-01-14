"""Pytest configuration and fixtures."""

import sys
from pathlib import Path

# Add translate_docx directory to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent / "translate_docx"))
