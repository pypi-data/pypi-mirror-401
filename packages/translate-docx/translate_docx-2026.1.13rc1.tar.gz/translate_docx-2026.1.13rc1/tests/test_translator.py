"""Tests for translation functionality."""

import os
import sys

import pytest

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from translate_docx.models import (
    Document,
    DocumentMetadata,
    LineNumbering,
    PageSettings,
    Paragraph,
    ParagraphFormatting,
    RunFormatting,
    Section,
    TextRun,
)
from translate_docx.translator import (
    CallbackTranslator,
    GoogleTranslatorWrapper,
    ManualTranslator,
    NoOpTranslator,
    TranslatorInterface,
    translate_document,
)


class TestTranslatorInterface:
    """Test the TranslatorInterface abstract class."""

    def test_should_translate_run_skips_superscript(self):
        """Superscripts should not be translated (citations)."""
        translator = NoOpTranslator()

        # Superscript run
        superscript_run = TextRun(text="1", formatting=RunFormatting(is_superscript=True))
        assert not translator.should_translate_run(superscript_run)

    def test_should_translate_run_skips_subscript(self):
        """Subscripts should not be translated."""
        translator = NoOpTranslator()

        subscript_run = TextRun(text="2", formatting=RunFormatting(is_subscript=True))
        assert not translator.should_translate_run(subscript_run)

    def test_should_translate_run_skips_whitespace(self):
        """Whitespace-only runs should not be translated."""
        translator = NoOpTranslator()

        whitespace_run = TextRun(text="   ", formatting=RunFormatting())
        assert not translator.should_translate_run(whitespace_run)

    def test_should_translate_run_skips_empty(self):
        """Empty runs should not be translated."""
        translator = NoOpTranslator()

        empty_run = TextRun(text="", formatting=RunFormatting())
        assert not translator.should_translate_run(empty_run)

    def test_should_translate_run_allows_normal_text(self):
        """Normal text runs should be translated."""
        translator = NoOpTranslator()

        normal_run = TextRun(text="Hello", formatting=RunFormatting())
        assert translator.should_translate_run(normal_run)

    def test_should_translate_run_allows_formatted_text(self):
        """Formatted text (bold, italic) should be translated."""
        translator = NoOpTranslator()

        bold_italic_run = TextRun(
            text="Important", formatting=RunFormatting(bold=True, italic=True)
        )
        assert translator.should_translate_run(bold_italic_run)


class TestCallbackTranslator:
    """Test CallbackTranslator implementation."""

    def test_callback_translator_calls_function(self):
        """CallbackTranslator should call the provided function."""
        translations = {
            "Hello": "Hallo",
            "World": "Welt",
        }

        def simple_translate(text, source, target):
            return translations.get(text, text)

        translator = CallbackTranslator(simple_translate)
        result = translator.translate("Hello", "en", "de")
        assert result == "Hallo"

    def test_callback_translator_receives_language_codes(self):
        """CallbackTranslator should pass language codes to function."""
        received_langs = {}

        def capture_langs(text, source, target):
            received_langs["source"] = source
            received_langs["target"] = target
            return text

        translator = CallbackTranslator(capture_langs)
        translator.translate("test", "en", "fr")

        assert received_langs["source"] == "en"
        assert received_langs["target"] == "fr"

    def test_callback_translator_with_lambda(self):
        """CallbackTranslator should work with lambda functions."""
        translator = CallbackTranslator(lambda text, src, tgt: text.upper())
        result = translator.translate("hello", "en", "de")
        assert result == "HELLO"


class TestManualTranslator:
    """Test ManualTranslator implementation."""

    def test_manual_translator_returns_translation(self):
        """ManualTranslator should return mapped translation."""
        translations = {
            "Hallo": "Hello",
            "Welt": "World",
        }
        translator = ManualTranslator(translations)

        result = translator.translate("Hallo", "de", "en")
        assert result == "Hello"

    def test_manual_translator_returns_original_if_not_found(self):
        """ManualTranslator should return original text if not in dictionary."""
        translations = {"Hallo": "Hello"}
        translator = ManualTranslator(translations)

        result = translator.translate("Goodbye", "de", "en")
        assert result == "Goodbye"

    def test_manual_translator_handles_empty_dict(self):
        """ManualTranslator should handle empty translation dictionary."""
        translator = ManualTranslator({})

        result = translator.translate("Any text", "en", "fr")
        assert result == "Any text"

    def test_manual_translator_case_sensitive(self):
        """ManualTranslator should be case-sensitive."""
        translations = {"Hello": "Hola"}
        translator = ManualTranslator(translations)

        # Different case, no translation
        result = translator.translate("hello", "en", "es")
        assert result == "hello"


class TestNoOpTranslator:
    """Test NoOpTranslator implementation."""

    def test_noop_translator_returns_unchanged(self):
        """NoOpTranslator should return text unchanged."""
        translator = NoOpTranslator()

        text = "Any text here"
        result = translator.translate(text, "en", "de")
        assert result == text

    def test_noop_translator_ignores_language_codes(self):
        """NoOpTranslator should ignore language codes."""
        translator = NoOpTranslator()

        result = translator.translate("test", "xx", "yy")
        assert result == "test"


