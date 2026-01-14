"""Translation interface and implementations for document content translation."""

import re
import time
from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Callable, Dict, List, Tuple

from translate_docx.models import Document, Hyperlink, Paragraph, RunFormatting, TextRun


def _validate_marker_name(marker: str) -> None:
    """Validate marker name is alphanumeric only.

    Args:
        marker: Marker name to validate

    Raises:
        ValueError: If marker contains non-alphanumeric characters
    """
    if not marker.isalnum():
        raise ValueError(
            f"Marker name must be alphanumeric only (letters and numbers), got: '{marker}'"
        )


def _compile_marker_patterns(markers: List[str]) -> Dict[str, re.Pattern]:
    """Compile regex patterns for each bypass marker.

    Args:
        markers: List of marker names (e.g., ['tc', 'note', 'ref'])

    Returns:
        Dict mapping marker name (lowercase) to compiled regex pattern

    Raises:
        ValueError: If any marker name is invalid
    """
    patterns = {}

    # Normalize to lowercase and deduplicate
    seen = set()
    normalized_markers = []
    for marker in markers:
        marker_lower = marker.lower()
        if marker_lower not in seen:
            seen.add(marker_lower)
            normalized_markers.append(marker_lower)

    # Validate and compile patterns
    for marker in normalized_markers:
        _validate_marker_name(marker)
        # Pattern: [[ marker: content ]]
        # Allows optional whitespace around marker and colon
        pattern = re.compile(rf'\[\[\s*{re.escape(marker)}:\s*([^\]]+)\]\]')
        patterns[marker] = pattern

    return patterns


def _extract_markers(
    text: str,
    marker_patterns: Dict[str, re.Pattern]
) -> Tuple[str, Dict[str, List[Dict]]]:
    """Extract all configured bypass markers and replace with placeholders.

    Users can mark content in their source documents to protect it from
    being modified by translation APIs. The [[ marker: ... ]] wrappers will
    be preserved in the output document.

    Args:
        text: Text that may contain [[ marker: ... ]] patterns
        marker_patterns: Compiled patterns for each marker type

    Returns:
        Tuple of:
        - text_with_placeholders: Text with markers replaced by {MARKER#}
        - extracted_markers: Dict[marker_name] -> List[extracted items]
          Each item has: 'placeholder', 'content', 'full_match'
    """
    extracted_markers = {}
    result_text = text

    # Extract each marker type separately
    for marker_name, pattern in marker_patterns.items():
        marker_list = []

        # Find all matches for this marker type
        for match in pattern.finditer(text):
            marker_idx = len(marker_list)
            # Use uppercase marker name in placeholder for visibility
            placeholder = f"{{{marker_name.upper()}{marker_idx}}}"
            original_content = match.group(1).strip()  # Just the inner content
            full_match = match.group(0)  # Including [[ marker: ... ]] wrapper

            marker_list.append({
                'placeholder': placeholder,
                'content': original_content,
                'full_match': full_match,
            })

        # Replace all matches for this marker type
        for item in marker_list:
            result_text = result_text.replace(item['full_match'], item['placeholder'], 1)

        # Store if any matches found
        if marker_list:
            extracted_markers[marker_name] = marker_list

    return result_text, extracted_markers


def _restore_markers(
    text: str,
    extracted_markers: Dict[str, List[Dict]]
) -> str:
    """Restore all bypass marker placeholders with original wrapped content.

    Args:
        text: Text with {MARKER#} placeholders
        extracted_markers: Dict from _extract_markers()

    Returns:
        Text with [[ marker: content ]] wrappers restored
    """
    result = text

    # Restore each marker type
    for marker_name, marker_list in extracted_markers.items():
        for item in marker_list:
            # Restore with the full [[ marker: ... ]] wrapper
            result = result.replace(item['placeholder'], item['full_match'])

    return result


class TranslatorInterface(ABC):
    """Abstract base class for document translators.

    Implementations should handle translation of text while preserving
    document structure and formatting. Subclasses must implement the
    translate() method.
    """

    @abstractmethod
    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Translate text from source language to target language.

        Args:
            text: The text to translate
            source_lang: Source language code (e.g., 'de', 'en')
            target_lang: Target language code (e.g., 'en', 'fr')

        Returns:
            Translated text
        """
        raise NotImplementedError

    def should_translate_run(self, run: TextRun) -> bool:
        """Determine if a text run should be translated.

        By default, skips superscripts and subscripts (citations, footnotes).
        Override in subclasses for different behavior.

        Args:
            run: TextRun to check

        Returns:
            True if the run should be translated, False otherwise
        """
        # Skip superscripts and subscripts (citations, footnotes)
        if run.formatting.is_superscript or run.formatting.is_subscript:
            return False

        # Skip whitespace-only runs
        if not run.text or not run.text.strip():
            return False

        return True


class CallbackTranslator(TranslatorInterface):
    """Translator that uses a callback function for translation.

    Useful for simple translations or integration with external APIs.
    """

    def __init__(self, translation_func: Callable[[str, str, str], str]):
        """Initialize with a translation function.

        Args:
            translation_func: Function that takes (text, source_lang, target_lang)
                            and returns translated text
        """
        self.translation_func = translation_func

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Translate using the callback function."""
        return self.translation_func(text, source_lang, target_lang)


class ManualTranslator(TranslatorInterface):
    """Translator that uses a pre-defined dictionary of translations.

    Useful for testing or when you have a static set of translations.
    Falls back to original text if translation not found.

    Supports both exact matching and word-level replacement.
    """

    def __init__(self, translations: Dict[str, str], word_level: bool = False):
        """Initialize with translation dictionary.

        Args:
            translations: Dictionary mapping original text to translated text
            word_level: If True, replace individual words within text.
                       If False (default), only exact text matches are replaced.
        """
        self.translations = translations
        self.word_level = word_level

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Return translation from dictionary, or original text if not found.

        If word_level=True, replaces individual words that match dictionary keys.
        If word_level=False, only replaces if entire text matches a dictionary key.
        """
        # Exact match mode (default behavior)
        if not self.word_level:
            return self.translations.get(text, text)

        # Word-level replacement mode
        result = text
        for original, translation in self.translations.items():
            # Use word boundaries to avoid partial word matches
            # e.g., "Zakenman" won't match "Zakenmannen"
            import re
            pattern = r'\b' + re.escape(original) + r'\b'
            result = re.sub(pattern, translation, result)

        return result


class NoOpTranslator(TranslatorInterface):
    """Translator that returns text unchanged.

    Useful for testing the translation workflow without actually translating.
    """

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Return text unchanged."""
        return text


