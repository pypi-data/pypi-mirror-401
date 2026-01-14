from pathlib import Path

from translate_docx import (
    GoogleTranslatorWrapper,
    ManualTranslator,
    extract_document,
    rebuild_document,
    translate_document,
)

input_path = Path.cwd() /  "user_data" / "griffith_original_newtc.docx"
output_path = Path.cwd() / "user_data" / "griffith_translated_fix2.docx"

# Extract → Translate → Rebuild (using input as template to preserve line spacing)
doc = extract_document(input_path.absolute().as_posix())

# Configure rate limiting and bypass markers
translator = GoogleTranslatorWrapper(
    delay_between_calls=0.5,  # 500ms between calls (2 calls/second)
    max_retries=3,            # Retry up to 3 times on failure
    bypass_markers=['tc']
)
# Translate with progress reporting (enabled by default)
# Set show_progress=False to disable progress output
translated = translate_document(doc, translator, "nl", "en")
rebuild_document(translated, output_path.absolute().as_posix(), template_path=input_path.absolute().as_posix())

print(f"✓ Translation complete! Output saved to {output_path.as_posix()}.docx")
