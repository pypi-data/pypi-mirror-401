"""Data models for DOCX document structure using dataclasses."""

from dataclasses import dataclass, field
from typing import List, Optional, Union


@dataclass
class RunFormatting:
    """Formatting attributes for a text run."""

    bold: Optional[bool] = None
    italic: Optional[bool] = None
    underline: Optional[bool] = None
    font_name: Optional[str] = None
    font_size: Optional[int] = None  # In points
    color: Optional[str] = None  # RGB hex format (e.g., "#FF0000")
    is_superscript: bool = False
    is_subscript: bool = False


@dataclass
class TextRun:
    """A single run of text with consistent formatting."""

    text: str
    formatting: RunFormatting


@dataclass
class Hyperlink:
    """A hyperlink containing one or more text runs."""

    runs: List['TextRun'] = field(default_factory=list)
    url: Optional[str] = None  # External URL (e.g., "https://example.com")
    anchor: Optional[str] = None  # Internal anchor/fragment (e.g., "section1")

    @property
    def text(self) -> str:
        """Get the full visible text of the hyperlink."""
        return "".join(run.text for run in self.runs)


# Type alias for inline elements (runs and hyperlinks)
InlineElement = Union['TextRun', 'Hyperlink']


@dataclass
class ParagraphFormatting:
    """Paragraph-level formatting attributes."""

    alignment: Optional[str] = None  # "left", "center", "right", "justify"
    line_spacing: Optional[float] = None
    space_before: Optional[int] = None  # In points
    space_after: Optional[int] = None  # In points
    first_line_indent: Optional[int] = None  # In twips
    left_indent: Optional[int] = None  # In twips
    right_indent: Optional[int] = None  # In twips
    keep_together: bool = False
    keep_with_next: bool = False
    page_break_before: bool = False


@dataclass
class Paragraph:
    """A paragraph containing multiple inline elements (runs and hyperlinks)."""

    runs: List[InlineElement] = field(default_factory=list)
    formatting: ParagraphFormatting = field(default_factory=ParagraphFormatting)
    is_header: bool = False  # Section header (bold) marker
    style_name: Optional[str] = None  # e.g., "Heading 1", "Normal"
    empty_paragraph_font_size: Optional[int] = None  # Font size for empty paragraphs (in points)

    @property
    def text(self) -> str:
        """Get the full text content of the paragraph."""
        result = []
        for element in self.runs:
            if isinstance(element, TextRun):
                result.append(element.text)
            elif isinstance(element, Hyperlink):
                result.append(element.text)
        return "".join(result)


@dataclass
class Section:
    """A document section defined by a bold header."""

    header: Paragraph  # Bold header defining section
    paragraphs: List[Paragraph] = field(default_factory=list)  # Body


@dataclass
class LineNumbering:
    """Line numbering settings for document sections."""

    enabled: bool = False
    start: int = 1
    increment: int = 1
    restart: Optional[str] = None  # "continuous", "newPage", "newSection"
    distance: Optional[int] = None  # Distance from text in twips


@dataclass
class PageSettings:
    """Page layout settings."""

    width: Optional[int] = None  # In twips
    height: Optional[int] = None  # In twips
    top_margin: Optional[int] = None  # In twips
    bottom_margin: Optional[int] = None  # In twips
    left_margin: Optional[int] = None  # In twips
    right_margin: Optional[int] = None  # In twips
    header_distance: Optional[int] = None  # In twips
    footer_distance: Optional[int] = None  # In twips
    gutter: Optional[int] = None  # In twips
    mirror_margins: bool = False


@dataclass
class DocumentMetadata:
    """Document-level metadata and settings."""

    line_numbering: LineNumbering = field(default_factory=LineNumbering)
    page_settings: PageSettings = field(default_factory=PageSettings)
    default_font: Optional[str] = None
    default_font_size: Optional[int] = None


@dataclass
class Document:
    """Complete document structure with all content and formatting."""

    metadata: DocumentMetadata = field(default_factory=DocumentMetadata)
    sections: List[Section] = field(default_factory=list)
    preamble_paragraphs: List[Paragraph] = field(default_factory=list)

    @property
    def all_paragraphs(self) -> List[Paragraph]:
        """Get all paragraphs in document order (preamble + all sections)."""
        result = self.preamble_paragraphs.copy()
        for section in self.sections:
            result.append(section.header)
            result.extend(section.paragraphs)
        return result