class TestTranslateDocument:
    """Test translate_document function."""

    def test_translate_document_simple_paragraph(self):
        """Should translate simple document with single paragraph."""
        doc = Document(
            metadata=DocumentMetadata(
                line_numbering=LineNumbering(),
                page_settings=PageSettings(),
            ),
            sections=[],
            preamble_paragraphs=[
                Paragraph(
                    runs=[TextRun(text="Hallo", formatting=RunFormatting())],
                    formatting=ParagraphFormatting(),
                )
            ],
        )

        translations = {"Hallo": "Hello"}
        translator = ManualTranslator(translations, word_level=True)

        translated = translate_document(doc, translator, "de", "en")

        assert translated.preamble_paragraphs[0].runs[0].text == "Hello"
        # Original should be unchanged
        assert doc.preamble_paragraphs[0].runs[0].text == "Hallo"

    def test_translate_document_multiple_runs(self):
        """Should translate all runs in a paragraph."""
        doc = Document(
            metadata=DocumentMetadata(
                line_numbering=LineNumbering(),
                page_settings=PageSettings(),
            ),
            sections=[],
            preamble_paragraphs=[
                Paragraph(
                    runs=[
                        TextRun(text="Hallo", formatting=RunFormatting()),
                        TextRun(text=" ", formatting=RunFormatting()),
                        TextRun(text="Welt", formatting=RunFormatting()),
                    ],
                    formatting=ParagraphFormatting(),
                )
            ],
        )

        translations = {"Hallo": "Hello", "Welt": "World"}
        translator = ManualTranslator(translations, word_level=True)

        translated = translate_document(doc, translator, "de", "en")

        assert translated.preamble_paragraphs[0].runs[0].text == "Hello"
        assert translated.preamble_paragraphs[0].runs[2].text == "World"

    def test_translate_document_preserves_formatting(self):
        """Should preserve run formatting during translation."""
        doc = Document(
            metadata=DocumentMetadata(
                line_numbering=LineNumbering(),
                page_settings=PageSettings(),
            ),
            sections=[],
            preamble_paragraphs=[
                Paragraph(
                    runs=[
                        TextRun(
                            text="Hallo",
                            formatting=RunFormatting(
                                bold=True,
                                font_name="Arial",
                                font_size=12,
                            ),
                        ),
                    ],
                    formatting=ParagraphFormatting(),
                )
            ],
        )

        translations = {"Hallo": "Hello"}
        translator = ManualTranslator(translations, word_level=True)

        translated = translate_document(doc, translator, "de", "en")

        run = translated.preamble_paragraphs[0].runs[0]
        assert run.text == "Hello"
        assert run.formatting.bold is True
        assert run.formatting.font_name == "Arial"
        assert run.formatting.font_size == 12

    def test_translate_document_skips_superscripts(self):
        """Should skip superscript runs (citations)."""
        doc = Document(
            metadata=DocumentMetadata(
                line_numbering=LineNumbering(),
                page_settings=PageSettings(),
            ),
            sections=[],
            preamble_paragraphs=[
                Paragraph(
                    runs=[
                        TextRun(text="Text", formatting=RunFormatting()),
                        TextRun(
                            text="1",
                            formatting=RunFormatting(is_superscript=True),
                        ),
                    ],
                    formatting=ParagraphFormatting(),
                )
            ],
        )

        translations = {"Text": "Texto", "1": "SHOULD_NOT_TRANSLATE"}
        translator = ManualTranslator(translations, word_level=True)

        translated = translate_document(doc, translator, "es", "en")

        assert translated.preamble_paragraphs[0].runs[0].text == "Texto"
        # Superscript should remain unchanged
        assert translated.preamble_paragraphs[0].runs[1].text == "1"

    def test_translate_document_sections(self):
        """Should translate section headers and body paragraphs."""
        doc = Document(
            metadata=DocumentMetadata(
                line_numbering=LineNumbering(),
                page_settings=PageSettings(),
            ),
            sections=[
                Section(
                    header=Paragraph(
                        runs=[TextRun(text="Abschnitt", formatting=RunFormatting())],
                        formatting=ParagraphFormatting(),
                        is_header=True,
                    ),
                    paragraphs=[
                        Paragraph(
                            runs=[TextRun(text="Inhalt", formatting=RunFormatting())],
                            formatting=ParagraphFormatting(),
                        ),
                    ],
                )
            ],
            preamble_paragraphs=[],
        )

        translations = {"Abschnitt": "Section", "Inhalt": "Content"}
        translator = ManualTranslator(translations, word_level=True)

        translated = translate_document(doc, translator, "de", "en")

        assert translated.sections[0].header.runs[0].text == "Section"
        assert translated.sections[0].paragraphs[0].runs[0].text == "Content"

    def test_translate_document_preserves_structure(self):
        """Should preserve document structure during translation."""
        doc = Document(
            metadata=DocumentMetadata(
                line_numbering=LineNumbering(),
                page_settings=PageSettings(),
            ),
            sections=[
                Section(
                    header=Paragraph(
                        runs=[TextRun(text="Header", formatting=RunFormatting())],
                        formatting=ParagraphFormatting(),
                        is_header=True,
                    ),
                    paragraphs=[
                        Paragraph(
                            runs=[TextRun(text="Para1", formatting=RunFormatting())],
                            formatting=ParagraphFormatting(),
                        ),
                        Paragraph(
                            runs=[TextRun(text="Para2", formatting=RunFormatting())],
                            formatting=ParagraphFormatting(),
                        ),
                    ],
                ),
                Section(
                    header=Paragraph(
                        runs=[TextRun(text="Header2", formatting=RunFormatting())],
                        formatting=ParagraphFormatting(),
                        is_header=True,
                    ),
                    paragraphs=[
                        Paragraph(
                            runs=[TextRun(text="Para3", formatting=RunFormatting())],
                            formatting=ParagraphFormatting(),
                        ),
                    ],
                ),
            ],
            preamble_paragraphs=[],
        )

        translator = NoOpTranslator()
        translated = translate_document(doc, translator, "en", "fr")

        # Check structure is preserved
        assert len(translated.sections) == 2
        assert len(translated.sections[0].paragraphs) == 2
        assert len(translated.sections[1].paragraphs) == 1
        # Check preamble
        assert len(translated.preamble_paragraphs) == 0

    def test_translate_document_preserves_metadata(self):
        """Should preserve document metadata during translation."""
        metadata = DocumentMetadata(
            line_numbering=LineNumbering(
                enabled=True,
                start=1,
                increment=1,
            ),
            page_settings=PageSettings(
                width=9144000,
                height=12700000,
            ),
            default_font="Times New Roman",
            default_font_size=11,
        )

        doc = Document(
            metadata=metadata,
            sections=[],
            preamble_paragraphs=[
                Paragraph(
                    runs=[TextRun(text="Test", formatting=RunFormatting())],
                    formatting=ParagraphFormatting(),
                )
            ],
        )

        translator = NoOpTranslator()
        translated = translate_document(doc, translator, "en", "de")

        assert translated.metadata.line_numbering.enabled is True
        assert translated.metadata.line_numbering.start == 1
        assert translated.metadata.page_settings.width == 9144000
        assert translated.metadata.default_font == "Times New Roman"
        assert translated.metadata.default_font_size == 11

    def test_translate_document_does_not_modify_original(self):
        """Translation should not modify the original document."""
        original_text = "Original"
        doc = Document(
            metadata=DocumentMetadata(
                line_numbering=LineNumbering(),
                page_settings=PageSettings(),
            ),
            sections=[],
            preamble_paragraphs=[
                Paragraph(
                    runs=[TextRun(text=original_text, formatting=RunFormatting())],
                    formatting=ParagraphFormatting(),
                )
            ],
        )

        translations = {"Original": "Modified"}
        translator = ManualTranslator(translations, word_level=True)

        translated = translate_document(doc, translator, "en", "de")

        # Original should be unchanged
        assert doc.preamble_paragraphs[0].runs[0].text == original_text
        # Translated should be changed
        assert translated.preamble_paragraphs[0].runs[0].text == "Modified"

    def test_translate_document_complex(self):
        """Test translation of complex document with all features."""
        doc = Document(
            metadata=DocumentMetadata(
                line_numbering=LineNumbering(enabled=True),
                page_settings=PageSettings(),
            ),
            preamble_paragraphs=[
                Paragraph(
                    runs=[
                        TextRun(text="Prolog", formatting=RunFormatting()),
                    ],
                    formatting=ParagraphFormatting(),
                )
            ],
            sections=[
                Section(
                    header=Paragraph(
                        runs=[
                            TextRun(text="Teil Eins", formatting=RunFormatting(bold=True)),
                        ],
                        formatting=ParagraphFormatting(),
                        is_header=True,
                    ),
                    paragraphs=[
                        Paragraph(
                            runs=[
                                TextRun(text="Absatz", formatting=RunFormatting()),
                                TextRun(text=" ", formatting=RunFormatting()),
                                TextRun(text="mit", formatting=RunFormatting()),
                                TextRun(
                                    text="1",
                                    formatting=RunFormatting(is_superscript=True),
                                ),
                            ],
                            formatting=ParagraphFormatting(),
                        ),
                    ],
                ),
            ],
        )

        translations = {
            "Prolog": "Prologue",
            "Teil Eins": "Part One",
            "Absatz": "Paragraph",
            "mit": "with",
        }
        translator = ManualTranslator(translations, word_level=True)

        translated = translate_document(doc, translator, "de", "en")

        # Check preamble
        assert translated.preamble_paragraphs[0].runs[0].text == "Prologue"

        # Check section header
        assert translated.sections[0].header.runs[0].text == "Part One"

        # Check body with mixed content
        assert translated.sections[0].paragraphs[0].runs[0].text == "Paragraph"
        assert translated.sections[0].paragraphs[0].runs[1].text == " "  # Whitespace run
        assert translated.sections[0].paragraphs[0].runs[2].text == "with"
        # Superscript should not be translated
        assert translated.sections[0].paragraphs[0].runs[3].text == "1"
        assert translated.sections[0].paragraphs[0].runs[3].formatting.is_superscript

    def test_translate_document_whitespace_runs_skipped(self):
        """Should skip whitespace-only runs from translation."""
        doc = Document(
            metadata=DocumentMetadata(
                line_numbering=LineNumbering(),
                page_settings=PageSettings(),
            ),
            sections=[],
            preamble_paragraphs=[
                Paragraph(
                    runs=[
                        TextRun(text="Word1", formatting=RunFormatting()),
                        TextRun(text="   ", formatting=RunFormatting()),
                        TextRun(text="Word2", formatting=RunFormatting()),
                    ],
                    formatting=ParagraphFormatting(),
                )
            ],
        )

        translations = {
            "Word1": "TRANSLATED1",
            "   ": "SHOULD_NOT_TRANSLATE",
            "Word2": "TRANSLATED2",
        }
        translator = ManualTranslator(translations, word_level=True)

        translated = translate_document(doc, translator, "en", "de")

        # Whitespace run should remain unchanged
        assert translated.preamble_paragraphs[0].runs[1].text == "   "
        assert translated.preamble_paragraphs[0].runs[0].text == "TRANSLATED1"
        assert translated.preamble_paragraphs[0].runs[2].text == "TRANSLATED2"


