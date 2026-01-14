#!/usr/bin/env python
"""Example: Citation preservation during translation.

This example demonstrates how the translation system automatically preserves
citations (superscripts/subscripts) in the original language while translating
the rest of the text.
"""

import os
import sys

# Add docx_translator to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "translate_docx"))

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
    ManualTranslator,
    translate_document,
)


def create_document_with_citations():
    """Create a sample document with citations (superscripts)."""

    # Define translations (German to English)
    translations = {
        "Diese": "This",
        "Methode": "method",
        "ist": "is",
        "sehr": "very",
        "effektiv": "effective",
        "Die": "The",
        "Ergebnisse": "results",
        "zeigen": "show",
        "dass": "that",
        "es": "it",
        "funktioniert": "works",
        "Abschnitt": "Section",
        "Einleitung": "Introduction",
        "Methoden": "Methods",
    }

    # Create a document with citations
    doc = Document(
        metadata=DocumentMetadata(
            line_numbering=LineNumbering(),
            page_settings=PageSettings(),
        ),
        preamble_paragraphs=[
            Paragraph(
                runs=[
                    TextRun(text="Einleitung", formatting=RunFormatting(bold=True)),
                ],
                formatting=ParagraphFormatting(),
            ),
        ],
        sections=[
            Section(
                header=Paragraph(
                    runs=[
                        TextRun(text="Methoden", formatting=RunFormatting(bold=True)),
                    ],
                    formatting=ParagraphFormatting(),
                    is_header=True,
                ),
                paragraphs=[
                    Paragraph(
                        runs=[
                            TextRun(text="Diese", formatting=RunFormatting()),
                            TextRun(text=" ", formatting=RunFormatting()),
                            TextRun(text="Methode", formatting=RunFormatting()),
                            TextRun(text=" ", formatting=RunFormatting()),
                            TextRun(text="ist", formatting=RunFormatting()),
                            TextRun(text=" ", formatting=RunFormatting()),
                            TextRun(text="sehr", formatting=RunFormatting()),
                            TextRun(text=" ", formatting=RunFormatting()),
                            TextRun(text="effektiv", formatting=RunFormatting()),
                            TextRun(text=" ", formatting=RunFormatting()),
                            TextRun(
                                text="[1]",
                                formatting=RunFormatting(is_superscript=True),
                            ),
                            TextRun(text=".", formatting=RunFormatting()),
                        ],
                        formatting=ParagraphFormatting(),
                    ),
                    Paragraph(
                        runs=[
                            TextRun(text="Die", formatting=RunFormatting()),
                            TextRun(text=" ", formatting=RunFormatting()),
                            TextRun(text="Ergebnisse", formatting=RunFormatting()),
                            TextRun(text=" ", formatting=RunFormatting()),
                            TextRun(text="zeigen", formatting=RunFormatting()),
                            TextRun(text=" ", formatting=RunFormatting()),
                            TextRun(text="dass", formatting=RunFormatting()),
                            TextRun(text=" ", formatting=RunFormatting()),
                            TextRun(text="es", formatting=RunFormatting()),
                            TextRun(text=" ", formatting=RunFormatting()),
                            TextRun(text="funktioniert", formatting=RunFormatting()),
                            TextRun(
                                text="[2]",
                                formatting=RunFormatting(is_superscript=True),
                            ),
                            TextRun(text=".", formatting=RunFormatting()),
                        ],
                        formatting=ParagraphFormatting(),
                    ),
                ],
            ),
        ],
    )

    return doc, translations


def main():
    """Demonstrate citation preservation."""

    print("Citation Preservation During Translation\n")
    print("=" * 60)

    # Create sample document
    doc, translations = create_document_with_citations()

    # Create translator
    translator = ManualTranslator(translations)

    # Display original document
    print("\nOriginal Document (German):")
    print("-" * 60)

    for para in doc.preamble_paragraphs:
        text = "".join(run.text for run in para.runs)
        print(f"  {text}")

    for section in doc.sections:
        header_text = "".join(run.text for run in section.header.runs)
        print(f"  {header_text}")
        for para in section.paragraphs:
            text = ""
            for run in para.runs:
                if run.formatting.is_superscript:
                    text += f"[SUPERSCRIPT: {run.text}]"
                else:
                    text += run.text
            print(f"  {text}")

    # Translate document
    print("\nTranslating...")
    print("-" * 60)
    translated = translate_document(doc, translator, "de", "en")

    # Display translated document
    print("\nTranslated Document (English):")
    print("-" * 60)

    for para in translated.preamble_paragraphs:
        text = "".join(run.text for run in para.runs)
        print(f"  {text}")

    for section in translated.sections:
        header_text = "".join(run.text for run in section.header.runs)
        print(f"  {header_text}")
        for para in section.paragraphs:
            text = ""
            for run in para.runs:
                if run.formatting.is_superscript:
                    # Citation preserved in original form
                    text += f"[CITATION: {run.text}]"
                else:
                    text += run.text
            print(f"  {text}")

    # Summary
    print("\n\nKey Points:")
    print("-" * 60)
    print("✓ Text content translated: German → English")
    print("✓ Citations preserved: [1], [2] remain unchanged")
    print("✓ Superscript formatting preserved")
    print("✓ Normal text formatting preserved (bold, etc.)")
    print("✓ Document structure preserved (sections, paragraphs)")

    print("\n\nHow It Works:")
    print("-" * 60)
    print(
        """
The TranslatorInterface has a method: should_translate_run(run)

This method returns False for:
  • Runs with is_superscript=True
  • Runs with is_subscript=True
  • Whitespace-only runs
  • Empty runs

This ensures citations and footnotes stay in their original language
while all other content gets translated.
"""
    )

    print("\n\nCustom Citation Handling:")
    print("-" * 60)
    print(
        """
You can override should_translate_run() in your translator:

class CustomTranslator(TranslatorInterface):
    def translate(self, text, source_lang, target_lang):
        # Your translation logic
        return translated_text

    def should_translate_run(self, run):
        # Skip URLs in addition to superscripts
        if run.text.startswith('http'):
            return False
        # Use default behavior for citations
        return super().should_translate_run(run)
"""
    )


if __name__ == "__main__":
    main()
