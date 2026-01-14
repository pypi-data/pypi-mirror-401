#!/usr/bin/env python
"""Example: Manual translation with pre-defined dictionary.

This example demonstrates how to translate a DOCX document using a
manual dictionary of translations. This is useful for static translation
or testing the translation workflow.
"""

import os
import sys

# Add docx_translator to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "translate_docx"))

from translate_docx import ManualTranslator, extract_document, rebuild_document, translate_document


def main():
    """Demonstrate manual translation workflow."""

    # Define a dictionary of translations (German to English)
    translations = {
        # Common words
        "Hallo": "Hello",
        "Welt": "World",
        "Test": "Test",
        "Dokumentation": "Documentation",
        "Beispiel": "Example",
        "Abschnitt": "Section",
        "Inhalt": "Content",
        "Einleitung": "Introduction",
        # Add more translations as needed
    }

    # Create translator
    translator = ManualTranslator(translations)

    # Example usage (commented out since we don't have test files)
    input_path = "german_document.docx"
    output_path = "english_document.docx"

    if not os.path.exists(input_path):
        print(f"Note: {input_path} not found. Showing workflow only.")
        print("\nWorkflow:")
        print("1. Extract DOCX into dataclasses")
        print("2. Translate content using ManualTranslator")
        print("3. Rebuild into new DOCX")
        print("\nCode:")
        print("  translator = ManualTranslator({\n")
        for key, value in list(translations.items())[:3]:
            print(f'      "{key}": "{value}",')
        print("      # ...\n  })")
        print(f"  doc = extract_document('{input_path}')")
        print("  translated = translate_document(doc, translator, 'de', 'en')")
        print(f"  rebuild_document(translated, '{output_path}')")
        return

    # Extract document from DOCX
    print(f"Extracting {input_path}...")
    doc = extract_document(input_path)
    num_sections = len(doc.sections)
    num_preamble = len(doc.preamble_paragraphs)
    print(f"  Extracted {num_sections} sections, {num_preamble} preamble")

    # Translate document
    print("\nTranslating content...")
    translated = translate_document(doc, translator, "de", "en")
    print("  Translation complete (skipped superscripts/subscripts)")

    # Rebuild and save
    print(f"\nRebuilding to {output_path}...")
    rebuild_document(translated, output_path)
    print("  Done!")

    # Summary
    print("\nSummary:")
    print(f"  Input: {input_path}")
    print(f"  Output: {output_path}")
    print("  Language: German → English")
    print("  Translation method: Manual dictionary")
    print(f"  Sections preserved: {len(translated.sections)}")
    print("  Formatting preserved: Yes (all formatting maintained)")
    print("  Citations preserved: Yes (superscripts/subscripts not translated)")


if __name__ == "__main__":
    main()
