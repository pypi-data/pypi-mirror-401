#!/usr/bin/env python
"""Example: Full pipeline - extract, translate, and rebuild in one call.

This example demonstrates the extract_translate_rebuild convenience function
that handles the complete workflow in a single call.
"""

import os
import sys

# Add docx_translator to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "translate_docx"))

from translate_docx.translator import (
    CallbackTranslator,
    ManualTranslator,
    extract_translate_rebuild,
)


def german_to_english(text, source_lang, target_lang):
    """Simple German to English translator for demo."""
    translations = {
        "Einleitung": "Introduction",
        "Hintergrund": "Background",
        "Methoden": "Methods",
        "Ergebnisse": "Results",
        "Schlussfolgerung": "Conclusion",
        "Danksagungen": "Acknowledgments",
        "Literatur": "References",
    }
    return translations.get(text, text)


def main():
    """Demonstrate the full pipeline."""

    print("Full Pipeline: Extract → Translate → Rebuild\n")

    # Option 1: Using ManualTranslator
    print("Option 1: Manual Dictionary Translation")
    print("-" * 50)

    translations = {
        "Willkommen": "Welcome",
        "Kapitel": "Chapter",
        "Zusammenfassung": "Summary",
    }

    translator = ManualTranslator(translations)
    input_file = "german_document.docx"
    output_file = "english_translated.docx"

    if os.path.exists(input_file):
        print(f"Processing: {input_file}")
        doc = extract_translate_rebuild(
            input_path=input_file,
            output_path=output_file,
            translator=translator,
            source_lang="de",
            target_lang="en",
        )
        print(f"✓ Translated document saved to: {output_file}")
        print(f"  Sections: {len(doc.sections)}")
        print("  Language: German → English")
    else:
        print(f"Example (file not found): {input_file} → {output_file}")
        print("Code:")
        print(
            f"""
    translator = ManualTranslator({translations})
    extract_translate_rebuild(
        input_path="{input_file}",
        output_path="{output_file}",
        translator=translator,
        source_lang="de",
        target_lang="en",
    )
"""
        )

    # Option 2: Using CallbackTranslator with function
    print("\n\nOption 2: Callback Function Translation")
    print("-" * 50)

    callback_translator = CallbackTranslator(german_to_english)
    input_file2 = "german_academic.docx"
    output_file2 = "english_academic.docx"

    if os.path.exists(input_file2):
        print(f"Processing: {input_file2}")
        doc2 = extract_translate_rebuild(
            input_path=input_file2,
            output_path=output_file2,
            translator=callback_translator,
            source_lang="de",
            target_lang="en",
        )
        print(f"✓ Translated document saved to: {output_file2}")
        print(f"  Sections: {len(doc2.sections)}")
    else:
        print(f"Example (file not found): {input_file2} → {output_file2}")
        print("Code:")
        print(
            f"""
    def german_to_english(text, source_lang, target_lang):
        translations = {{
            "Einleitung": "Introduction",
            "Ergebnisse": "Results",
            # ... more translations
        }}
        return translations.get(text, text)

    translator = CallbackTranslator(german_to_english)
    extract_translate_rebuild(
        input_path="{input_file2}",
        output_path="{output_file2}",
        translator=translator,
        source_lang="de",
        target_lang="en",
    )
"""
        )

    # Option 3: Using Lambda
    print("\n\nOption 3: Lambda Translator")
    print("-" * 50)

    print("Code:")
    print(
        """
    def mark_text(text, src, tgt):
        return f"[TRANSLATED: {text}]"

    translator = CallbackTranslator(mark_text)
    extract_translate_rebuild(
        input_path="test_document.docx",
        output_path="marked_document.docx",
        translator=translator,
        source_lang="en",
        target_lang="marked",
    )
"""
    )

    # Summary
    print("\n\nKey Features")
    print("-" * 50)
    print("✓ Single function call for complete workflow")
    print("✓ Supports multiple translator implementations")
    print("✓ Preserves document structure and formatting")
    print("✓ Automatically skips citations (superscripts)")
    print("✓ Original document unchanged (deep copy used)")
    print("✓ Metadata preserved (page settings, line numbering)")
    print("✓ Section organization maintained")

    # API Integration Example
    print("\n\nIntegration with Translation APIs")
    print("-" * 50)
    print(
        """
To integrate with Google Translate, DeepL, or other APIs:

    from google.cloud import translate_v2

    client = translate_v2.Client()

    def google_translate(text, source_lang, target_lang):
        result = client.translate_text(
            text,
            source_language=source_lang,
            target_language=target_lang
        )
        return result['translatedText']

    translator = CallbackTranslator(google_translate)
    extract_translate_rebuild(
        input_path="input.docx",
        output_path="output.docx",
        translator=translator,
        source_lang="de",
        target_lang="en",
    )
"""
    )


if __name__ == "__main__":
    main()
