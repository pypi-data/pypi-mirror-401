# Contributing to DOCX Parser

Thank you for your interest in contributing! This guide explains how to contribute to the project.

## Getting Started

### Prerequisites

- Python 3.8+
- git
- Basic familiarity with python-docx

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/pixelprotest/docx-parser.git
cd docx-parser

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Or with uv
uv venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify setup
pytest --version
black --version
```

### Verify Installation

```bash
# Run test suite
pytest

# Should show: 143 passed in ~12s
```

## Development Workflow

### 1. Create Feature Branch

```bash
# Create branch with descriptive name
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

**Naming convention:**
- `feature/` - New functionality
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test improvements

### 2. Make Changes

#### File Structure

```
src/
├── models.py        # Dataclass definitions (don't add new unless needed)
├── extractor.py     # DOCX extraction logic
├── rebuilder.py     # DOCX rebuilding logic
├── translator.py    # Translation functionality
├── utils.py         # Utility functions
└── __init__.py      # Package exports (update when adding new public APIs)

tests/
├── test_extractor.py     # Extraction tests
├── test_rebuilder.py     # Rebuild tests
├── test_roundtrip.py     # Round-trip tests
├── test_translator.py    # Translation tests
└── conftest.py           # Pytest configuration

examples/
├── example_*.py          # Runnable examples
```

#### Editing Guidelines

**For new functionality:**
1. Add tests first (`tests/test_*.py`)
2. Implement feature in appropriate `src/` module
3. Update docstrings and type hints
4. Update `src/__init__.py` if adding public API
5. Run full test suite: `pytest`

**For bug fixes:**
1. Add regression test demonstrating the bug
2. Fix the bug
3. Verify test now passes
4. Run full suite: `pytest`

**For documentation:**
1. Update relevant `.md` files
2. Update docstrings if modifying code
3. Update examples if changing API

### 3. Write Tests

**Test file location:** `tests/test_<module>.py`

**Test class naming:** `Test<Feature>`

**Test method naming:** `test_<specific_behavior>`

**Example:**
```python
import pytest
from docx_parser import extract_document, extract_paragraph

class TestExtractFeature:
    """Tests for new extraction feature."""

    def test_extracts_basic_case(self):
        """Should extract basic case."""
        para = create_test_paragraph("text")
        result = extract_paragraph(para)
        assert result.runs[0].text == "text"

    def test_handles_edge_case(self):
        """Should handle edge case."""
        para = create_test_paragraph("")
        result = extract_paragraph(para)
        assert len(result.runs) == 0

    def test_raises_on_invalid_input(self):
        """Should raise on invalid input."""
        with pytest.raises(ValueError):
            extract_paragraph(None)
```

**Coverage requirement:** Maintain ≥88% coverage

```bash
# Check coverage
pytest --cov=src --cov-report=term-missing

# Generate HTML report
pytest --cov=src --cov-report=html
# Open htmlcov/index.html in browser
```

### 4. Code Quality

#### Style Guide

Use **black** for formatting and **flake8** for linting:

```bash
# Format code
black src/ tests/ examples/

# Check for issues
flake8 src/ tests/ examples/

# Or fix automatically (limited)
black src/
```

**Style guidelines:**
- Max line length: 88 characters (black default)
- 4 spaces per indentation level
- Use type hints for all function parameters and returns
- Write docstrings for all public functions

#### Type Hints

All functions should have type hints:

```python
from typing import Optional, List, Tuple
from models import Document, Paragraph

def process_document(
    doc: Document,
    filter_func: Optional[callable] = None,
) -> Tuple[List[Paragraph], int]:
    """Process document with optional filtering.

    Args:
        doc: Document to process
        filter_func: Optional filter function

    Returns:
        Tuple of (filtered paragraphs, count)
    """
    pass
```

#### Docstrings

Use Google-style docstrings:

```python
def extract_document(docx_path: str) -> Document:
    """Extracts a DOCX file into a Document dataclass.

    Parses the DOCX file and creates structured dataclass
    representation preserving all formatting.

    Args:
        docx_path: Path to DOCX file

    Returns:
        Document object with all content and formatting

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file is not a valid DOCX

    Example:
        >>> doc = extract_document("input.docx")
        >>> print(len(doc.sections))
        5
    """
    pass
```

### 5. Test Your Changes

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_extractor.py

# Run specific test
pytest tests/test_extractor.py::TestExtractParagraph::test_basic

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=src
```

**Target:** 143 tests passing, ≥88% coverage

### 6. Commit Changes

```bash
# Stage changes
git add src/ tests/ examples/

# Commit with descriptive message
git commit -m "Add feature: [short description]

