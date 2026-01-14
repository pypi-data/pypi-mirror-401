#!/usr/bin/env python
"""Example: Translation using a callback function.

This example demonstrates how to translate a DOCX document using a
callback function. This is useful for integrating with external
translation APIs or custom translation logic.
"""

import os
import sys

# Add docx_translator to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "translate_docx"))

from translate_docx import CallbackTranslator, extract_document, rebuild_document, translate_document

# Example translation functions


def simple_uppercase_translator(text, source_lang, target_lang):
    """Simple translator that converts to uppercase.

    This is a dummy example - in real use, you would call an API.
    """
    return text.upper()


def mock_google_translate(text, source_lang, target_lang):
    """Mock Google Translate API.

    In a real application, you would call:
    from google.cloud import translate_v2

    client = translate_v2.Client()
    result = client.translate_text(
        text, source_language=source_lang, target_language=target_lang
    )
    return result['translatedText']
    """
    # Mock dictionary for demo
    translations = {
        "Hello": "Hola",
        "World": "Mundo",
        "Document": "Documento",
        "Section": "Sección",
    }
    return translations.get(text, text)


def mock_deepl_translator(text, source_lang, target_lang):
    """Mock DeepL API.

    In a real application, you would call:
    import deepl

    translator = deepl.Translator("YOUR_API_KEY")
    result = translator.translate_text(
        text, source_lang=source_lang, target_lang=target_lang
    )
    return str(result)
    """
    # Mock dictionary for demo
    translations = {
        "Hello": "Hallo",
        "World": "Welt",
        "Document": "Dokument",
        "Section": "Abschnitt",
    }
    return translations.get(text, text)


def main():
    """Demonstrate callback-based translation workflow."""

    print("Translation Callback Examples\n")

    # Example 1: Simple uppercase translator
    print("1. Simple Function Translator")
    print("   Translator: Converts text to uppercase")
    translator1 = CallbackTranslator(simple_uppercase_translator)
    result = translator1.translate("hello", "en", "en")
    print(f"   Input: 'hello' → Output: '{result}'")

    # Example 2: Mock Google Translate
    print("\n2. Mock Google Translate")
    print("   Translator: English → Spanish")
    translator2 = CallbackTranslator(mock_google_translate)
    result = translator2.translate("Hello", "en", "es")
    print(f"   Input: 'Hello' → Output: '{result}'")

    # Example 3: Mock DeepL
    print("\n3. Mock DeepL Translator")
    print("   Translator: English → German")
    translator3 = CallbackTranslator(mock_deepl_translator)
    result = translator3.translate("Hello", "en", "de")
    print(f"   Input: 'Hello' → Output: '{result}'")

    # Example 4: Lambda translator
    print("\n4. Lambda Translator")
    print("   Translator: Custom lambda function")

    def format_text(text, src, tgt):
        return f"[{tgt}] {text}"

    translator4 = CallbackTranslator(format_text)
    result = translator4.translate("hello", "en", "fr")
    print(f"   Input: 'hello' → Output: '{result}'")

    # Example 5: Real document translation (if file exists)
    print("\n5. Full Document Translation Example")
    input_path = "english_document.docx"
    output_path = "spanish_translated.docx"

    if not os.path.exists(input_path):
        print(f"   Note: {input_path} not found")
        print("   Showing workflow:")
        print("   translator = CallbackTranslator(mock_google_translate)")
        print(f"   doc = extract_document('{input_path}')")
        print("   translated = translate_document(doc, translator, 'en', 'es')")
        print(f"   rebuild_document(translated, '{output_path}')")
        return

    print(f"   Extracting from {input_path}...")
    doc = extract_document(input_path)

    print("   Translating with callback...")
    translator = CallbackTranslator(mock_google_translate)
    translated = translate_document(doc, translator, "en", "es")

    print(f"   Rebuilding to {output_path}...")
    rebuild_document(translated, output_path)
    print("   Done!")


if __name__ == "__main__":
    main()
