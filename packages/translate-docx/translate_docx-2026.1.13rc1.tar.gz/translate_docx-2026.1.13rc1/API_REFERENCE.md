# DOCX Parser - API Reference

Complete API documentation for docx-parser library.

## Table of Contents

1. [Extraction API](#extraction-api)
2. [Rebuilding API](#rebuilding-api)
3. [Translation API](#translation-api)
4. [Data Models](#data-models)
5. [Utilities](#utilities)
6. [Error Handling](#error-handling)

---

## Extraction API

### `extract_document(docx_path: str, header_detector: Optional[Callable] = None) -> Document`

Extracts a DOCX file into a Document dataclass structure.

**Parameters:**
- `docx_path` (str): Path to DOCX file to extract
- `header_detector` (callable, optional): Custom function `(paragraph) -> bool` to detect headers. If None, uses default heuristics (bold text + short or "Heading X" style)

**Returns:**
- `Document`: Complete document structure with all content and formatting

**Raises:**
- `FileNotFoundError`: If DOCX file doesn't exist

**Example:**
```python
from docx_parser import extract_document

# Default header detection
doc = extract_document("document.docx")

# Custom header detection
def my_detector(para):
    return para.style.name.startswith("CustomHeader")

doc = extract_document("document.docx", header_detector=my_detector)
```

---

### `extract_paragraph(paragraph: DXMLParagraph, is_header: bool = False) -> Paragraph`

Extracts a single paragraph from python-docx paragraph.

**Parameters:**
- `paragraph`: python-docx Paragraph object
- `is_header` (bool): Whether to mark as section header

**Returns:**
- `Paragraph`: Extracted paragraph with all runs and formatting

**Example:**
```python
from docx import Document as DocxDocument
from docx_parser import extract_paragraph

docx_doc = DocxDocument("input.docx")
for para in docx_doc.paragraphs:
    extracted = extract_paragraph(para)
    print(f"Text: {''.join(r.text for r in extracted.runs)}")
```

---

### `extract_text_run(run: DXMLRun) -> TextRun`

Extracts a text run from python-docx run object.

**Parameters:**
- `run`: python-docx Run object

**Returns:**
- `TextRun`: Text run with formatting

**Example:**
```python
from docx_parser import extract_text_run

for para in doc.paragraphs:
    for run in para.runs:
        text_run = extract_text_run(run)
        print(f"Text: {text_run.text}, Bold: {text_run.formatting.bold}")
```

---

### `extract_run_formatting(run: DXMLRun) -> RunFormatting`

Extracts formatting from a text run.

**Parameters:**
- `run`: python-docx Run object

**Returns:**
- `RunFormatting`: Formatting object with bold, italic, fonts, colors, etc.

**Properties extracted:**
- `bold`, `italic`, `underline`
- `font_name`, `font_size`
- `color` (as hex string)
- `is_superscript`, `is_subscript`

---

### `extract_paragraph_formatting(paragraph: DXMLParagraph) -> ParagraphFormatting`

Extracts formatting from a paragraph.

**Parameters:**
- `paragraph`: python-docx Paragraph object

**Returns:**
- `ParagraphFormatting`: Alignment, spacing, indentation, etc.

---

### `extract_metadata(docx_doc: DXMLDocument) -> DocumentMetadata`

Extracts document-level metadata.

**Parameters:**
- `docx_doc`: python-docx Document object

**Returns:**
- `DocumentMetadata`: Page settings, line numbering, default fonts

---

### `split_into_sections(paragraphs: List[DXMLParagraph], header_detector: Optional[Callable] = None) -> Tuple[List[Section], List[Paragraph]]`

Splits paragraphs into sections based on header detection.

**Parameters:**
- `paragraphs`: List of paragraphs to split
- `header_detector` (callable, optional): Custom header detection function

**Returns:**
- Tuple of:
  - `sections`: List of Section objects (each with header + body)
  - `preamble`: List of Paragraph objects before first header

**Behavior:**
- Paragraphs before first header go to preamble
- Each header starts a new section
- Following paragraphs belong to that section

**Example:**
```python
from docx_parser import split_into_sections

sections, preamble = split_into_sections(doc.paragraphs)
print(f"Preamble: {len(preamble)} paragraphs")
print(f"Sections: {len(sections)}")
for section in sections:
    header_text = "".join(r.text for r in section.header.runs)
    print(f"  {header_text}: {len(section.paragraphs)} paragraphs")
```

---

### `is_section_header(paragraph: DXMLParagraph, header_detector: Optional[Callable] = None) -> bool`

Determines if a paragraph is a section header.

**Parameters:**
- `paragraph`: python-docx Paragraph to check
- `header_detector` (callable, optional): Custom detection function

**Returns:**
- `bool`: True if paragraph is a header, False otherwise

**Default heuristics:**
1. Style name starts with "Heading" (case-insensitive)
2. OR: All runs are bold AND text < 200 characters

**Example:**
```python
from docx_parser import is_section_header

for para in doc.paragraphs:
    if is_section_header(para):
        text = para.text
        print(f"Found section: {text}")
```

---

## Rebuilding API

### `rebuild_document(doc_data: Document, output_path: str) -> None`

Rebuilds a DOCX file from Document dataclass.

**Parameters:**
- `doc_data` (Document): Document to rebuild
- `output_path` (str): Path where DOCX will be written

**Raises:**
- `IOError`: If file can't be written

**Side Effects:**
- Creates/overwrites file at `output_path`

**Example:**
```python
from docx_parser import rebuild_document

rebuild_document(doc, "output.docx")
```

---

### `add_paragraph_to_document(docx_doc: DXMLDocument, para_data: Paragraph, style: Optional[str] = None) -> DXMLParagraph`

Adds a paragraph to a python-docx Document.

**Parameters:**
- `docx_doc`: python-docx Document to add to
- `para_data` (Paragraph): Paragraph data to add
- `style` (str, optional): Style name. Defaults to `para_data.style_name` or "Normal"

**Returns:**
- `DXMLParagraph`: The created python-docx Paragraph

**Behavior:**
- If specified style doesn't exist, falls back to "Normal"
- All text runs and formatting applied
- Paragraph formatting applied

**Example:**
```python
from docx import Document as DocxDocument
from docx_parser import add_paragraph_to_document, Paragraph, TextRun

docx_doc = DocxDocument()
para = Paragraph(
    runs=[TextRun(text="Hello")],
    formatting=ParagraphFormatting(),
)
add_paragraph_to_document(docx_doc, para)
docx_doc.save("output.docx")
```

---

### `apply_run_formatting(run: DXMLRun, formatting: RunFormatting) -> None`

Applies RunFormatting to a python-docx Run.

**Parameters:**
- `run`: python-docx Run object
- `formatting` (RunFormatting): Formatting to apply

**Side Effects:**
- Modifies `run` in-place

**Example:**
```python
from docx_parser import apply_run_formatting, RunFormatting

run = para.add_run("text")
fmt = RunFormatting(bold=True, font_size=12)
apply_run_formatting(run, fmt)
```

---

### `apply_paragraph_formatting(para: DXMLParagraph, formatting: ParagraphFormatting) -> None`

Applies ParagraphFormatting to a python-docx Paragraph.

**Parameters:**
- `para`: python-docx Paragraph
- `formatting` (ParagraphFormatting): Formatting to apply

**Side Effects:**
- Modifies paragraph in-place

---

### `apply_page_settings(section: DXMLSection, page_settings: PageSettings) -> None`

Applies page settings to a document section.

**Parameters:**
- `section`: python-docx Section
- `page_settings` (PageSettings): Width, height, margins, etc.

**Measurements:** All values in twips (1/20th of a point)

---

### `apply_line_numbering(section: DXMLSection, line_numbering: LineNumbering) -> None`

Applies line numbering to a section via XML manipulation.

**Parameters:**
- `section`: python-docx Section
- `line_numbering` (LineNumbering): Numbering settings

**Technical Notes:**
- Uses XML manipulation (python-docx doesn't fully support this)
- Creates/updates `w:lnNumType` element in section properties
- Safe to call multiple times (updates existing element)

---

### `apply_metadata(docx_doc: DXMLDocument, metadata: DocumentMetadata) -> None`

Applies all metadata to document (page settings, line numbering, etc.).

**Parameters:**
- `docx_doc`: python-docx Document
- `metadata` (DocumentMetadata): Metadata to apply

**Side Effects:**
- Modifies first section in document

---

## Translation API

### `translate_document(doc: Document, translator: TranslatorInterface, source_lang: str, target_lang: str) -> Document`

Translates a Document's text content while preserving formatting.

**Parameters:**
- `doc` (Document): Document to translate
- `translator` (TranslatorInterface): Translator implementation
- `source_lang` (str): Source language code (e.g., "de")
- `target_lang` (str): Target language code (e.g., "en")

**Returns:**
- `Document`: New translated document (original unchanged)

**Important:**
- Creates deep copy of document
- Automatically skips superscripts/subscripts (citations)
- Preserves all formatting and structure

**Example:**
```python
from docx_parser import translate_document, ManualTranslator

translator = ManualTranslator({"Hallo": "Hello", "Welt": "World"})
translated = translate_document(doc, translator, "de", "en")
```

---

### `extract_translate_rebuild(input_path: str, output_path: str, translator: TranslatorInterface, source_lang: str, target_lang: str) -> Document`

Complete pipeline: extract → translate → rebuild.

**Parameters:**
- `input_path` (str): Input DOCX file path
- `output_path` (str): Output DOCX file path
- `translator` (TranslatorInterface): Translator to use
- `source_lang` (str): Source language code
- `target_lang` (str): Target language code

**Returns:**
- `Document`: Translated document (also saved to `output_path`)

**Example:**
```python
from docx_parser import extract_translate_rebuild, CallbackTranslator

def my_api(text, src, tgt):
    return translation_service(text, src, tgt)

extract_translate_rebuild(
    "german.docx",
    "english.docx",
    CallbackTranslator(my_api),
    "de", "en"
)
```

---

## Translation Interfaces

### `TranslatorInterface` (Abstract Base Class)

Base class for all translator implementations.

**Methods:**

#### `translate(text: str, source_lang: str, target_lang: str) -> str` (abstract)

Translate text from source to target language.

**Parameters:**
- `text` (str): Text to translate
- `source_lang` (str): Source language code
- `target_lang` (str): Target language code

**Returns:**
- `str`: Translated text

#### `should_translate_run(run: TextRun) -> bool`

Determine if a text run should be translated.

**Default behavior:**
- Returns `False` if `run.formatting.is_superscript` or `is_subscript`
- Returns `False` if text is whitespace-only or empty
- Returns `True` otherwise

**Override this method to customize filtering:**
```python
class MyTranslator(TranslatorInterface):
    def should_translate_run(self, run):
        # Skip URLs
        if run.text.startswith("http"):
            return False
        # Use default behavior for everything else
        return super().should_translate_run(run)
```

---

### `CallbackTranslator`

Translator using a callback function.

**Constructor:**
```python
CallbackTranslator(translation_func: Callable[[str, str, str], str])
```

**Parameters:**
- `translation_func`: Function with signature `(text, source_lang, target_lang) -> str`

**Example:**
```python
from docx_parser import CallbackTranslator

def google_translate(text, src, tgt):
    from google.cloud import translate_v2
    client = translate_v2.Client()
    result = client.translate_text(text, source_language=src, target_language=tgt)
    return result['translatedText']

translator = CallbackTranslator(google_translate)
```

---

### `ManualTranslator`

Translator using a static dictionary.

**Constructor:**
```python
ManualTranslator(translations: Dict[str, str])
```

**Parameters:**
- `translations`: Dictionary mapping source text to target text

**Behavior:**
- Returns mapped translation if found
- Returns original text if not in dictionary

**Example:**
```python
from docx_parser import ManualTranslator

translator = ManualTranslator({
    "Hello": "Hola",
    "World": "Mundo",
})
```

---

### `NoOpTranslator`

No-operation translator (returns text unchanged). Useful for testing.

**Constructor:**
```python
NoOpTranslator()
```

**Example:**
```python
from docx_parser import NoOpTranslator

translator = NoOpTranslator()
translated = translate_document(doc, translator, "en", "en")
# Document unchanged (for testing workflow)
```

---

## Data Models

All data models are Python dataclasses using `@dataclass` decorator.

### `Document`

Top-level document container.

**Fields:**
- `metadata` (DocumentMetadata): Document settings
- `sections` (List[Section]): Document sections
- `preamble_paragraphs` (List[Paragraph]): Content before first section

**Example:**
```python
doc.metadata  # Page settings, line numbering
doc.sections[0].header  # First section header
doc.preamble_paragraphs[0]  # First preamble paragraph
```

---

### `Section`

Document section (header + body paragraphs).

**Fields:**
- `header` (Paragraph): Section header paragraph (bold)
- `paragraphs` (List[Paragraph]): Body paragraphs in section

---

### `Paragraph`

Paragraph container.

**Fields:**
- `runs` (List[TextRun]): Text runs with individual formatting
- `formatting` (ParagraphFormatting): Paragraph-level formatting
- `is_header` (bool): Whether this is a section header
- `style_name` (str): Original style name from DOCX

**Methods:**
- None (dataclass, use fields directly)

**Example:**
```python
para = doc.sections[0].header
full_text = "".join(run.text for run in para.runs)
```

---

### `TextRun`

Minimal text unit with consistent formatting.

**Fields:**
- `text` (str): Text content
- `formatting` (RunFormatting): Text formatting

---

### `RunFormatting`

Text-level formatting.

**Fields:**
- `bold` (bool, optional): Bold text (default: None)
- `italic` (bool, optional): Italic text (default: None)
- `underline` (bool, optional): Underlined text (default: None)
- `font_name` (str, optional): Font family (default: None)
- `font_size` (int, optional): Font size in points (default: None)
- `color` (str, optional): RGB color as hex "#RRGGBB" (default: None)
- `is_superscript` (bool): Superscript text (default: False)
- `is_subscript` (bool): Subscript text (default: False)

**Optional vs None:**
- `None` means "use default"
- Explicit `False` means "don't apply this"
- `True` means "apply this"

---

### `ParagraphFormatting`

Paragraph-level formatting.

**Fields:**
- `alignment` (str): "left", "center", "right", "justify", "distribute"
- `line_spacing` (float, optional): Line spacing multiplier
- `space_before` (int, optional): Space before in twips
- `space_after` (int, optional): Space after in twips
- `first_line_indent` (int, optional): First line indent in twips
- `left_indent` (int, optional): Left indent in twips
- `right_indent` (int, optional): Right indent in twips
- `keep_together` (bool): Keep on same page
- `keep_with_next` (bool): Keep with next paragraph
- `page_break_before` (bool): Page break before

---

### `DocumentMetadata`

Document-level metadata.

**Fields:**
- `line_numbering` (LineNumbering): Line numbering settings
- `page_settings` (PageSettings): Page layout
- `default_font` (str, optional): Default font name
- `default_font_size` (int, optional): Default font size in points

---

### `PageSettings`

Page layout configuration.

**Fields (all optional, all in twips):**
- `width`: Page width (default: 9144000 for letter)
- `height`: Page height (default: 12700000 for letter)
- `top_margin`: Top margin
- `bottom_margin`: Bottom margin
- `left_margin`: Left margin
- `right_margin`: Right margin
- `header_distance`: Distance from top to header
- `footer_distance`: Distance from bottom to footer

**Unit Conversions:**
- 1 point = 20 twips
- 1 inch = 1440 twips
- Letter: 8.5" × 11" = 12240 × 15840 twips

---

### `LineNumbering`

Line numbering configuration.

**Fields:**
- `enabled` (bool): Whether line numbering is active
- `start` (int): Starting line number (default: 1)
- `increment` (int): Count by increment (default: 1)
- `restart` (str): "continuous", "page", or "section" (default: "continuous")
- `distance` (int, optional): Distance from text in twips

---

## Utilities

### `hex_to_rgb_color(hex_color: str) -> Optional[RGBColor]`

Converts hex color string to python-docx RGBColor.

**Parameters:**
- `hex_color` (str): Hex color like "#FF0000" or "FF0000"

**Returns:**
- `RGBColor` if valid, `None` if invalid

**Example:**
```python
from docx_parser.utils import hex_to_rgb_color

color = hex_to_rgb_color("#FF0000")  # Red
```

---

### `color_to_hex(color_obj) -> str`

Converts python-docx color to hex string.

**Parameters:**
- `color_obj`: python-docx RGBColor or ColorFormat

**Returns:**
- `str`: Hex color like "#FF0000"

---

### `normalize_alignment(alignment) -> str`

Converts alignment enum to string.

**Parameters:**
- `alignment`: python-docx alignment enum

**Returns:**
- `str`: "left", "center", "right", "justify", or "distribute"

---

### Unit Conversion Functions

```python
from docx_parser.utils import (
    points_to_twips,
    twips_to_points,
    inches_to_twips,
    twips_to_inches,
)

twips = points_to_twips(12)  # 12 pt = 240 twips
points = twips_to_points(240)  # 240 twips = 12 pt

twips = inches_to_twips(1)  # 1 inch = 1440 twips
inches = twips_to_inches(1440)  # 1440 twips = 1 inch
```

---

## Error Handling

### Common Exceptions

#### `FileNotFoundError`
- Raised by `extract_document()` if DOCX file doesn't exist

**Handling:**
```python
from docx_parser import extract_document

try:
    doc = extract_document("nonexistent.docx")
except FileNotFoundError:
    print("File not found")
```

#### `KeyError` (Style not found)
- During rebuild, if DOCX uses custom styles not in target document
- **Automatic fallback:** Style falls back to "Normal" (safe to ignore)

#### `IOError` (File write error)
- Raised by `rebuild_document()` if output can't be written

**Handling:**
```python
from docx_parser import rebuild_document
import os

try:
    rebuild_document(doc, "output.docx")
except IOError as e:
    print(f"Failed to write: {e}")
```

### Safe Patterns

**Pattern 1: Safe extraction with fallback**
```python
from docx_parser import extract_document
import os

if os.path.exists(file_path):
    doc = extract_document(file_path)
else:
    print(f"File not found: {file_path}")
```

**Pattern 2: Safe translation**
```python
from docx_parser import translate_document, NoOpTranslator

try:
    translated = translate_document(doc, translator, src, tgt)
except Exception as e:
    print(f"Translation failed: {e}")
    # Fall back to original document
    translated = doc
```

**Pattern 3: Full pipeline with error handling**
```python
from docx_parser import extract_translate_rebuild
import os

try:
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"{input_file} not found")

    extract_translate_rebuild(
        input_file,
        output_file,
        translator,
        source_lang,
        target_lang
    )
    print(f"Success: {output_file}")
except Exception as e:
    print(f"Pipeline failed: {e}")
```

---

## Type Hints

All functions have complete type hints. Import types for type checking:

```python
from docx_parser import Document, Section, Paragraph, TextRun
from docx_parser.translator import TranslatorInterface

def my_processor(doc: Document) -> Document:
    """Process a document."""
    for section in doc.sections:
        for para in section.paragraphs:
            for run in para.runs:
                if run.formatting.bold:
                    print(run.text)
    return doc
```

---

## Version Information

- **Current Version:** 0.1.0
- **Python:** 3.8+
- **Dependencies:**
  - python-docx >= 0.8.11

---

## See Also

- [README.md](./README.md) - Quick start and overview
- [examples/](./examples/) - Working example scripts
- [CLAUDE.md](./CLAUDE.md) - AI assistant guidance
