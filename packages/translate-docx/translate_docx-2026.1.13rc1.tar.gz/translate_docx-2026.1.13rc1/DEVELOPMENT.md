# DOCX Parser - Development Guide

This guide explains the architecture, design decisions, and implementation details of the docx-parser project.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Module Descriptions](#module-descriptions)
3. [Data Model](#data-model)
4. [Key Design Decisions](#key-design-decisions)
5. [Implementation Patterns](#implementation-patterns)
6. [Testing Strategy](#testing-strategy)
7. [Performance Considerations](#performance-considerations)
8. [Common Patterns](#common-patterns)
9. [Troubleshooting](#troubleshooting)

---

## Architecture Overview

```
                    ┌─────────────────┐
                    │   DOCX File     │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  extractor.py   │
                    │  (Extraction)   │
                    └────────┬────────┘
                             │
                    ┌────────▼────────────────┐
                    │   Document (dataclass)  │
                    │  + metadata             │
                    │  + sections             │
                    │  + formatting           │
                    └────────┬────────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
    ┌────▼────────┐  ┌──────▼──────┐  ┌────────▼───────┐
    │translator.py│  │rebuilder.py │  │Other uses      │
    │(Translation)│  │ (Rebuild)   │  │(Analyze, etc)  │
    └────┬────────┘  └──────┬──────┘  └────────────────┘
         │                  │
    ┌────▼─────────────────▼────┐
    │   Translated Document     │
    │   (or Modified Document)  │
    │   (or Original Document)  │
    └────┬─────────────────────┘
         │
    ┌────▼────────────────────┐
    │  rebuilt_document.docx  │
    └─────────────────────────┘
```

### Three-Phase Pipeline

1. **Extraction** (`extractor.py`): Parse DOCX → Dataclass
   - Converts python-docx objects into structured dataclasses
   - Preserves all formatting attributes
   - Detects sections based on bold headers
   - Extracts metadata (page settings, line numbering)

2. **Transformation** (user code): Manipulate dataclass
   - Translation via `translator.py`
   - Or custom transformations by user
   - Document structure remains intact

3. **Rebuilding** (`rebuilder.py`): Dataclass → DOCX
   - Converts dataclass back to python-docx format
   - Restores all formatting attributes
   - Recreates sections and structure

---

## Module Descriptions

### `models.py` (78 lines, 100% coverage)

**Purpose:** Dataclass definitions for document structure.

**Key Classes:**

```python
@dataclass
class RunFormatting:
    """Text-level formatting (bold, italic, colors, fonts)."""
    bold: Optional[bool] = None
    italic: Optional[bool] = None
    # ... 6 more fields

@dataclass
class TextRun:
    """Minimal text unit with consistent formatting."""
    text: str
    formatting: RunFormatting

@dataclass
class ParagraphFormatting:
    """Paragraph-level formatting (alignment, spacing, indentation)."""
    alignment: str = "left"
    # ... 8 more fields

@dataclass
class Paragraph:
    """Container for text runs with formatting."""
    runs: List[TextRun]
    formatting: ParagraphFormatting
    # ... more fields

@dataclass
class Section:
    """Document section (header + body paragraphs)."""
    header: Paragraph
    paragraphs: List[Paragraph]

@dataclass
class LineNumbering:
    """Line numbering configuration (XML-based)."""
    enabled: bool
    # ... more fields

@dataclass
class PageSettings:
    """Page layout (width, height, margins, all in twips)."""
    width: Optional[int] = None
    # ... 7 more fields

@dataclass
class DocumentMetadata:
    """Document-level metadata."""
    line_numbering: LineNumbering
    page_settings: PageSettings
    # ... more fields

@dataclass
class Document:
    """Top-level document container."""
    metadata: DocumentMetadata
    sections: List[Section]
    preamble_paragraphs: List[Paragraph]
```

**Design Rationale:**
- Flat hierarchy (not deeply nested) for ease of use
- Optional fields (`Optional[type]`) for defaults
- `None` vs `False` distinction: `None` = "use default", `False` = "don't apply"
- All measurements in twips (1/20th point) for precision

---

### `extractor.py` (116 lines, 93% coverage)

**Purpose:** Convert DOCX files to Document dataclasses.

**Public Functions:**

1. **`extract_document(docx_path, header_detector=None) -> Document`**
   - Entry point for extraction
   - Calls helper functions for each component
   - Returns complete Document object

2. **`extract_paragraph(paragraph, is_header=False) -> Paragraph`**
   - Extracts single paragraph with all runs
   - Marks whether it's a header
   - Used by section splitting

3. **`extract_text_run(run) -> TextRun`**
   - Lowest-level extraction
   - Extracts text and formatting from python-docx Run

4. **`extract_run_formatting(run) -> RunFormatting`**
   - Extracts all formatting attributes
   - Converts colors to hex strings
   - Detects superscript/subscript

5. **`is_section_header(paragraph, header_detector=None) -> bool`**
   - Multi-criteria header detection:
     - Check style name for "Heading X"
     - Check if all runs are bold AND text < 200 chars
     - Support custom detector

6. **`split_into_sections(paragraphs, header_detector=None) -> Tuple[List[Section], List[Paragraph]]`**
   - Splits paragraphs by headers
   - Returns (sections, preamble)
   - Preamble = paragraphs before first header

7. **`extract_line_numbering(section) -> LineNumbering`**
   - XML-based extraction
   - Finds w:lnNumType element
   - Extracts start, increment, restart attributes

8. **`extract_metadata(docx_doc) -> DocumentMetadata`**
   - Aggregates all metadata
   - Calls helper functions
   - Returns DocumentMetadata object

**Implementation Pattern:**
```
High-level → Medium-level → Low-level
extract_document() → extract_paragraph() → extract_text_run()
                  ↘ extract_metadata() → extract_line_numbering()
                  ↘ is_section_header() / split_into_sections()
```

**Key Decisions:**
- Multi-criteria header detection balances false positives/negatives
- XML access for line numbering (python-docx limitation workaround)
- Custom detector support for non-standard documents

---

### `rebuilder.py` (130 lines, 90% coverage)

**Purpose:** Reconstruct DOCX files from Document dataclasses.

**Public Functions:**

1. **`rebuild_document(doc_data, output_path) -> None`**
   - Entry point for rebuilding
   - Orchestrates all sub-functions
   - Saves to DOCX file

2. **`add_paragraph_to_document(docx_doc, para_data, style=None) -> DXMLParagraph`**
   - Adds paragraph to python-docx Document
   - Applies formatting via helper functions
   - Fallback to "Normal" if style not found

3. **`apply_run_formatting(run, formatting) -> None`**
   - Applies RunFormatting to python-docx Run
   - Handles bold, italic, fonts, colors
   - Sets superscript/subscript

4. **`apply_paragraph_formatting(para, formatting) -> None`**
   - Applies ParagraphFormatting to Paragraph
   - Sets alignment, spacing, indentation
   - Handles keep_together, page_break_before, etc.

5. **`apply_page_settings(section, page_settings) -> None`**
   - Sets page dimensions
   - Sets margins
   - Sets header/footer distances

6. **`apply_line_numbering(section, line_numbering) -> None`**
   - XML manipulation to set line numbering
   - Creates w:lnNumType element if needed
   - Updates existing if already present

7. **`apply_metadata(docx_doc, metadata) -> None`**
   - Applies all metadata to document
   - Orchestrates other apply_* functions

**Key Decisions:**
- Safe fallback for missing styles
- XML manipulation for line numbering (matches extraction)
- Try/except for graceful degradation

---

### `translator.py` (51 lines, 86% coverage)

**Purpose:** Translation interface and implementations.

**Classes:**

1. **`TranslatorInterface` (Abstract Base)**
   - `translate(text, source_lang, target_lang) -> str` (abstract)
   - `should_translate_run(run) -> bool` (virtual)

2. **`CallbackTranslator`**
   - Wraps function for translation
   - Useful for APIs

3. **`ManualTranslator`**
   - Static dictionary lookups
   - Useful for testing

4. **`NoOpTranslator`**
   - No-op implementation
   - Useful for testing workflows

**Functions:**

1. **`translate_document(doc, translator, src, tgt) -> Document`**
   - Deep copies document
   - Iterates all paragraphs (preamble + sections)
   - Calls translator.should_translate_run() for filtering
   - Translates remaining runs
   - Returns new document

2. **`extract_translate_rebuild(input_path, output_path, translator, src, tgt) -> Document`**
   - Convenience function
   - Calls extract_document, translate_document, rebuild_document
   - Returns translated document

**Key Decisions:**
- Pluggable interface via abstract base class
- Deep copy to avoid modifying original
- Automatic citation (superscript) preservation
- Language codes as parameters for API flexibility

---

### `utils.py` (45 lines, 67% coverage)

**Purpose:** Utility functions for conversions.

**Functions:**

1. **Color conversions**
   - `hex_to_rgb_color(hex_color) -> RGBColor`
   - `color_to_hex(color_obj) -> str`

2. **Unit conversions**
   - `points_to_twips(points) -> int`
   - `twips_to_points(twips) -> int`
   - `inches_to_twips(inches) -> int`
   - `twips_to_inches(twips) -> int`

3. **Alignment conversion**
   - `normalize_alignment(alignment) -> str`

**Design Rationale:**
- Centralized conversions for code reuse
- All measurements use twips internally for precision
- Safe fallbacks for invalid inputs

---

### `__init__.py`

**Purpose:** Package initialization and exports.

**Exports:**
- All dataclasses from `models`
- All public functions from `extractor`
- All public functions from `rebuilder`
- All translator classes and functions

**Pattern:**
```python
from .modules import (
    Class1, Class2,  # Dataclasses
    function1, function2,  # Functions
)

__all__ = [
    "Class1", "Class2",
    "function1", "function2",
]
```

---

## Data Model

### Design Principles

1. **Explicit formatting**: All formatting stored explicitly (never defaults)
   - Allows lossless reconstruction
   - Makes formatting visible in code

2. **Optional vs None**:
   - `None` = "not specified, use document defaults"
   - `False` = "explicitly disable this formatting"
   - Used for bold, italic, underline (tri-state)

3. **Flat hierarchy**: Not deeply nested
   - Easy to iterate and modify
   - No complex traversal needed

4. **Twips for measurements**: Precision, no floating point errors
   - All page/margin/indent values in twips
   - 1 point = 20 twips
   - 1 inch = 1440 twips

### Example: Document Structure

```
Document
  metadata:
    line_numbering: LineNumbering(enabled=True, start=1)
    page_settings: PageSettings(width=9144000, height=12700000)
    default_font: "Times New Roman"
    default_font_size: 12

  preamble_paragraphs: [
    Paragraph(
      runs: [
        TextRun(text="Preamble text", formatting=RunFormatting())
      ],
      formatting: ParagraphFormatting(alignment="left")
    )
  ]

  sections: [
    Section(
      header: Paragraph(
        runs: [TextRun(text="Section 1", formatting=RunFormatting(bold=True))],
        formatting: ParagraphFormatting(),
        is_header: True
      ),
      paragraphs: [
        Paragraph(...),  # Body paragraphs
        Paragraph(...),
      ]
    ),
    Section(...)  # More sections
  ]
```

---

## Key Design Decisions

### 1. Dataclass Hierarchy

**Decision:** Use flat dataclass hierarchy (Document → Section → Paragraph → TextRun)

**Why:**
- Simple to work with
- Easy to iterate
- Easy to modify

**Alternatives considered:**
- Tree structure (nested): Harder to iterate, harder to modify
- Single flat list: Loses structure information

---

### 2. Multiple Formatting Levels

**Decision:** Separate RunFormatting and ParagraphFormatting

**Why:**
- Reflects DOCX model accurately
- Allows independent manipulation
- Clear separation of concerns

**Structure:**
```
Paragraph → ParagraphFormatting (alignment, spacing)
Paragraph → runs[*] → TextRun → RunFormatting (bold, font, color)
```

---

### 3. Bold Header Detection Heuristic

**Decision:** Multi-criteria detection:
1. Check for "Heading X" style
2. Or check all bold + short text

**Why:**
- Balances false positives and negatives
- Works with both styled and unstyled documents
- Configurable via custom detector

**Code:**
```python
def is_section_header(paragraph, header_detector=None):
    if header_detector:
        return header_detector(paragraph)

    all_bold = all(run.bold for run in paragraph.runs if run.text.strip())
    is_heading_style = paragraph.style.name.startswith("Heading")
    is_short = 0 < len(paragraph.text.strip()) < 200

    return is_heading_style or (all_bold and is_short)
```

---

### 4. XML Manipulation for Line Numbering

**Decision:** Direct XML access via `qn()` for line numbering

**Why:**
- python-docx doesn't expose line numbering API
- XML manipulation is direct and reliable
- Try/except for safe error handling

**Code:**
```python
sect_pr = section._sectPr
ln_num_type = sect_pr.find(qn('w:lnNumType'))
if ln_num_type is None:
    ln_num_type = parse_xml(ln_num_xml)
    sect_pr.append(ln_num_type)
else:
    ln_num_type.set(qn('w:start'), str(line_numbering.start))
```

---

### 5. Citation Preservation via Superscript Detection

**Decision:** Automatically skip superscripts/subscripts during translation

**Why:**
- Citations must stay in original language
- Detected via `run.font.superscript == True`
- Automatic, no user configuration needed

**Code:**
```python
class TranslatorInterface:
    def should_translate_run(self, run: TextRun) -> bool:
        if run.formatting.is_superscript or run.formatting.is_subscript:
            return False
        if not run.text or not run.text.strip():
            return False
        return True
```

---

### 6. Pluggable Translation Interface

**Decision:** Abstract TranslatorInterface with multiple implementations

**Why:**
- Supports any translation backend
- Easy to integrate with APIs
- Easy to test with mock translators

**Interface:**
```python
class TranslatorInterface(ABC):
    @abstractmethod
    def translate(self, text, source_lang, target_lang) -> str:
        pass

    def should_translate_run(self, run) -> bool:
        # Default: skip superscripts
        return not (run.formatting.is_superscript or run.formatting.is_subscript)
```

---

### 7. Deep Copy for Non-Destructive Translation

**Decision:** `translate_document()` returns new Document object

**Why:**
- Original document unchanged
- User can compare before/after
- Easy to debug

**Code:**
```python
def translate_document(doc, translator, source_lang, target_lang):
    translated_doc = deepcopy(doc)
    # Modify translated_doc, not doc
    return translated_doc
```

---

## Implementation Patterns

### Pattern 1: Multi-level Function Calls

Functions are organized by level:

```python
# High-level (entry point)
def extract_document(docx_path):
    docx_doc = DocxDocument(docx_path)
    # ... call medium-level functions

# Medium-level (orchestration)
def extract_metadata(docx_doc):
    # ... call low-level functions

# Low-level (basic operations)
def extract_run_formatting(run):
    # ... basic extraction
```

**Benefit:** Easy to test at each level independently

---

### Pattern 2: Try/Except for Graceful Degradation

```python
try:
    para = docx_doc.add_paragraph(style=style)
except KeyError:
    # Fall back to Normal style
    para = docx_doc.add_paragraph(style="Normal")
```

**Benefit:** Robustness with custom or missing styles

---

### Pattern 3: Iterator Pattern for Collection Processing

```python
# Translate all paragraphs
for para in doc.preamble_paragraphs:
    for text_run in para.runs:
        if translator.should_translate_run(text_run):
            text_run.text = translator.translate(...)

# Iterate sections
for section in doc.sections:
    for para in section.paragraphs:
        # ... same processing
```

**Benefit:** Consistent processing, easy to understand

---

### Pattern 4: Builder Pattern for Complex Objects

```python
# Extract piece by piece, build Document
metadata = extract_metadata(docx_doc)
sections, preamble = split_into_sections(docx_doc.paragraphs)

doc = Document(
    metadata=metadata,
    sections=sections,
    preamble_paragraphs=preamble,
)
```

---

## Testing Strategy

### Test Organization

```
tests/
├── test_extractor.py     # Extraction tests
├── test_rebuilder.py     # Rebuild tests
├── test_roundtrip.py     # Extract→Rebuild→Extract tests
├── test_translator.py    # Translation tests
└── conftest.py           # Shared fixtures
```

### Coverage Goals

- **Target:** ≥88% overall
- **models.py:** 100% (all code tested)
- **extractor.py:** 93% (error paths not tested)
- **rebuilder.py:** 90% (error paths not tested)
- **translator.py:** 86% (error paths not tested)

### Test Pattern

```python
class TestFeature:
    """Test a specific feature."""

    def test_basic_case(self):
        """Test basic happy path."""
        input_data = create_test_data()
        result = function_under_test(input_data)
        assert result.expected_field == expected_value

    def test_edge_case(self):
        """Test edge cases."""
        # ... test edge case

    def test_error_handling(self):
        """Test error handling."""
        with pytest.raises(ValueError):
            function_under_test(invalid_input)
```

### Test Fixture Pattern

```python
# conftest.py
@pytest.fixture
def sample_document():
    """Create sample document for testing."""
    return Document(...)

# test_*.py
def test_with_fixture(sample_document):
    result = process_document(sample_document)
    assert result is not None
```

---

## Performance Considerations

### Optimization Principles

1. **Use comprehensions**: Fast list creation
2. **Iterate once**: Don't search repeatedly
3. **Avoid nested loops**: O(n²) complexity bad
4. **Use generators** for large datasets

### Performance Characteristics

- **Extraction:** O(n) where n = number of paragraphs
- **Translation:** O(n × m) where m = avg runs per paragraph
- **Rebuilding:** O(n × m) to recreate formatting
- **Round-trip:** O(n) + O(n) + O(n) = O(n)

### Memory Usage

- Document dataclass: Minimal overhead
- Deep copy: ~2x memory usage during translation
- Large documents: ~100K paragraphs tested successfully

---

## Common Patterns

### Pattern: Processing All Paragraphs

```python
# Preamble
for para in doc.preamble_paragraphs:
    process_paragraph(para)

# Sections
for section in doc.sections:
    process_paragraph(section.header)
    for para in section.paragraphs:
        process_paragraph(para)
```

### Pattern: Processing All Runs

```python
for para in doc.sections[0].paragraphs:
    for run in para.runs:
        if should_process(run):
            process_run(run)
```

### Pattern: Custom Translator

```python
class MyTranslator(TranslatorInterface):
    def translate(self, text, source_lang, target_lang):
        return my_api(text, source_lang, target_lang)

    def should_translate_run(self, run):
        # Skip URLs too
        if run.text.startswith("http"):
            return False
        return super().should_translate_run(run)

translator = MyTranslator()
translated = translate_document(doc, translator, "de", "en")
```

---

## Troubleshooting

### Issue: Extraction seems slow

**Solution:**
- Profile: `python -m cProfile -s cumulative script.py`
- Likely: Multiple passes over data
- Fix: Use single iterator pattern

### Issue: Translation missing some text

**Solution:**
- Check: Is text in superscript? (won't translate)
- Check: Is text in whitespace-only run? (skipped)
- Verify: `should_translate_run()` returning True

### Issue: Rebuild changes formatting

**Solution:**
- Style might not exist in target document (falls back to Normal)
- Font might not be available (falls back to default)
- This is expected behavior

### Issue: Custom styles lost

**Explanation:**
- When rebuilding, custom styles may not be in new document
- Falls back to "Normal" style
- Content and formatting preserved, just different style name

### Issue: Test coverage not increasing

**Solution:**
- Check which lines not covered: `pytest --cov-report=term-missing`
- Add tests for error paths
- Mock external dependencies if needed

---

## Adding New Features

### Checklist

1. **Research**
   - Understand existing code
   - Check if similar feature exists
   - Plan implementation

2. **Test First**
   - Write test(s) in `tests/test_*.py`
   - Verify test fails (TDD)

3. **Implementation**
   - Implement feature in appropriate module
   - Update type hints
   - Add docstrings

4. **Integration**
   - Update `__init__.py` if adding public API
   - Update `README.md` if user-facing
   - Update examples if relevant

5. **Verification**
   - Run full test suite: `pytest`
   - Check coverage: ≥88%
   - Format code: `black src/`
   - Lint: `flake8 src/`

### Example: Adding Line Spacing Support

```python
# 1. Add test
def test_extracts_line_spacing(self):
    para = create_para_with_line_spacing(1.5)
    result = extract_paragraph(para)
    assert result.formatting.line_spacing == 1.5

# 2. Implement extraction
def extract_paragraph_formatting(para):
    return ParagraphFormatting(
        line_spacing=para.paragraph_format.line_spacing,
        # ...
    )

# 3. Implement rebuilding
def apply_paragraph_formatting(para, fmt):
    if fmt.line_spacing is not None:
        para.paragraph_format.line_spacing = fmt.line_spacing
    # ...

# 4. Update __init__.py if new class added
# (No change needed here)

# 5. Run tests
pytest  # Should all pass!
```

---

## Version History

- **0.1.0** (Current): Initial implementation
  - Extraction with all formatting
  - Rebuilding with structure preservation
  - Translation with citation preservation
  - 143 tests, 88% coverage

---

## Related Reading

- [python-docx documentation](https://python-docx.readthedocs.io/)
- [OOXML specification](http://www.ecma-international.org/publications/standards/Ecma-376.htm)
- [XML for Office Open XML](https://en.wikipedia.org/wiki/Office_Open_XML)