class MarkerStrippingTranslator(TranslatorInterface):
    """Translator that simulates Google Translate stripping HTML-like markers.

    Google Translate and similar services often remove or corrupt HTML-like
    syntax such as <RUN0>, </RUN1>, etc. This translator simulates that behavior
    to test that our translation pipeline handles it correctly.
    """

    import re

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Strip all RUN markers from text, simulating Google Translate behavior."""
        import re

        # Remove all RUN markers (both opening and closing)
        result = re.sub(r'<RUN\d+>', '', text)
        result = re.sub(r'</RUN\d+>', '', result)
        return result


class TestRunMarkerProtection:
    """Test that RUN markers are properly protected during translation.

    This tests for a bug where RUN markers like <RUN0>, </RUN1> were not being
    protected before translation, causing external translators (like Google
    Translate) to strip or corrupt them, resulting in truncated output.
    """

    def test_translation_preserves_text_when_markers_stripped(self):
        """Text should be fully preserved even if translator strips RUN markers.

        This is the key regression test for the truncation bug where paragraphs
        were being cut off because RUN markers weren't protected.
        """
        # Create a document with a long paragraph containing multiple runs
        doc = Document(
            metadata=DocumentMetadata(
                line_numbering=LineNumbering(),
                page_settings=PageSettings(),
            ),
            sections=[],
            preamble_paragraphs=[
                Paragraph(
                    runs=[
                        TextRun(
                            text="First part of the paragraph with some content. ",
                            formatting=RunFormatting(),
                        ),
                        TextRun(
                            text="Second part that should not be lost. ",
                            formatting=RunFormatting(bold=True),
                        ),
                        TextRun(
                            text="Third part with more important content. ",
                            formatting=RunFormatting(),
                        ),
                        TextRun(
                            text="Fourth and final part of this test paragraph.",
                            formatting=RunFormatting(italic=True),
                        ),
                    ],
                    formatting=ParagraphFormatting(),
                )
            ],
        )

        original_text = doc.preamble_paragraphs[0].text
        original_length = len(original_text)

        # Use the marker-stripping translator that simulates Google Translate
        translator = MarkerStrippingTranslator()
        translated = translate_document(doc, translator, "en", "de", show_progress=False)

        translated_text = translated.preamble_paragraphs[0].text
        translated_length = len(translated_text)

        # The translated text should have the same content (since this translator
        # doesn't actually change the text, just strips markers)
        assert translated_length == original_length, (
            f"Text was truncated! Original: {original_length} chars, "
            f"Translated: {translated_length} chars. "
            f"Missing {original_length - translated_length} chars."
        )
        assert translated_text == original_text, (
            f"Text content differs!\n"
            f"Original: {original_text}\n"
            f"Translated: {translated_text}"
        )

    def test_translation_preserves_all_runs_when_markers_stripped(self):
        """All runs should be preserved even if translator strips RUN markers."""
        doc = Document(
            metadata=DocumentMetadata(
                line_numbering=LineNumbering(),
                page_settings=PageSettings(),
            ),
            sections=[],
            preamble_paragraphs=[
                Paragraph(
                    runs=[
                        TextRun(text="Run1", formatting=RunFormatting()),
                        TextRun(text=" ", formatting=RunFormatting()),
                        TextRun(text="Run2", formatting=RunFormatting()),
                        TextRun(text=" ", formatting=RunFormatting()),
                        TextRun(text="Run3", formatting=RunFormatting()),
                    ],
                    formatting=ParagraphFormatting(),
                )
            ],
        )

        translator = MarkerStrippingTranslator()
        translated = translate_document(doc, translator, "en", "de", show_progress=False)

        # All runs should be present
        assert len(translated.preamble_paragraphs[0].runs) >= 1, "No runs in output!"
        assert translated.preamble_paragraphs[0].text == "Run1 Run2 Run3", (
            f"Expected 'Run1 Run2 Run3', got '{translated.preamble_paragraphs[0].text}'"
        )

    def test_long_paragraph_not_truncated(self):
        """Long paragraphs should not be truncated during translation.

        This specifically tests the reported bug where a paragraph starting with
        "'In de stad, bij het theater, op zoek naar werk.'" was cut off after
        "Payne drinkt en feest met vrienden, waaronder Spottiswoode Aitken."
        """
        # Create a very long paragraph similar to the one that was truncated
        long_text_parts = [
            "'In de stad, bij het theater, op zoek naar werk.' ",
            "'Payne mag auditie doen' en wordt door Spottiswoode Aitken aangenomen. ",
            "'Payne's godsdienstige moeder vindt de roeping van haar zoon vreselijk.' ",
            "Zij krijgt hier per brief bericht van. ",
            "Payne drinkt en feest met vrienden, waaronder Spottiswoode Aitken. ",
            "Griffith snijdt nu heen en weer tussen de woonkamer. ",
            "Deze sequentie wordt gekenmerkt door akoestische koppeling. ",
            "Moeder wordt onrustig terwijl Lilian de situatie probeert te redden. ",
            "'Wat een walgelijke taal' zegt moeder. ",
            "De dronken vrienden vertrekken. ",
        ]

        runs = [TextRun(text=part, formatting=RunFormatting()) for part in long_text_parts]

        doc = Document(
            metadata=DocumentMetadata(
                line_numbering=LineNumbering(),
                page_settings=PageSettings(),
            ),
            sections=[],
            preamble_paragraphs=[
                Paragraph(runs=runs, formatting=ParagraphFormatting())
            ],
        )

        original_text = doc.preamble_paragraphs[0].text

        translator = MarkerStrippingTranslator()
        translated = translate_document(doc, translator, "nl", "en", show_progress=False)

        translated_text = translated.preamble_paragraphs[0].text

        # The key assertion: no content should be lost
        assert len(translated_text) == len(original_text), (
            f"Long paragraph was truncated! "
            f"Original: {len(original_text)} chars, "
            f"Translated: {len(translated_text)} chars"
        )

        # Also verify the text after the cutoff point is present
        assert "Griffith snijdt" in translated_text, (
            "Text after the cutoff point is missing!"
        )
        assert "De dronken vrienden vertrekken" in translated_text, (
            "End of paragraph is missing!"
        )


class TestGoogleTranslateGarbledOutput:
    """Test that Google Translate doesn't produce garbled output.

    These tests verify that the spacing around protected RUN markers
    prevents Google Translate from:
    1. Concatenating markers with surrounding text
    2. Producing garbled translations
    3. Truncating content
    """

    def test_markers_are_protected(self):
        """RUN markers should be replaced with safe placeholders."""
        from translate_docx.translator import _protect_run_markers

        # Create text with RUN markers
        text = "<RUN0>Hello world</RUN0><RUN1>Test</RUN1>"

        protected, backup = _protect_run_markers(text)

        # Check that markers are replaced with safe placeholders
        assert "##RUN_OPEN_0##" in protected, "RUN_OPEN_0 should be protected"
        assert "##RUN_CLOSE_0##" in protected, "RUN_CLOSE_0 should be protected"
        assert "##RUN_OPEN_1##" in protected, "RUN_OPEN_1 should be protected"
        assert "##RUN_CLOSE_1##" in protected, "RUN_CLOSE_1 should be protected"

        # Original markers should not be present
        assert "<RUN0>" not in protected
        assert "</RUN0>" not in protected

    def test_markers_restored_correctly(self):
        """Protected markers should be restored to original RUN markers."""
        from translate_docx.translator import _protect_run_markers, _restore_run_markers

        original = "<RUN0>Hello world</RUN0><RUN1>Test</RUN1>"

        protected, backup = _protect_run_markers(original)
        restored = _restore_run_markers(protected, backup)

        # The restored text should match the original exactly
        assert restored == original, (
            f"Restored text should match original.\n"
            f"Original: {original}\n"
            f"Restored: {restored}"
        )

    def test_translation_with_protected_markers_preserves_content(self):
        """Translation with protected markers should preserve all content."""
        # Create a document with multiple runs
        doc = Document(
            metadata=DocumentMetadata(
                line_numbering=LineNumbering(),
                page_settings=PageSettings(),
            ),
            sections=[],
            preamble_paragraphs=[
                Paragraph(
                    runs=[
                        TextRun(text="First run ", formatting=RunFormatting()),
                        TextRun(text="Second run ", formatting=RunFormatting()),
                        TextRun(text="Third run", formatting=RunFormatting()),
                    ],
                    formatting=ParagraphFormatting(),
                )
            ],
        )

        # Use marker-stripping translator (simulates Google removing unprotected markers)
        translator = MarkerStrippingTranslator()
        translated = translate_document(doc, translator, "en", "en", show_progress=False)

        # All content should be preserved
        assert translated.preamble_paragraphs[0].text == "First run Second run Third run"

    def test_long_paragraph_with_cross_cuts_preserved(self):
        """Long paragraphs with cross-cut timestamps should not be truncated.

        This specifically tests the reported bug where content after cross-cut
        timestamps was being lost or garbled by Google Translate.
        """
        # Create a paragraph similar to the failing one with cross-cut timestamps
        long_text = (
            "Griffith cuts back and forth between the living room, where the party "
            "is going on, and the bedroom, where Lilian and mother are worriedly "
            "listening to what is happening in the living room (cross-cuts 00:06:01, "
            "00:06:09, 00:06:13, 00:06:16, 00:06:22, 00:06:25, 00:06:36, 00:06:39, "
            "00:06:48, 00:06:52, 00:06:52, 00:06:57, 00:07:05, 00:07:07, 00:07:13, "
            "00:07:16, 00:07:22. This sequence is characterized by acoustic coupling. "
            "Lilian and mother react to what they hear happening in the adjacent room. "
            "Mother becomes restless while Lilian tries to save the situation."
        )

        # Split into multiple runs to simulate the real document structure
        runs = [
            TextRun(text=long_text[:200], formatting=RunFormatting()),
            TextRun(text=long_text[200:400], formatting=RunFormatting()),
            TextRun(text=long_text[400:], formatting=RunFormatting()),
        ]

        doc = Document(
            metadata=DocumentMetadata(
                line_numbering=LineNumbering(),
                page_settings=PageSettings(),
            ),
            sections=[],
            preamble_paragraphs=[
                Paragraph(runs=runs, formatting=ParagraphFormatting())
            ],
        )

        translator = MarkerStrippingTranslator()
        translated = translate_document(doc, translator, "en", "en", show_progress=False)

        translated_text = translated.preamble_paragraphs[0].text

        # Key assertions: all important content should be present
        assert "acoustic coupling" in translated_text, (
            "Text about 'acoustic coupling' should not be lost"
        )
        assert "adjacent room" in translated_text, (
            "Text about 'adjacent room' should not be lost"
        )
        assert "Mother becomes restless" in translated_text, (
            "Text about 'Mother becomes restless' should not be lost"
        )

        # Check that total length is preserved
        assert len(translated_text) == len(long_text), (
            f"Content length should be preserved. "
            f"Original: {len(long_text)}, Translated: {len(translated_text)}"
        )

    def test_adjacent_markers_dont_create_double_spaces(self):
        """Adjacent RUN markers should not create double spaces."""
        from translate_docx.translator import _protect_run_markers, _restore_run_markers

        # Text with adjacent RUN markers (common pattern)
        text = "<RUN0>Text one</RUN0><RUN1>Text two</RUN1><RUN2>Text three</RUN2>"

        protected, backup = _protect_run_markers(text)
        restored = _restore_run_markers(protected, backup)

        # Should not have double spaces in restored text
        assert "  " not in restored, (
            f"Restored text should not have double spaces.\n"
            f"Restored: {restored}"
        )

    def test_real_dutch_paragraph_structure(self):
        """Test with structure similar to the actual failing Dutch paragraph.

        This tests the exact pattern that was causing the issue:
        - Multiple runs with different formatting
        - Long cross-cut sequence with timestamps
        - Critical sentence after timestamps that was being lost
        """
        runs = [
            # Run 0: Long intro (563 chars in original)
            TextRun(
                text=(
                    "'In de stad, bij het theater, op zoek naar werk.' "
                    "'Payne mag auditie doen' en wordt door Spottiswoode Aitken "
                    "aangenomen. 'Payne's godsdienstige moeder vindt de roeping "
                    "van haar zoon vreselijk.' Zij krijgt hier per brief bericht "
                    "van en leest de brief samen met Lilian: 'Hij is acteur.' "
                    "'Moeder en Lillian zoeken Payne in zijn verblijf in de stad op' "
                    "en moeder is verheugd dat zij daar de bijbel vindt liggen. "
                    "Maar als in zijn woonkamer een luidruchtig gezelschap binnenkomt "
                    "vluchten zij naar de belendende slaapkamer. "
                    "Payne drinkt en feest met vrienden, waaronder "
                ),
                formatting=RunFormatting(),
            ),
            # Run 1: Name with special formatting (19 chars in original)
            TextRun(text="Spottiswoode Aitken", formatting=RunFormatting(bold=True)),
            # Run 2: Cross-cuts and CRITICAL sentence (488 chars in original)
            TextRun(
                text=(
                    ". Griffith snijdt nu heen en weer tussen de woonkamer, "
                    "waar gefeest wordt en de slaapkamer waar Lilian en moeder "
                    "bezorgd het gebeuren in de woonkamer beluisteren (cross-cut's "
                    "00:06:01, 00:06:09, 00:06:13, 00:06:16, 00:06:22, 00:06:25, "
                    "00:06:36, 00:06:39, 00:06:48, 00:06:52, 00:06:52, 00:06:57, "
                    "00:07:05, 00:07:07, 00:07:13, 00:07:16, 00:07:22. "
                    "Deze sequentie wordt gekenmerkt door akoestische koppeling. "
                    "Lilian en moeder reageren op wat zij in de belendende kamer "
                    "horen gebeuren. Moeder "
                ),
                formatting=RunFormatting(),
            ),
            # Run 3: Rest of paragraph (817 chars in original)
            TextRun(
                text=(
                    "wordt onrustig terwijl Lilian de situatie probeert te redden. "
                    "'Wat een walgelijke taal' zegt moeder, terwijl Payne en zijn "
                    "vrienden niet bijkomen van het lachen."
                ),
                formatting=RunFormatting(),
            ),
        ]

        doc = Document(
            metadata=DocumentMetadata(
                line_numbering=LineNumbering(),
                page_settings=PageSettings(),
            ),
            sections=[],
            preamble_paragraphs=[
                Paragraph(runs=runs, formatting=ParagraphFormatting())
            ],
        )

        translator = MarkerStrippingTranslator()
        translated = translate_document(doc, translator, "nl", "en", show_progress=False)

        translated_text = translated.preamble_paragraphs[0].text

        # The CRITICAL assertion: this sentence was being completely lost
        assert "Deze sequentie wordt gekenmerkt door akoestische koppeling" in translated_text, (
            "The critical sentence about acoustic coupling must not be lost!"
        )

        assert "Lilian en moeder reageren op wat zij in de belendende kamer horen gebeuren" in translated_text, (
            "The sentence about Lilian and mother reacting must not be lost!"
        )

        # Verify all runs are present in output
        assert "Spottiswoode Aitken" in translated_text
        assert "cross-cut" in translated_text
        assert "00:07:22" in translated_text


class TestParagraphChunking:
    """Test automatic paragraph chunking for long content.

    These tests verify that very long paragraphs are automatically split
    into smaller chunks to prevent Google Translate from truncating or
    garbling the output.
    """

    def test_short_paragraph_not_chunked(self):
        """Short paragraphs should not be chunked."""
        short_text = "This is a short paragraph. It has a few sentences. But it's not long."

        doc = Document(
            metadata=DocumentMetadata(
                line_numbering=LineNumbering(),
                page_settings=PageSettings(),
            ),
            sections=[],
            preamble_paragraphs=[
                Paragraph(
                    runs=[TextRun(text=short_text, formatting=RunFormatting())],
                    formatting=ParagraphFormatting(),
                )
            ],
        )

        translator = NoOpTranslator()
        translated = translate_document(doc, translator, "en", "en", show_progress=False)

        # Should still have one run (not chunked)
        assert len(translated.preamble_paragraphs[0].runs) == 1
        assert translated.preamble_paragraphs[0].text == short_text

    def test_long_paragraph_gets_chunked(self):
        """Long paragraphs (>1500 chars) should be automatically chunked."""
        # Create a paragraph longer than 1500 chars
        long_text = ". ".join([f"This is sentence number {i}" for i in range(100)])

        doc = Document(
            metadata=DocumentMetadata(
                line_numbering=LineNumbering(),
                page_settings=PageSettings(),
            ),
            sections=[],
            preamble_paragraphs=[
                Paragraph(
                    runs=[TextRun(text=long_text, formatting=RunFormatting())],
                    formatting=ParagraphFormatting(),
                )
            ],
        )

        translator = NoOpTranslator()
        translated = translate_document(doc, translator, "en", "en", show_progress=False)

        # Content should be preserved
        assert translated.preamble_paragraphs[0].text == long_text
        # Should have multiple runs (chunked and reassembled)
        assert len(translated.preamble_paragraphs[0].runs) >= 1

    def test_chunking_preserves_all_content(self):
        """Chunked translation should preserve all content without loss."""
        # Create text with identifiable markers to verify nothing is lost
        sections = [
            "SECTION_A: " + "Word " * 200 + ".",
            "SECTION_B: " + "Text " * 200 + ".",
            "SECTION_C: " + "Data " * 200 + ".",
        ]
        long_text = " ".join(sections)

        doc = Document(
            metadata=DocumentMetadata(
                line_numbering=LineNumbering(),
                page_settings=PageSettings(),
            ),
            sections=[],
            preamble_paragraphs=[
                Paragraph(
                    runs=[TextRun(text=long_text, formatting=RunFormatting())],
                    formatting=ParagraphFormatting(),
                )
            ],
        )

        translator = NoOpTranslator()
        translated = translate_document(doc, translator, "en", "en", show_progress=False)

        translated_text = translated.preamble_paragraphs[0].text

        # All sections should be present
        assert "SECTION_A:" in translated_text
        assert "SECTION_B:" in translated_text
        assert "SECTION_C:" in translated_text

        # Length should match
        assert len(translated_text) == len(long_text)

    def test_chunking_preserves_formatting_across_chunks(self):
        """Formatting should be preserved when chunks are split."""
        # Create runs with different formatting that will be chunked
        runs = [
            TextRun(text="Normal text. " * 100, formatting=RunFormatting()),
            TextRun(text="Bold text. " * 100, formatting=RunFormatting(bold=True)),
            TextRun(text="Italic text. " * 100, formatting=RunFormatting(italic=True)),
        ]

        doc = Document(
            metadata=DocumentMetadata(
                line_numbering=LineNumbering(),
                page_settings=PageSettings(),
            ),
            sections=[],
            preamble_paragraphs=[
                Paragraph(runs=runs, formatting=ParagraphFormatting())
            ],
        )

        translator = NoOpTranslator()
        translated = translate_document(doc, translator, "en", "en", show_progress=False)

        # Check that we have runs with the expected formatting
        has_normal = any(not r.formatting.bold and not r.formatting.italic
                        for r in translated.preamble_paragraphs[0].runs)
        has_bold = any(r.formatting.bold for r in translated.preamble_paragraphs[0].runs)
        has_italic = any(r.formatting.italic for r in translated.preamble_paragraphs[0].runs)

        assert has_normal, "Should have normal (unformatted) runs"
        assert has_bold, "Should have bold runs"
        assert has_italic, "Should have italic runs"

    def test_griffith_paragraph_chunked_correctly(self):
        """Test that the actual failing Griffith paragraph gets chunked properly.

        This is a real-world test with the 1887-character paragraph that was
        causing Google Translate to truncate and garble output.
        """
        # This is the exact structure from the griffith document
        runs = [
            TextRun(
                text=(
                    "'In de stad, bij het theater, op zoek naar werk.' "
                    "'Payne mag auditie doen' en wordt door Spottiswoode Aitken "
                    "aangenomen. 'Payne's godsdienstige moeder vindt de roeping "
                    "van haar zoon vreselijk.' Zij krijgt hier per brief bericht "
                    "van en leest de brief samen met Lilian: 'Hij is acteur.' "
                    "'Moeder en Lillian zoeken Payne in zijn verblijf in de stad op' "
                    "en moeder is verheugd dat zij daar de bijbel vindt liggen. "
                    "Maar als in zijn woonkamer een luidruchtig gezelschap binnenkomt "
                    "vluchten zij naar de belendende slaapkamer. "
                    "Payne drinkt en feest met vrienden, waaronder "
                ),
                formatting=RunFormatting(),
            ),
            TextRun(text="Spottiswoode Aitken", formatting=RunFormatting(bold=True)),
            TextRun(
                text=(
                    ". Griffith snijdt nu heen en weer tussen de woonkamer, "
                    "waar gefeest wordt en de slaapkamer waar Lilian en moeder "
                    "bezorgd het gebeuren in de woonkamer beluisteren (cross-cut's "
                    "00:06:01, 00:06:09, 00:06:13, 00:06:16, 00:06:22, 00:06:25, "
                    "00:06:36, 00:06:39, 00:06:48, 00:06:52, 00:06:52, 00:06:57, "
                    "00:07:05, 00:07:07, 00:07:13, 00:07:16, 00:07:22. "
                    "Deze sequentie wordt gekenmerkt door akoestische koppeling. "
                    "Lilian en moeder reageren op wat zij in de belendende kamer "
                    "horen gebeuren. Moeder "
                ),
                formatting=RunFormatting(),
            ),
            TextRun(
                text=(
                    "wordt onrustig terwijl Lilian de situatie probeert te redden. "
                    "'Wat een walgelijke taal' zegt moeder, terwijl Payne en zijn "
                    "vrienden niet bijkomen van het lachen. Lillian zegt hierop: "
                    "'Zij zijn alleen maar hun rol aan het repeteren.' Maar dan "
                    "komen er ook dames, die Payne kust. Moeder krimpt steeds meer "
                    "ineen, terwijl Lilian haar troost. Er wordt steeds tussen de "
                    "slaapkamer en de woonkamer in cross-cut heen en weer gesneden. "
                    "De dronken vrienden vertrekken en Lillian en moeder komen uit "
                    "de slaapkamer en treffen, in medium close, Payne stomdronken "
                    "in een stoel aan. Lillian streelt hem liefhebbend terwijl "
                    "moeder haar afschuw toont. 'De volgende morgen: zijn belofte.' "
                    "Moeder wijst Payne op de bijbel en Lilian geeft hem een "
                    "bloemetje (00:08:42) dat haar liefde voor hem symboliseert. "
                    "Lilian en moeder vertrekken. "
                ),
                formatting=RunFormatting(),
            ),
        ]

        doc = Document(
            metadata=DocumentMetadata(
                line_numbering=LineNumbering(),
                page_settings=PageSettings(),
            ),
            sections=[],
            preamble_paragraphs=[
                Paragraph(runs=runs, formatting=ParagraphFormatting())
            ],
        )

        original_text = doc.preamble_paragraphs[0].text
        original_length = len(original_text)

        translator = NoOpTranslator()
        translated = translate_document(doc, translator, "nl", "en", show_progress=False)

        translated_text = translated.preamble_paragraphs[0].text

        # CRITICAL: The sentence that was being lost should be present
        assert "Deze sequentie wordt gekenmerkt door akoestische koppeling" in translated_text, (
            "The critical sentence about 'acoustic coupling' must be preserved!"
        )

        assert "Lilian en moeder reageren op wat zij in de belendende kamer horen gebeuren" in translated_text, (
            "The sentence about reactions must be preserved!"
        )

        # All content should be preserved
        assert len(translated_text) == original_length, (
            f"Content length must be preserved. "
            f"Original: {original_length}, Translated: {len(translated_text)}"
        )


class TestBypassMarkerProtection:
    """Test that markers with [[ marker: ... ]] are protected during translation."""

    def test_validate_marker_name(self):
        """Marker names should only allow alphanumeric characters."""
        from translate_docx.translator import _validate_marker_name

        # Valid markers - should not raise
        _validate_marker_name('tc')
        _validate_marker_name('note123')
        _validate_marker_name('REF')

        # Invalid markers - should raise ValueError
        with pytest.raises(ValueError, match="alphanumeric"):
            _validate_marker_name('tc!')

        with pytest.raises(ValueError, match="alphanumeric"):
            _validate_marker_name('note-ref')

        with pytest.raises(ValueError, match="alphanumeric"):
            _validate_marker_name('ref@home')

    def test_compile_marker_patterns(self):
        """Should compile regex patterns for each marker type."""
        from translate_docx.translator import _compile_marker_patterns

        patterns = _compile_marker_patterns(['tc', 'note', 'ref'])

        assert 'tc' in patterns
        assert 'note' in patterns
        assert 'ref' in patterns
        assert len(patterns) == 3

    def test_compile_marker_patterns_deduplicates(self):
        """Should deduplicate marker names (case-insensitive)."""
        from translate_docx.translator import _compile_marker_patterns

        patterns = _compile_marker_patterns(['tc', 'TC', 'Tc', 'note'])

        # Only lowercase 'tc' and 'note' should be in result
        assert 'tc' in patterns
        assert 'note' in patterns
        assert len(patterns) == 2

    def test_extract_markers_single_type(self):
        """Single marker type should be extracted."""
        from translate_docx.translator import _compile_marker_patterns, _extract_markers

        patterns = _compile_marker_patterns(['tc'])
        text = "Cross-cuts [[ tc: 00:06:01, 00:06:09, 00:06:13 ]] in the film."
        result, extracted = _extract_markers(text, patterns)

        assert 'tc' in extracted
        assert len(extracted['tc']) == 1
        assert "{TC0}" in result
        assert "[[ tc:" not in result
        assert extracted['tc'][0]['content'] == "00:06:01, 00:06:09, 00:06:13"
        assert extracted['tc'][0]['placeholder'] == "{TC0}"

    def test_extract_markers_multiple_instances_same_type(self):
        """Multiple instances of same marker type should all be extracted."""
        from translate_docx.translator import _compile_marker_patterns, _extract_markers

        patterns = _compile_marker_patterns(['tc'])
        text = "Scene 1 [[ tc: 00:01:00 ]] and Scene 2 [[ tc: 00:02:00 ]]."
        result, extracted = _extract_markers(text, patterns)

        assert 'tc' in extracted
        assert len(extracted['tc']) == 2
        assert "{TC0}" in result
        assert "{TC1}" in result
        assert extracted['tc'][0]['content'] == "00:01:00"
        assert extracted['tc'][1]['content'] == "00:02:00"

    def test_extract_markers_multiple_types(self):
        """Multiple marker types should all be extracted."""
        from translate_docx.translator import _compile_marker_patterns, _extract_markers

        patterns = _compile_marker_patterns(['tc', 'note', 'ref'])
        text = "Text [[ tc: 00:01:00 ]] and [[ note: important ]] and [[ ref: Smith2020 ]]."
        result, extracted = _extract_markers(text, patterns)

        assert 'tc' in extracted
        assert 'note' in extracted
        assert 'ref' in extracted
        assert "{TC0}" in result
        assert "{NOTE0}" in result
        assert "{REF0}" in result

    def test_restore_markers(self):
        """Marker placeholders should be restored with original content."""
        from translate_docx.translator import _compile_marker_patterns, _extract_markers, _restore_markers

        patterns = _compile_marker_patterns(['tc'])
        original = "Cross-cuts [[ tc: 00:06:01, 00:06:09 ]] in the film."
        text_with_placeholders, extracted = _extract_markers(original, patterns)

        restored = _restore_markers(text_with_placeholders, extracted)

        # The [[ tc: ]] wrapper should be PRESERVED to match input document
        assert restored == original
        assert "[[ tc:" in restored

    def test_markers_survive_translation_pipeline(self):
        """Markers should be preserved through full translation pipeline."""
        # Text with timecode markers
        text_with_marker = (
            "Griffith snijdt heen en weer (cross-cut's "
            "[[ tc: 00:06:01, 00:06:09, 00:06:13 ]]). "
            "Deze sequentie is belangrijk."
        )

        runs = [TextRun(text=text_with_marker, formatting=RunFormatting())]

        doc = Document(
            metadata=DocumentMetadata(
                line_numbering=LineNumbering(),
                page_settings=PageSettings(),
            ),
            sections=[],
            preamble_paragraphs=[
                Paragraph(runs=runs, formatting=ParagraphFormatting())
            ],
        )

        # Use GoogleTranslatorWrapper with bypass_markers configured
        translator = GoogleTranslatorWrapper(bypass_markers=['tc'])
        # Override translate to just return input (simpler than NoOpTranslator)
        original_translate = translator.translate
        translator.translate = lambda text, src, tgt: text  # type: ignore[method-assign]

        translated = translate_document(doc, translator, "nl", "en", show_progress=False)

        translated_text = translated.preamble_paragraphs[0].text

        # Markers should be in output WITH the [[ tc: ]] markers preserved
        assert "[[ tc: 00:06:01, 00:06:09, 00:06:13 ]]" in translated_text

    def test_markers_with_marker_stripping_translator(self):
        """Markers should survive even if translator strips RUN markers."""
        import re

        # Text with timecode markers
        text_with_marker = (
            "Griffith snijdt (cross-cut's "
            "[[ tc: 00:06:01, 00:06:09 ]]). "
            "Deze sequentie is belangrijk."
        )

        runs = [TextRun(text=text_with_marker, formatting=RunFormatting())]

        doc = Document(
            metadata=DocumentMetadata(
                line_numbering=LineNumbering(),
                page_settings=PageSettings(),
            ),
            sections=[],
            preamble_paragraphs=[
                Paragraph(runs=runs, formatting=ParagraphFormatting())
            ],
        )

        # GoogleTranslatorWrapper with marker stripping
        translator = GoogleTranslatorWrapper(bypass_markers=['tc'])
        translator.translate = lambda text, src, tgt: re.sub(r'<RUN\d+>|</RUN\d+>|</?[biu]>', '', text)  # type: ignore[method-assign]

        translated = translate_document(doc, translator, "nl", "en", show_progress=False)

        translated_text = translated.preamble_paragraphs[0].text

        # Markers should be restored WITH the [[ tc: ]] wrapper
        assert "[[ tc: 00:06:01, 00:06:09 ]]" in translated_text

    def test_markers_long_sequence(self):
        """Long sequences of markers should be protected."""
        long_timecodes = (
            "[[ tc: 00:06:01, 00:06:09, 00:06:13, 00:06:16, 00:06:22, "
            "00:06:25, 00:06:36, 00:06:39, 00:06:48, 00:06:52, 00:06:57, "
            "00:07:05, 00:07:07, 00:07:13, 00:07:16, 00:07:22 ]]"
        )

        text_with_marker = f"Griffith snijdt (cross-cut's {long_timecodes}). Deze sequentie."

        runs = [TextRun(text=text_with_marker, formatting=RunFormatting())]

        doc = Document(
            metadata=DocumentMetadata(
                line_numbering=LineNumbering(),
                page_settings=PageSettings(),
            ),
            sections=[],
            preamble_paragraphs=[
                Paragraph(runs=runs, formatting=ParagraphFormatting())
            ],
        )

        translator = GoogleTranslatorWrapper(bypass_markers=['tc'])
        translator.translate = lambda text, src, tgt: text  # type: ignore[method-assign]

        translated = translate_document(doc, translator, "nl", "en", show_progress=False)

        translated_text = translated.preamble_paragraphs[0].text

        # ALL markers should be in output WITH the [[ tc: ]] wrapper
        assert "[[ tc:" in translated_text
        assert "00:06:01" in translated_text
        assert "00:07:22" in translated_text
        assert "Deze sequentie" in translated_text

    def test_multiple_marker_types_in_document(self):
        """Multiple marker types should all be protected in full document."""
        text_with_markers = (
            "Text with [[ tc: 00:01:00 ]] and [[ note: important detail ]] "
            "and [[ ref: Smith2020 ]]. All should be preserved."
        )

        runs = [TextRun(text=text_with_markers, formatting=RunFormatting())]

        doc = Document(
            metadata=DocumentMetadata(
                line_numbering=LineNumbering(),
                page_settings=PageSettings(),
            ),
            sections=[],
            preamble_paragraphs=[
                Paragraph(runs=runs, formatting=ParagraphFormatting())
            ],
        )

        translator = GoogleTranslatorWrapper(bypass_markers=['tc', 'note', 'ref'])
        translator.translate = lambda text, src, tgt: text  # type: ignore[method-assign]

        translated = translate_document(doc, translator, "nl", "en", show_progress=False)

        translated_text = translated.preamble_paragraphs[0].text

        # All marker types should be preserved
        assert "[[ tc: 00:01:00 ]]" in translated_text
        assert "[[ note: important detail ]]" in translated_text
        assert "[[ ref: Smith2020 ]]" in translated_text


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
