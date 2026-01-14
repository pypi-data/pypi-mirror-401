"""Command-line interface for translate-docx."""

from pathlib import Path
from typing import Optional

import typer
from typing_extensions import Annotated

from translate_docx import __version__
from translate_docx.extractor import extract_document
from translate_docx.rebuilder import rebuild_document
from translate_docx.translator import GoogleTranslatorWrapper, translate_document


def version_callback(value: bool):
    if value:
        typer.echo(f"translate-docx version {__version__}")
        raise typer.Exit()


app = typer.Typer(
    name="translate-docx",
    help="Translate DOCX documents while preserving formatting.",
    add_completion=False,
)


@app.callback()
def main(
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version",
            "-V",
            callback=version_callback,
            is_eager=True,
            help="Show version and exit",
        ),
    ] = None,
):
    """Translate DOCX documents while preserving formatting."""
    pass


@app.command()
def translate(
    input_file: Annotated[
        Path,
        typer.Argument(
            help="Input DOCX file to translate",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
        ),
    ],
    output_file: Annotated[
        Path,
        typer.Argument(
            help="Output DOCX file path",
            file_okay=True,
            dir_okay=False,
        ),
    ],
    source: Annotated[
        str,
        typer.Option(
            "--source",
            "-s",
            help="Source language code (e.g., 'nl', 'de', 'fr')",
        ),
    ] = "auto",
    target: Annotated[
        str,
        typer.Option(
            "--target",
            "-t",
            help="Target language code (e.g., 'en', 'es', 'de')",
        ),
    ] = "en",
    template: Annotated[
        Optional[Path],
        typer.Option(
            "--template",
            help="Template DOCX file (defaults to input file)",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
        ),
    ] = None,
    delay: Annotated[
        float,
        typer.Option(
            "--delay",
            "-d",
            help="Delay between translation API calls in seconds",
        ),
    ] = 0.5,
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose",
            "-v",
            help="Show detailed progress information",
        ),
    ] = False,
    bypass_markers: Annotated[
        Optional[str],
        typer.Option(
            "--bypass-markers",
            "-b",
            help="Comma-separated list of markers to protect from translation (e.g., 'tc,note,ref')",
        ),
    ] = None,
):
    """
    Translate a DOCX document from one language to another.

    Preserves all formatting, styles, headers, and document structure.

    Use --bypass-markers to protect specific content:
        Text wrapped in [[ marker: content ]] will not be translated.

    Examples:

        translate-docx translate input.docx output.docx -s nl -t en

        translate-docx translate report.docx report_translated.docx --source de --target en --verbose

        translate-docx translate input.docx output.docx -s nl -t en --bypass-markers tc,note,ref
    """
    template_path = template if template else input_file

    # Parse bypass markers from CLI
    marker_list = None
    if bypass_markers:
        marker_list = [m.strip() for m in bypass_markers.split(',') if m.strip()]

    if verbose:
        typer.echo(f"Input:    {input_file}")
        typer.echo(f"Output:   {output_file}")
        typer.echo(f"Source:   {source}")
        typer.echo(f"Target:   {target}")
        typer.echo(f"Template: {template_path}")
        typer.echo(f"Delay:    {delay}s")
        if marker_list:
            typer.echo(f"Bypass markers: {', '.join(marker_list)}")
        typer.echo()

    try:
        if verbose:
            typer.echo("Extracting document structure...")

        doc = extract_document(str(input_file))

        if verbose:
            section_count = len(doc.sections)
            preamble_count = len(doc.preamble)
            typer.echo(f"Found {preamble_count} preamble paragraphs and {section_count} sections")
            typer.echo()
            typer.echo("Translating content...")

        translator = GoogleTranslatorWrapper(
            delay_between_calls=delay,
            bypass_markers=marker_list
        )

        translated_doc = translate_document(doc, translator, source, target)

        if verbose:
            typer.echo("Rebuilding document...")

        rebuild_document(translated_doc, str(output_file), template_path=str(template_path))

        typer.echo(f"Successfully translated: {output_file}")

    except FileNotFoundError as e:
        typer.echo(f"Error: File not found - {e}", err=True)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        if verbose:
            import traceback

            typer.echo(traceback.format_exc(), err=True)
        raise typer.Exit(code=1)


@app.command()
def info(
    input_file: Annotated[
        Path,
        typer.Argument(
            help="DOCX file to analyze",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
        ),
    ],
):
    """
    Show information about a DOCX document structure.

    Displays section count, paragraph count, and document metadata.
    """
    try:
        doc = extract_document(str(input_file))

        typer.echo(f"Document: {input_file}")
        typer.echo()
        typer.echo("Structure:")
        typer.echo(f"  Preamble paragraphs: {len(doc.preamble)}")
        typer.echo(f"  Sections: {len(doc.sections)}")

        total_paragraphs = len(doc.preamble)
        for section in doc.sections:
            total_paragraphs += len(section.body) + (1 if section.header else 0)
        typer.echo(f"  Total paragraphs: {total_paragraphs}")

        if doc.metadata:
            typer.echo()
            typer.echo("Metadata:")
            if doc.metadata.page_settings:
                ps = doc.metadata.page_settings
                typer.echo(f"  Page size: {ps.width_inches:.2f}\" x {ps.height_inches:.2f}\"")
            if doc.metadata.line_numbering:
                ln = doc.metadata.line_numbering
                typer.echo(f"  Line numbering: enabled (start={ln.start}, interval={ln.count_by})")

        if doc.sections:
            typer.echo()
            typer.echo("Sections:")
            for i, section in enumerate(doc.sections, 1):
                header_text = ""
                if section.header:
                    for element in section.header.elements:
                        if hasattr(element, "text"):
                            header_text += element.text
                header_preview = header_text[:50] + "..." if len(header_text) > 50 else header_text
                typer.echo(f"  {i}. {header_preview} ({len(section.body)} paragraphs)")

    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