class GoogleTranslatorWrapper(TranslatorInterface):
    """Wrapper for deep-translator's GoogleTranslator.

    Caches translator instances for each language pair to avoid
    recreating them for every text run.

    Requires: pip install deep-translator
    """

    def __init__(
        self,
        delay_between_calls: float = 0.3,
        max_retries: int = 3,
        bypass_markers: List[str] | None = None
    ):
        """Initialize with rate limiting and bypass marker configuration.

        Args:
            delay_between_calls: Seconds to wait between API calls (default: 0.3s)
                                Set to 0 to disable rate limiting
            max_retries: Number of retry attempts on translation failure (default: 3)
            bypass_markers: List of marker names to protect during translation
                          (e.g., ['tc', 'note', 'ref']). Content marked with
                          [[ marker: ... ]] will not be translated.
                          If None, no markers are protected (explicit opt-in).
        """
        self._translators = {}  # Cache: (source, target) -> GoogleTranslator
        self._delay_between_calls = delay_between_calls
        self._max_retries = max_retries
        self._last_call_time = 0

        # Compile marker patterns once during initialization
        if bypass_markers:
            self._marker_patterns = _compile_marker_patterns(bypass_markers)
        else:
            self._marker_patterns = {}  # Empty dict = no markers protected

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Translate using Google Translate with rate limiting and retry logic.

        Args:
            text: Text to translate
            source_lang: Source language code (e.g., 'nl', 'de')
            target_lang: Target language code (e.g., 'en', 'fr')

        Returns:
            Translated text

        Raises:
            ImportError: If deep-translator is not installed
        """
        try:
            # Create cache key
            key = (source_lang, target_lang)

            # Get or create translator for this language pair
            if key not in self._translators:
                from deep_translator import GoogleTranslator

                self._translators[key] = GoogleTranslator(
                    source=source_lang,
                    target=target_lang
                )

            # Rate limiting: wait if needed
            if self._delay_between_calls > 0:
                elapsed = time.time() - self._last_call_time
                if elapsed < self._delay_between_calls:
                    wait_time = self._delay_between_calls - elapsed
                    time.sleep(wait_time)

            # Retry logic with exponential backoff
            for attempt in range(self._max_retries):
                try:
                    translated = self._translators[key].translate(text)
                    self._last_call_time = time.time()

                    # Remove zero-width characters that Google Translate may insert
                    # These are artifacts used for word-joining hints that we don't need
                    translated = translated.replace('\u200b', '').replace('\u200c', '').replace('\u200d', '').replace('\ufeff', '')

                    return translated

                except Exception as e:
                    if attempt < self._max_retries - 1:
                        # Exponential backoff: 1s, 2s, 4s...
                        wait_time = 2 ** attempt
                        print(f"⚠ Translation attempt {attempt + 1} failed: {e}. Retrying in {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        print(f"⚠ Translation failed after {self._max_retries} attempts: {e}")
                        return text  # Return original text as fallback
            # Fallback if max_retries is 0 (loop never executes)
            return text

        except ImportError:
            raise ImportError(
                "deep-translator is required for GoogleTranslatorWrapper. "
                "Install with: pip install deep-translator"
            )
        except Exception:
            # Return original text as fallback for any other unexpected error
            return text


def _get_format_markers(formatting) -> Dict[str, List[str]]:
    """Get HTML-like opening and closing markers for formatting.

    Args:
        formatting: RunFormatting object

    Returns:
        Dictionary with 'open' and 'close' lists of markers
    """
    markers = {'open': [], 'close': []}

    if formatting.bold:
        markers['open'].append('<b>')
        markers['close'].insert(0, '</b>')
    if formatting.italic:
        markers['open'].append('<i>')
        markers['close'].insert(0, '</i>')
    if formatting.underline:
        markers['open'].append('<u>')
        markers['close'].insert(0, '</u>')

    return markers


def _reconstruct_paragraph_text(para: Paragraph, translator: TranslatorInterface) -> Tuple[str, List[Dict]]:
    """Reconstruct full paragraph text with formatting markup and run boundary markers.

    Converts paragraph runs to HTML-like markup with special markers to preserve
    run boundaries for accurate reconstruction after translation.

    Args:
        para: Paragraph object
        translator: Translator instance (for should_translate_run checks)

    Returns:
        Tuple of:
        - marked_text: Text with HTML-like markers and run boundaries (e.g., "Text is <b>bold</b>|word")
        - format_map: List of metadata for reconstructing runs after translation
    """
    marked_parts = []
    format_map = []
    citation_count = 0
    run_idx = 0

    for element in para.runs:
        if isinstance(element, TextRun):
            # Distinguish between whitespace-only and non-translatable (citations)
            is_whitespace_only = element.text and not element.text.strip()
            is_citation = (
                element.formatting.is_superscript or
                element.formatting.is_subscript
            )

            # Add run start marker
            marked_parts.append(f'<RUN{run_idx}>')

            if is_whitespace_only:
                # Preserve whitespace as-is (e.g., spaces between words)
                marked_parts.append(element.text)
                format_map.append({
                    'type': 'whitespace',
                    'text': element.text,
                    'formatting': deepcopy(element.formatting)
                })
            elif is_citation:
                # Citations/superscripts - use placeholder
                placeholder = f"{{CITE{citation_count}}}"
                marked_parts.append(placeholder)
                format_map.append({
                    'type': 'citation',
                    'text': element.text,
                    'formatting': deepcopy(element.formatting)
                })
                citation_count += 1
            else:
                # Regular text run - add with formatting markers
                markers = _get_format_markers(element.formatting)
                for marker in markers['open']:
                    marked_parts.append(marker)
                marked_parts.append(element.text)
                for marker in markers['close']:
                    marked_parts.append(marker)

                format_map.append({
                    'type': 'text_run',
                    'formatting': deepcopy(element.formatting)
                })

            # Add run end marker
            marked_parts.append(f'</RUN{run_idx}>')
            run_idx += 1

        elif isinstance(element, Hyperlink):
            # Wrap hyperlink with special markers
            link_idx = len(format_map)
            marked_parts.append(f'<RUN{run_idx}><LINK{link_idx}>')

            # Track citations inside this hyperlink
            hyperlink_citations = []

            # Add runs inside hyperlink
            for run in element.runs:
                is_whitespace_only = run.text and not run.text.strip()
                is_citation = (
                    run.formatting.is_superscript or
                    run.formatting.is_subscript
                )

                if is_whitespace_only:
                    marked_parts.append(run.text)
                elif is_citation:
                    # Citation inside hyperlink - track for restoration
                    placeholder = f"{{CITE{citation_count}}}"
                    marked_parts.append(placeholder)
                    hyperlink_citations.append({
                        'cite_num': citation_count,
                        'text': run.text,
                        'formatting': deepcopy(run.formatting)
                    })
                    citation_count += 1
                else:
                    markers = _get_format_markers(run.formatting)
                    for marker in markers['open']:
                        marked_parts.append(marker)
                    marked_parts.append(run.text)
                    for marker in markers['close']:
                        marked_parts.append(marker)

            marked_parts.append(f'</LINK{link_idx}></RUN{run_idx}>')

            format_map.append({
                'type': 'hyperlink',
                'url': element.url,
                'anchor': element.anchor,
                'citations': hyperlink_citations  # Store citation info for restoration
            })
            run_idx += 1

    # Join all parts into marked text
    marked_text = ''.join(marked_parts)

    # Extract bypass markers if translator has them configured
    # This protects marked content from being modified by translation APIs
    marker_patterns = getattr(translator, '_marker_patterns', {})
    if marker_patterns:
        marked_text, extracted_markers = _extract_markers(marked_text, marker_patterns)

        # Store in format_map for restoration after translation
        if extracted_markers:
            format_map.append({
                'type': 'bypass_markers',
                'markers': extracted_markers
            })

    return marked_text, format_map


def _parse_formatted_text(text: str) -> List[TextRun]:
    """Parse text with HTML-like markers into TextRun objects.

    Converts markup like "This is <b>bold</b> text" back to runs with
    appropriate formatting.

    Args:
        text: Text with HTML-like formatting markers

    Returns:
        List of TextRun objects with parsed formatting
    """
    runs = []
    # Pattern to match tags and non-tag content
    pattern = r'(</?[biu]>)|([^<>]+)'

    current_formatting = {
        'bold': False,
        'italic': False,
        'underline': False,
    }

    for match in re.finditer(pattern, text):
        tag = match.group(1)
        content = match.group(2)

        if tag:
            # Process formatting tag
            if tag == '<b>':
                current_formatting['bold'] = True
            elif tag == '</b>':
                current_formatting['bold'] = False
            elif tag == '<i>':
                current_formatting['italic'] = True
            elif tag == '</i>':
                current_formatting['italic'] = False
            elif tag == '<u>':
                current_formatting['underline'] = True
            elif tag == '</u>':
                current_formatting['underline'] = False

        elif content:
            # Create a TextRun with current formatting
            formatting = RunFormatting(
                bold=current_formatting['bold'] if current_formatting['bold'] else None,
                italic=current_formatting['italic'] if current_formatting['italic'] else None,
                underline=current_formatting['underline'] if current_formatting['underline'] else None,
            )
            runs.append(TextRun(text=content, formatting=formatting))

    return runs


def _protect_hyperlinks(marked_text: str, format_map: List[Dict]) -> Tuple[str, Dict]:
    """Protect hyperlink markers from translator modification.

    Replaces LINK markers with simple placeholders that won't be modified
    by translators, and stores the original content for restoration.

    Args:
        marked_text: Text with RUN and LINK markers
        format_map: List of run metadata

    Returns:
        Tuple of:
        - protected_text: Text with LINK markers replaced by safe placeholders
        - hyperlink_backup: Dictionary mapping placeholder IDs to LINK marker content
    """
    hyperlink_backup = {}
    protected_text = marked_text

    # Find all LINK markers and replace with safe placeholders
    link_pattern = r'<LINK(\d+)>(.*?)</LINK\1>'

    for match in re.finditer(link_pattern, marked_text, re.DOTALL):
        link_idx = int(match.group(1))
        link_content = match.group(2)

        # Store the full LINK marker content for restoration
        hyperlink_backup[link_idx] = f'<LINK{link_idx}>{link_content}</LINK{link_idx}>'

        # Replace with a safe placeholder (no angle brackets)
        safe_placeholder = f'##HYPERLINK_MARKER_{link_idx}##'
        protected_text = protected_text.replace(
            f'<LINK{link_idx}>{link_content}</LINK{link_idx}>',
            safe_placeholder,
            1  # Only replace first occurrence to avoid issues with multiple same content
        )

    return protected_text, hyperlink_backup


def _restore_hyperlinks(protected_text: str, hyperlink_backup: Dict[int, str]) -> str:
    """Restore hyperlink markers from safe placeholders.

    Replaces safe placeholders back with original LINK markers.

    Args:
        protected_text: Text with LINK markers replaced by placeholders
        hyperlink_backup: Dictionary mapping placeholder IDs to LINK marker content

    Returns:
        Text with LINK markers restored
    """
    restored_text = protected_text

    for link_idx, link_content in hyperlink_backup.items():
        safe_placeholder = f'##HYPERLINK_MARKER_{link_idx}##'
        restored_text = restored_text.replace(safe_placeholder, link_content)

    return restored_text


def _protect_run_markers(text: str) -> Tuple[str, Dict[str, str]]:
    """Protect RUN markers from translator modification.

    Replaces RUN open/close tags with safe placeholders that won't be modified
    by translators.

    Args:
        text: Text with RUN markers

    Returns:
        Tuple of:
        - protected_text: Text with RUN markers replaced by safe placeholders
        - marker_backup: Dictionary mapping placeholders to original markers
    """
    marker_backup = {}
    protected_text = text

    # Find all unique RUN markers (both opening and closing)
    run_markers = set()
    for match in re.finditer(r'</?RUN\d+>', text):
        run_markers.add(match.group(0))

    # Replace each unique marker with a safe placeholder
    for marker in sorted(run_markers):  # Sort for consistent ordering
        # Create a safe placeholder using format similar to hyperlinks
        # Use ## delimiters and underscores which Google Translate tends to preserve
        # Extract the run number for the placeholder
        run_num = re.search(r'\d+', marker).group(0)
        if marker.startswith('</'):
            safe_placeholder = f'##RUN_CLOSE_{run_num}##'
        else:
            safe_placeholder = f'##RUN_OPEN_{run_num}##'

        marker_backup[safe_placeholder] = marker
        protected_text = protected_text.replace(marker, safe_placeholder)

    return protected_text, marker_backup


def _restore_run_markers(text: str, marker_backup: Dict[str, str]) -> str:
    """Restore RUN markers from safe placeholders.

    Replaces safe placeholders back with original RUN markers.

    Args:
        text: Text with RUN markers replaced by placeholders
        marker_backup: Dictionary mapping placeholders to original markers

    Returns:
        Text with RUN markers restored
    """
    restored_text = text

    for placeholder, original_marker in marker_backup.items():
        restored_text = restored_text.replace(placeholder, original_marker)

    return restored_text


def _protect_quotes(text: str) -> str:
    """Replace all quote characters with placeholders before translation.

    Google Translate tends to normalize quotes - converting straight quotes to
    curly quotes and sometimes vice versa. This protects all quote types by
    replacing them with placeholders that survive translation unchanged.

    For straight quotes, we detect opening vs closing position to use different
    placeholders, since Google adds spurious spaces after opening quotes.

    Args:
        text: Text that may contain quotes

    Returns:
        Text with all quotes replaced by placeholders
    """
    # Protect curly quotes
    text = text.replace('\u201c', '{{DCQS}}')  # U+201C left double quotation mark "
    text = text.replace('\u201d', '{{DCQE}}')  # U+201D right double quotation mark "
    text = text.replace('\u2018', '{{SCQS}}')  # U+2018 left single quotation mark '
    text = text.replace('\u2019', '{{SCQE}}')  # U+2019 right single quotation mark '

    # Protect straight quotes with opening/closing detection
    # Opening quote: preceded by whitespace/start, followed by non-whitespace
    # Closing quote: preceded by non-whitespace, followed by whitespace/end
    text = re.sub(r'(?<=\s)"(?=\S)', '{{DQO}}', text)  # opening double after space
    text = re.sub(r'^"(?=\S)', '{{DQO}}', text)  # opening double at start
    text = re.sub(r'(?<=\S)"(?=\s)', '{{DQC}}', text)  # closing double before space
    text = re.sub(r'(?<=\S)"$', '{{DQC}}', text)  # closing double at end
    text = text.replace('"', '{{DQS}}')  # remaining double quotes (ambiguous)

    text = re.sub(r"(?<=\s)'(?=\S)", '{{SQO}}', text)  # opening single after space
    text = re.sub(r"^'(?=\S)", '{{SQO}}', text)  # opening single at start
    text = re.sub(r"(?<=\S)'(?=\s)", '{{SQC}}', text)  # closing single before space
    text = re.sub(r"(?<=\S)'$", '{{SQC}}', text)  # closing single at end
    text = text.replace("'", '{{SQS}}')  # remaining single quotes (ambiguous)

    return text


def _restore_quotes(text: str) -> str:
    """Restore all quotes from placeholders after translation.

    Args:
        text: Text with quote placeholders

    Returns:
        Text with quotes restored
    """
    # Restore curly quotes
    text = text.replace('{{DCQS}}', '\u201c')  # "
    text = text.replace('{{DCQE}}', '\u201d')  # "
    text = text.replace('{{SCQS}}', '\u2018')  # '
    text = text.replace('{{SCQE}}', '\u2019')  # '

    # Restore opening quotes - strip spurious space AFTER (Google adds these)
    text = re.sub(r'\{\{DQO\}\}\s+(?=\S)', '"', text)
    text = re.sub(r'\{\{SQO\}\}\s+(?=\S)', "'", text)
    text = text.replace('{{DQO}}', '"')  # fallback
    text = text.replace('{{SQO}}', "'")  # fallback

    # Restore closing quotes - no space stripping needed
    text = text.replace('{{DQC}}', '"')
    text = text.replace('{{SQC}}', "'")

    # Restore ambiguous quotes - no space stripping (safer)
    text = text.replace('{{DQS}}', '"')
    text = text.replace('{{SQS}}', "'")

    # Clean up duplicate apostrophes (Google adds straight ' next to our restored curly ')
    text = text.replace("\u2019'", "\u2019")  # curly+straight → curly
    text = text.replace("'\u2019", "\u2019")  # straight+curly → curly

    return text


def _protect_cite_placeholders(text: str) -> Tuple[str, Dict[str, str]]:
    """Protect CITE placeholders from translator modification.

    Replaces {CITE#} with safe placeholders that translators tend to preserve.
    This prevents Google Translate from adding spaces, changing case, or
    translating the word "CITE" to another language.

    Args:
        text: Text with CITE placeholders like {CITE0}, {CITE1}, etc.

    Returns:
        Tuple of:
        - protected_text: Text with CITE placeholders replaced by safe placeholders
        - cite_backup: Dictionary mapping safe placeholders to original placeholders
    """
    cite_backup = {}
    protected_text = text

    # Find all CITE placeholders
    for match in re.finditer(r'\{CITE(\d+)\}', text):
        original = match.group(0)
        cite_num = match.group(1)
        # Use similar format to RUN markers - ## delimiters and underscores
        # which Google Translate tends to preserve
        safe_placeholder = f'##CITE_{cite_num}##'
        cite_backup[safe_placeholder] = original
        protected_text = protected_text.replace(original, safe_placeholder, 1)

    return protected_text, cite_backup


def _restore_cite_placeholders(text: str, cite_backup: Dict[str, str]) -> str:
    """Restore CITE placeholders from safe versions.

    Args:
        text: Text with safe CITE placeholders
        cite_backup: Dictionary mapping safe placeholders to original placeholders

    Returns:
        Text with original CITE placeholders restored
    """
    restored_text = text
    for placeholder, original in cite_backup.items():
        restored_text = restored_text.replace(placeholder, original)
    return restored_text


def _reconstruct_with_run_markers(
    original_marked: str,
    translated_clean: str,
    format_map: List[Dict]
) -> str:
    """Reconstruct RUN markers in translated text based on original structure.

    Maps the run structure from the original marked text to the translated
    clean text, preserving run boundaries.

    Args:
        original_marked: Original text with RUN and other markers
        translated_clean: Translated text without RUN/LINK markers
        format_map: List of format metadata for each run

    Returns:
        Translated text with RUN markers restored
    """
    # Extract the run structure from original marked text
    run_contents = []
    clean_original = re.sub(r'</?RUN\d+>|</?LINK\d+>', '', original_marked)

    # Find all run markers and their positions in the original
    for match in re.finditer(r'<RUN(\d+)>(.*?)</RUN\1>', original_marked, re.DOTALL):
        run_idx = int(match.group(1))
        content = match.group(2)
        run_contents.append({
            'idx': run_idx,
            'content': content,
            'clean_content': re.sub(r'</?[biu]>|</?LINK\d+>|\{CITE\d+\}', '', content)
        })

    # If we have exact same content before/after, just restore the markers directly
    if clean_original == translated_clean:
        return translated_clean.replace(clean_original, original_marked.replace(clean_original, translated_clean))

    # Otherwise, try to map run boundaries by matching content patterns
    # For each run in the original, find where it would be in the translated text
    result_parts = []
    trans_pos = 0

    for run_info in run_contents:
        clean_run_content = run_info['clean_content']

        # Try to find where this run's content appears in the translated text
        # This is tricky because translation can change lengths and structure
        if clean_run_content.strip():  # Non-whitespace run
            # Try to find a matching word or phrase
            # For now, use a simple approach: find the next word boundaries
            remaining = translated_clean[trans_pos:]

            # Find where the next content should end
            # This is approximate - we assume roughly similar word count
            words_in_original = len(clean_run_content.strip().split())

            # Find approximately that many words in remaining
            if words_in_original > 0:
                words_found = 0
                match_end = trans_pos

                for word_match in re.finditer(r'\S+', remaining):
                    words_found += 1
                    match_end = trans_pos + word_match.end()
                    if words_found >= words_in_original:
                        break

                # Extract the translated content for this run
                run_translated = translated_clean[trans_pos:match_end]
                trans_pos = match_end
            else:  # Whitespace or empty
                run_translated = clean_run_content

        else:  # Whitespace run - preserve as-is
            run_translated = clean_run_content

        # Add with RUN markers
        result_parts.append(f'<RUN{run_info["idx"]}>')
        result_parts.append(run_translated)
        result_parts.append(f'</RUN{run_info["idx"]}>')

    # Add any remaining translated content
    if trans_pos < len(translated_clean):
        result_parts.append(translated_clean[trans_pos:])

    return ''.join(result_parts)


def _reconstruct_runs_from_translation(
    translated_text: str,
    format_map: List[Dict],
    translator: TranslatorInterface
) -> List:
    """Reconstruct paragraph runs from translated text with markup and run markers.

    Uses RUN boundary markers to extract individual run texts while preserving
    formatting and restoring citations and hyperlinks.

    Args:
        translated_text: Translated text with formatting markup and RUN markers
        format_map: List of metadata for runs and citations
        translator: Translator instance (for reference)

    Returns:
        List of TextRun and Hyperlink objects
    """
    new_runs = []

    # First, restore any bypass markers that were protected before translation
    # This must happen before other processing to restore {MARKER#} placeholders
    for item in format_map:
        if item['type'] == 'bypass_markers':
            translated_text = _restore_markers(translated_text, item['markers'])
            break  # Only one bypass_markers entry per format_map

    # Build citation lookup: citation_number -> citation_item
    # This enables O(1) lookup by placeholder number (e.g., {CITE0} -> citation_lookup[0])
    # Includes both standalone citations AND citations inside hyperlinks
    citation_lookup = {}
    cite_idx = 0
    for item in format_map:
        if item['type'] == 'citation':
            # Standalone citation
            citation_lookup[cite_idx] = item
            cite_idx += 1
        elif item['type'] == 'hyperlink' and item.get('citations'):
            # Citations inside hyperlink - use their stored cite_num
            for cite_info in item['citations']:
                citation_lookup[cite_info['cite_num']] = {
                    'type': 'citation',
                    'text': cite_info['text'],
                    'formatting': cite_info['formatting']
                }

    # Track which citations have been restored (for fallback handling)
    restored_citations = set()

    # Extract hyperlink contents and replace with placeholders
    hyperlink_contents = {}
    for i, item in enumerate(format_map):
        if item['type'] == 'hyperlink':
            # Find the hyperlink markers in text
            pattern = f'<LINK{i}>(.*?)</LINK{i}>'
            match = re.search(pattern, translated_text, re.DOTALL)
            if match:
                link_content = match.group(1)
                # Parse the content inside hyperlink
                link_runs = _parse_formatted_text(link_content)

                # Handle CITE placeholders in hyperlink content
                # Replace {CITE#} with actual citation text from citation_lookup
                final_runs = []
                for run in link_runs:
                    if '{CITE' in run.text:
                        # Split and replace CITE placeholders
                        cite_parts = re.split(r'(\{CITE\d+\})', run.text)
                        for part in cite_parts:
                            if part.startswith('{CITE') and part.endswith('}'):
                                cite_match = re.search(r'\d+', part)
                                if cite_match:
                                    cite_num = int(cite_match.group())
                                    cite_item = citation_lookup.get(cite_num)
                                    if cite_item:
                                        final_runs.append(TextRun(
                                            text=cite_item['text'],
                                            formatting=cite_item['formatting']
                                        ))
                                        restored_citations.add(cite_num)
                            elif part:
                                final_runs.append(TextRun(
                                    text=part,
                                    formatting=run.formatting
                                ))
                    else:
                        final_runs.append(run)

                hyperlink_contents[i] = {
                    'runs': final_runs,
                    'text': ''.join(run.text for run in final_runs)
                }

    # Remove hyperlink markers from text
    for i in range(len(format_map)):
        if format_map[i]['type'] == 'hyperlink':
            pattern = f'<LINK{i}>(.*?)</LINK{i}>'
            translated_text = re.sub(pattern, f'{{HYPERLINK{i}}}', translated_text, flags=re.DOTALL)

    # Extract run boundaries and their content
    # Handle both matched AND mismatched RUN markers (Google may merge runs)
    # Pattern matches: <RUNX>content</RUNY> where X and Y might be different
    run_pattern = r'<RUN(\d+)>(.*?)</RUN(\d+)>'

    for match in re.finditer(run_pattern, translated_text, re.DOTALL):
        open_idx = int(match.group(1))
        run_content = match.group(2)
        close_idx = int(match.group(3))

        # Use the opening RUN number to look up format
        run_idx = open_idx
        format_item = format_map[run_idx] if run_idx < len(format_map) else None

        if not format_item:
            continue

        # If markers are mismatched (Google merged runs), we may need to handle multiple runs
        # For now, process the opening run and let subsequent iterations handle the rest
        if open_idx != close_idx:
            # Google merged runs - the content spans multiple original runs
            # Process based on the opening run's format
            pass

        if format_item['type'] == 'whitespace':
            # Whitespace run - preserve as-is
            new_runs.append(TextRun(
                text=format_item['text'],
                formatting=format_item['formatting']
            ))

        elif format_item['type'] == 'citation':
            # Citation run - check if placeholder still in content
            if '{CITE' in run_content:
                # Extract the citation text
                cite_pattern = r'\{CITE\d+\}'
                if re.search(cite_pattern, run_content):
                    new_runs.append(TextRun(
                        text=format_item['text'],
                        formatting=format_item['formatting']
                    ))
                    # Track this citation as restored
                    for cite_num, item in citation_lookup.items():
                        if item is format_item:
                            restored_citations.add(cite_num)
                            break
            else:
                # Placeholder was removed, add citation
                new_runs.append(TextRun(
                    text=format_item['text'],
                    formatting=format_item['formatting']
                ))
                # Track this citation as restored
                for cite_num, item in citation_lookup.items():
                    if item is format_item:
                        restored_citations.add(cite_num)
                        break

        elif format_item['type'] == 'hyperlink':
            # Hyperlink run
            hyperlink_pattern = r'\{HYPERLINK(\d+)\}'
            match = re.search(hyperlink_pattern, run_content)
            if match:
                link_idx = int(match.group(1))
                if link_idx in hyperlink_contents:
                    new_hyperlink = Hyperlink(
                        runs=hyperlink_contents[link_idx]['runs'],
                        url=format_map[link_idx]['url'],
                        anchor=format_map[link_idx]['anchor']
                    )
                    new_runs.append(new_hyperlink)

        elif format_item['type'] == 'text_run':
            # Regular text run - parse with formatting
            parsed_runs = _parse_formatted_text(run_content)
            # Get the original formatting to preserve non-visual attributes
            original_formatting = format_item['formatting']

            for parsed_run in parsed_runs:
                # Merge parsed formatting with original attributes
                # Use parsed bold/italic/underline but keep original font info
                merged_formatting = deepcopy(original_formatting)
                merged_formatting.bold = parsed_run.formatting.bold
                merged_formatting.italic = parsed_run.formatting.italic
                merged_formatting.underline = parsed_run.formatting.underline

                # Handle placeholders in parsed runs
                text = parsed_run.text
                if '{CITE' in text:
                    # Extract citations using direct lookup
                    cite_parts = re.split(r'(\{CITE\d+\})', text)
                    for part in cite_parts:
                        if part.startswith('{CITE') and part.endswith('}'):
                            # Extract citation number directly from placeholder
                            cite_match = re.search(r'\d+', part)
                            if cite_match:
                                cite_num = int(cite_match.group())
                                cite_item = citation_lookup.get(cite_num)
                                if cite_item:
                                    new_runs.append(TextRun(
                                        text=cite_item['text'],
                                        formatting=cite_item['formatting']
                                    ))
                                    restored_citations.add(cite_num)
                        elif part:
                            new_runs.append(TextRun(
                                text=part,
                                formatting=merged_formatting
                            ))
                else:
                    new_runs.append(TextRun(
                        text=parsed_run.text,
                        formatting=merged_formatting
                    ))

    # Fallback: Check for any unrestored citations and append them
    # This handles cases where translator merged RUN markers and citations were lost
    for cite_num in sorted(citation_lookup.keys()):
        if cite_num not in restored_citations:
            cite_item = citation_lookup[cite_num]
            new_runs.append(TextRun(
                text=cite_item['text'],
                formatting=cite_item['formatting']
            ))

    return new_runs


def translate_document(
    doc: Document,
    translator: TranslatorInterface,
    source_lang: str,
    target_lang: str,
    show_progress: bool = True,
    progress_callback: "Callable[[int, int], None] | None" = None,
) -> Document:
    """Translate a document's content while preserving structure and formatting.

    Translates all text runs that match the translator's should_translate_run()
    criteria (by default, all runs except superscripts/subscripts).
    Document structure, formatting, metadata, and section organization are
    preserved.

    Args:
        doc: Document object to translate
        translator: TranslatorInterface implementation for translation
        source_lang: Source language code (e.g., 'de')
        target_lang: Target language code (e.g., 'en')
        show_progress: If True, print translation progress (default: True)
        progress_callback: Optional callback(current, total) for progress updates

    Returns:
        New Document object with translated content. Original document is unchanged.
    """
    # Store original metadata and paragraph formatting before deepcopy
    # (deepcopy corrupts python-docx Length objects in formatting)
    original_metadata = doc.metadata

    # Store references to original paragraph formatting objects
    original_formatting = {}
    for i, para in enumerate(doc.preamble_paragraphs):
        original_formatting[('preamble', i)] = para.formatting

    for sec_idx, section in enumerate(doc.sections):
        original_formatting[('section_header', sec_idx)] = section.header.formatting
        for para_idx, para in enumerate(section.paragraphs):
            original_formatting[('section_body', sec_idx, para_idx)] = para.formatting

    # Deep copy to avoid modifying original
    translated_doc = deepcopy(doc)

    # Restore the uncorrupted metadata
    translated_doc.metadata = original_metadata

    # Restore uncorrupted paragraph formatting
    for i, para in enumerate(translated_doc.preamble_paragraphs):
        para.formatting = original_formatting[('preamble', i)]

    for sec_idx, section in enumerate(translated_doc.sections):
        section.header.formatting = original_formatting[('section_header', sec_idx)]
        for para_idx, para in enumerate(section.paragraphs):
            para.formatting = original_formatting[('section_body', sec_idx, para_idx)]

    def _split_paragraph_into_chunks(para: Paragraph, max_chunk_size: int = 1500) -> List[Paragraph]:
        """Split a long paragraph into smaller chunks at sentence boundaries.

        This prevents Google Translate from truncating or garbling long content.
        Chunks are split at sentence endings ('. ', '? ', '! ') to maintain context.

        Args:
            para: Paragraph to potentially split
            max_chunk_size: Maximum characters per chunk (default 1500)

        Returns:
            List of Paragraph objects (just one if no split needed)
        """
        # Quick check: if paragraph text is short enough, don't split
        if len(para.text) < max_chunk_size:
            return [para]

        # Build chunks by grouping runs
        chunks = []
        current_chunk_runs = []
        current_chunk_text = ""

        for run in para.runs:
            # Check if adding this run would exceed the limit
            potential_text = current_chunk_text + run.text

            if len(potential_text) > max_chunk_size and current_chunk_runs:
                # Try to find a good split point in the current chunk text
                # Look for sentence endings: '. ', '? ', '! '
                split_point = -1

                # SMART CHUNKING: If we have a long sequence of timestamps/numbers,
                # split right after them to avoid Google Translate getting confused
                # Pattern: look for ". " following a sequence like "00:07:22. "
                import re
                timestamp_pattern = r'(\d{2}:\d{2}:\d{2})\.\s+'
                matches = list(re.finditer(timestamp_pattern, current_chunk_text))
                if matches:
                    # Find the last timestamp in the chunk
                    last_match = matches[-1]
                    # Split right after it (after the ". ")
                    potential_split = last_match.end()
                    # Only use this split if it's in the latter half of the chunk
                    if potential_split > len(current_chunk_text) // 2:
                        split_point = potential_split

                # If no timestamp split found, use regular sentence endings
                if split_point == -1:
                    for separator in ['. ', '? ', '! ', '. "', '." ', '.\' ']:
                        idx = current_chunk_text.rfind(separator)
                        if idx > len(current_chunk_text) // 2:  # Only split if past halfway
                            split_point = idx + len(separator)
                            break

                if split_point > 0:
                    # Split within the current runs by finding which run contains split point
                    chars_so_far = 0
                    for i, chunk_run in enumerate(current_chunk_runs):
                        chars_so_far += len(chunk_run.text)
                        if chars_so_far >= split_point:
                            # Split this run
                            overflow = chars_so_far - split_point
                            if overflow > 0:
                                # Need to split this run into two parts
                                split_run_idx = split_point - (chars_so_far - len(chunk_run.text))
                                run_text = chunk_run.text
                                first_part = run_text[:split_run_idx]
                                second_part = run_text[split_run_idx:]

                                # Create new runs
                                first_run = TextRun(text=first_part, formatting=chunk_run.formatting)
                                second_run = TextRun(text=second_part, formatting=chunk_run.formatting)

                                # Add first part to current chunk
                                current_chunk_runs[i] = first_run

                                # Create chunk from current runs
                                chunk_para = Paragraph(
                                    runs=current_chunk_runs[:i+1],
                                    formatting=para.formatting,
                                    is_header=para.is_header,
                                    style_name=para.style_name
                                )
                                chunks.append(chunk_para)

                                # Start new chunk with second part and remaining runs
                                current_chunk_runs = [second_run] + current_chunk_runs[i+1:]
                                current_chunk_text = "".join(r.text for r in current_chunk_runs)
                                break
                            else:
                                # Split falls exactly on run boundary
                                chunk_para = Paragraph(
                                    runs=current_chunk_runs[:i+1],
                                    formatting=para.formatting,
                                    is_header=para.is_header,
                                    style_name=para.style_name
                                )
                                chunks.append(chunk_para)

                                current_chunk_runs = current_chunk_runs[i+1:]
                                current_chunk_text = "".join(r.text for r in current_chunk_runs)
                                break
                else:
                    # No good split point found, just split at current run boundary
                    chunk_para = Paragraph(
                        runs=current_chunk_runs,
                        formatting=para.formatting,
                        is_header=para.is_header,
                        style_name=para.style_name
                    )
                    chunks.append(chunk_para)
                    current_chunk_runs = []
                    current_chunk_text = ""

            # Add current run to chunk
            current_chunk_runs.append(run)
            current_chunk_text = "".join(r.text for r in current_chunk_runs)

        # Add remaining runs as final chunk
        if current_chunk_runs:
            chunk_para = Paragraph(
                runs=current_chunk_runs,
                formatting=para.formatting,
                is_header=para.is_header,
                style_name=para.style_name
            )
            chunks.append(chunk_para)

        return chunks if chunks else [para]

    def translate_paragraph(para: Paragraph) -> Paragraph:
        """Translate entire paragraph while preserving formatting and context.

        Uses markup-based approach: converts formatting to HTML-like tags,
        translates full paragraph text for better context preservation,
        then reconstructs runs from translated markup.

        For very long paragraphs (>1500 chars), automatically chunks them
        at sentence boundaries to prevent Google Translate truncation/garbling.
        """
        # Skip empty paragraphs
        if not para.runs or not para.text.strip():
            return para

        # Check if paragraph needs chunking (long paragraphs cause Google Translate issues)
        # Use 1000 chars as max to be conservative and ensure Google doesn't truncate/garble
        chunks = _split_paragraph_into_chunks(para, max_chunk_size=1000)

        if len(chunks) > 1:
            # Translate each chunk separately and combine results
            all_translated_runs = []
            for chunk in chunks:
                translated_chunk = _translate_single_paragraph(chunk)
                all_translated_runs.extend(translated_chunk.runs)

            # Update original paragraph with all translated runs
            para.runs = all_translated_runs
            return para
        else:
            # Paragraph is short enough, translate normally
            return _translate_single_paragraph(para)

    def _translate_single_paragraph(para: Paragraph) -> Paragraph:
        """Translate a single paragraph (helper function for translate_paragraph).

        This is the core translation logic extracted to allow chunking.
        """
        # Convert paragraph to markup format with run boundaries
        marked_text, format_map = _reconstruct_paragraph_text(para, translator)

        # Protect CITE placeholders FIRST - before hyperlinks, so CITE inside hyperlinks
        # are also protected. This prevents translators from modifying {CITE0} to
        # {cite0}, { CITE0 }, or translating "CITE" to another language.
        protected_text, cite_backup = _protect_cite_placeholders(marked_text)

        # Protect hyperlinks and special markers before translation
        # Store hyperlink content separately to avoid translator modification
        # Note: CITE placeholders inside hyperlinks are already protected (##CITE_0##)
        protected_text, hyperlink_backup = _protect_hyperlinks(protected_text, format_map)

        # Also protect RUN markers to prevent translators (like Google Translate)
        # from stripping or corrupting them. Without this, HTML-like <RUN0> markers
        # get removed, causing the reconstruction to fail and lose content.
        protected_text, run_marker_backup = _protect_run_markers(protected_text)

        # Protect all quotes from being normalized by Google Translate
        protected_text = _protect_quotes(protected_text)

        # Translate the marked text (CITE, hyperlinks, RUN markers, and quotes all protected)
        translated_protected = translator.translate(protected_text, source_lang, target_lang)

        # Restore in reverse order of protection
        translated_protected = _restore_run_markers(translated_protected, run_marker_backup)

        # Restore quotes
        translated_protected = _restore_quotes(translated_protected)

        # Restore hyperlinks - this brings back ##CITE_0## inside hyperlink content
        translated_protected = _restore_hyperlinks(translated_protected, hyperlink_backup)

        # Restore CITE placeholders LAST - converts ##CITE_0## back to {CITE0}
        translated_marked_text = _restore_cite_placeholders(translated_protected, cite_backup)

        # Reconstruct runs from translated text with markers
        new_runs = _reconstruct_runs_from_translation(translated_marked_text, format_map, translator)

        # Update paragraph with new runs
        para.runs = new_runs

        return para

    # Calculate total paragraphs for progress reporting
    total_paragraphs = (
        len(translated_doc.preamble_paragraphs) +
        sum(len(s.paragraphs) + 1 for s in translated_doc.sections)  # +1 for each section header
    )
    translated_count = [0]  # Use list to allow modification in nested function

    def translate_paragraph_with_progress(para: Paragraph) -> Paragraph:
        """Translate paragraph with progress tracking."""
        translated_count[0] += 1
        if show_progress:
            print(f"\rTranslating: {translated_count[0]}/{total_paragraphs} paragraphs...", end='', flush=True)
        if progress_callback:
            progress_callback(translated_count[0], total_paragraphs)
        return translate_paragraph(para)

    # Translate preamble paragraphs
    for para in translated_doc.preamble_paragraphs:
        translate_paragraph_with_progress(para)

    # Translate section headers and body paragraphs
    for section in translated_doc.sections:
        translate_paragraph_with_progress(section.header)
        for para in section.paragraphs:
            translate_paragraph_with_progress(para)

    # Print new line after progress reporting
    if show_progress:
        print()

    return translated_doc


def extract_translate_rebuild(
    input_path: str,
    output_path: str,
    translator: TranslatorInterface,
    source_lang: str,
    target_lang: str,
    use_template: bool = True,
) -> Document:
    """Complete pipeline: extract document, translate, and rebuild.

    Convenience function that combines extraction, translation, and rebuilding
    into a single operation.

    Args:
        input_path: Path to input DOCX file
        output_path: Path where translated DOCX will be saved
        translator: TranslatorInterface implementation for translation
        source_lang: Source language code
        target_lang: Target language code
        use_template: If True, use input document as template to preserve
                     line spacing and other document defaults (default: True)

    Returns:
        Translated Document object (also saved to output_path)
    """
    # Import here to avoid circular imports
    from .extractor import extract_document
    from .rebuilder import rebuild_document

    # Extract document
    doc = extract_document(input_path)

    # Translate
    translated_doc = translate_document(doc, translator, source_lang, target_lang)

    # Rebuild and save (optionally using input as template)
    template_path = input_path if use_template else None
    rebuild_document(translated_doc, output_path, template_path=template_path)

    return translated_doc