Detailed explanation of what was changed and why.
- List specific changes
- Explain any decisions made
- Reference issues if applicable (#123)

🤖 Generated with Claude Code

Co-Authored-By: Your Name <your.email@example.com>"
```

**Commit message format:**
- First line: Short summary (<50 chars)
- Blank line
- Detailed explanation (wrap at 72 chars)
- Reference issues: "Fixes #123" or "Related to #456"
- Use past tense: "Add", "Fix", "Update" (not "Added", "Fixed")

### 7. Push and Create Pull Request

```bash
# Push to remote
git push origin feature/your-feature-name

# Create pull request via GitHub web interface
# Or use GitHub CLI:
gh pr create --title "Your feature title" --body "Description"
```

**PR requirements:**
- [ ] All tests pass (`pytest`)
- [ ] Coverage ≥88% (`pytest --cov=src`)
- [ ] Code formatted (`black src/`)
- [ ] No linting issues (`flake8 src/`)
- [ ] Docstrings added/updated
- [ ] Type hints added/updated
- [ ] Examples updated if API changed

## Code Review Process

### What We Look For

- ✅ Tests present and passing
- ✅ Code style consistent (black/flake8)
- ✅ Type hints complete
- ✅ Docstrings clear and accurate
- ✅ No breaking changes to public API
- ✅ Performance reasonable (no N² loops for N items)
- ✅ Error handling appropriate
- ✅ Edge cases considered

### Common Feedback

**"Missing type hints"**
```python
# Before
def process(data):
    return data

# After
from typing import List
def process(data: List[str]) -> List[str]:
    return data
```

**"Add test for this case"**
```python
def test_handles_empty_input(self):
    """Should handle empty input gracefully."""
    result = extract_document([])
    assert result.sections == []
```

**"Simplify/DRY this up"**
- Don't repeat similar code blocks
- Extract common patterns into helper functions
- Use existing utilities

**"Update docstring"**
```python
def my_func(x: int) -> str:
    """Convert integer to string.

    Args:
        x: Integer to convert

    Returns:
        String representation of x
    """
```

## Testing Tips

### Running Tests Efficiently

```bash
# Run only failed tests from last run
pytest --lf

# Run tests matching pattern
pytest -k "test_extract"

# Run tests in parallel (faster on multicore)
pytest -n auto

# Stop on first failure
pytest -x

# Show most time-consuming tests
pytest --durations=10
```

### Writing Effective Tests

**Good test:**
```python
def test_extracts_bold_formatting(self):
    """Should extract bold formatting from runs."""
    para = create_test_paragraph([
        create_run("plain"),
        create_run("bold", bold=True),
    ])
    result = extract_paragraph(para)
    assert result.runs[0].formatting.bold is None
    assert result.runs[1].formatting.bold is True
```

**Not as good:**
```python
def test_extraction(self):
    """Test extraction."""
    para = get_para()
    result = extract_paragraph(para)
    assert result is not None
```

### Test Fixtures

Use `conftest.py` for shared test utilities:

```python
# tests/conftest.py
import pytest

@pytest.fixture
def sample_document():
    """Create a sample document for testing."""
    from docx import Document
    doc = Document()
    doc.add_paragraph("Test paragraph")
    return doc

# tests/test_extractor.py
def test_with_fixture(sample_document):
    from docx_parser import extract_document
    # Use sample_document fixture
```

## Performance Considerations

### Optimization Guidelines

**Good:**
```python
# Use comprehensions (fast)
texts = [run.text for run in para.runs]

# Iterate once
for run in para.runs:
    process(run)
```

**Not as good:**
```python
# Don't search repeatedly
for run in para.runs:
    if run in para.runs:  # Redundant search
        pass

# Don't nest iterations unnecessarily
for para in doc.paragraphs:
    for run in para.runs:
        for char in run.text:
            for x in some_list:  # 4 nested loops!
                pass
```

### Profiling

```bash
# Profile test execution
pytest --profile

# Profile specific operation
python -m cProfile -s cumulative script.py
```

## Documentation

### Types of Documentation

1. **Docstrings** - In-code function documentation
2. **README.md** - Project overview and quick start
3. **API_REFERENCE.md** - Detailed API documentation
4. **Examples** - Working example scripts
5. **Comments** - Explain "why", not "what"

### Updating Documentation

**When to update:**
- Adding new public function/class
- Changing function signature
- Changing expected behavior
- Adding new example

**Where to update:**
- Add docstring in code
- Update `API_REFERENCE.md` for public API
- Update `README.md` if user-facing
- Add example if complex

## Common Issues

### Issue: Tests fail locally but pass in CI

**Likely causes:**
- Different Python version
- Missing dependency
- Hardcoded path that doesn't exist on CI

**Solution:**
```bash
# Check Python version
python --version

# Verify all deps installed
pip list

# Use relative paths
os.path.join(os.path.dirname(__file__), "fixture.txt")
```

### Issue: Import errors in tests

**Solution:**
```python
# Make sure conftest.py exists in tests/
# tests/conftest.py should exist (even if empty)

# Or add to path explicitly
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
```

### Issue: Slow tests

**Solution:**
```bash
# Find slow tests
pytest --durations=10

# Run only fast tests
pytest -m "not slow"

# Or use fixtures to avoid repeated setup
@pytest.fixture
def expensive_resource():
    # Set up once per test session
    return create_expensive_thing()
```

## Release Process

### Creating a Release

1. Update version in `src/__init__.py`
2. Update `CHANGELOG.md` (if it exists)
3. Run full test suite: `pytest`
4. Create git tag: `git tag v0.2.0`
5. Push tag: `git push origin v0.2.0`
6. GitHub Actions will create release

### Versioning

Follow [Semantic Versioning](https://semver.org/):
- **MAJOR** - Breaking API changes
- **MINOR** - New features, backwards compatible
- **PATCH** - Bug fixes

## Getting Help

### Resources

- [README.md](./README.md) - Project overview
- [API_REFERENCE.md](./API_REFERENCE.md) - Detailed API docs
- [examples/](./examples/) - Working examples
- [python-docx docs](https://python-docx.readthedocs.io/)

### Questions?

- Check existing issues/discussions
- Create new issue with:
  - Clear title
  - Description of problem
  - Minimal reproducible example
  - Python version and OS

## Code of Conduct

Be respectful and constructive. We value:
- Helpful feedback
- Learning from mistakes
- Collaborative problem-solving
- Inclusive community

---

Thank you for contributing!
