"""Command-line interface for HOLE Fonts"""

import logging
import sys
from pathlib import Path
from typing import List, Optional

import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich import print as rprint

from .config import get_config
from .converter import FontConverter
from .organizer import FontOrganizer
from .exporter import FontExporter
from .metadata import FontDatabase, FontAnalyzer
from .typekit import TypekitClient, TypekitEnricher
from .dedup import DuplicateDetector
from .search import FontSearch, SearchCriteria


console = Console()


def setup_logging(level: str = 'INFO'):
    """Setup logging configuration"""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('hole-fonts.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )


@click.group()
@click.option('--config', default='config.yaml', help='Path to configuration file')
@click.option('--log-level', default='INFO', help='Logging level')
@click.pass_context
def main(ctx, config: str, log_level: str):
    """HOLE Fonts - Font library management system"""
    ctx.ensure_object(dict)

    # Setup logging
    setup_logging(log_level)

    # Load configuration
    try:
        ctx.obj['config'] = get_config(config)
    except FileNotFoundError as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@main.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output directory')
@click.option('--formats', '-f', multiple=True, help='Formats to generate (ttf, otf, woff2)')
@click.option('--skip-existing/--overwrite', default=True, help='Skip existing fonts')
@click.pass_context
def convert(ctx, input_path: str, output: Optional[str], formats: tuple, skip_existing: bool):
    """
    Convert fonts to multiple formats and organize into library

    INPUT_PATH can be:
    - A single font file (.ttf, .otf, .woff, .woff2)
    - A directory containing font files
    """
    config = ctx.obj['config']
    input_path = Path(input_path)

    # Determine output directory
    output_dir = Path(output) if output else config.output_path

    # Get formats to generate
    output_formats = list(formats) if formats else config.formats

    console.print(Panel(
        f"[bold]Converting fonts[/bold]\n"
        f"Input: {input_path}\n"
        f"Output: {output_dir}\n"
        f"Formats: {', '.join(output_formats)}",
        title="HOLE Fonts Converter"
    ))

    # Initialize converter and organizer
    converter = FontConverter(output_dir)
    organizer = FontOrganizer(config.library_path)

    # Collect font files
    font_files = _collect_font_files(input_path)

    if not font_files:
        console.print("[yellow]No font files found![/yellow]")
        return

    console.print(f"\n[cyan]Found {len(font_files)} font file(s)[/cyan]\n")

    # Determine family name from input path if it's a directory
    family_name_override = None
    if input_path.is_dir():
        family_name_override = input_path.name

    # Process each font
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Processing fonts...", total=len(font_files))

        for font_file in font_files:
            progress.update(task, description=f"Converting {font_file.name}...")

            try:
                # Convert font
                converted = converter.convert(font_file, output_formats)

                # Check if variable font
                var_info = converted.pop('variable_font_info', None)

                # Organize into library (use folder name as family if from directory)
                family_path = organizer.organize_font(
                    converted,
                    family_name=family_name_override,
                    skip_existing=skip_existing
                )

                # Display result with variable font indicator
                if var_info:
                    axes_str = ", ".join([f"{ax['tag']}: {ax['min']}-{ax['max']}" for ax in var_info.axes])
                    console.print(f"[green]✓[/green] {font_file.name} → {family_path.name} [magenta]🎨 Variable[/magenta] ({axes_str})")
                else:
                    console.print(f"[green]✓[/green] {font_file.name} → {family_path.name}")

            except Exception as e:
                console.print(f"[red]✗[/red] {font_file.name}: {e}")
                logging.error(f"Failed to process {font_file.name}: {e}")

            progress.advance(task)

    console.print("\n[bold green]Conversion complete![/bold green]")


@main.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.option('--to', '-t', 'export_to', type=click.Path(), help='Export directory (for FontBase)')
@click.option('--structure', '-s', type=click.Choice(['flat-by-family', 'format-separated', 'single-flat']), default='flat-by-family', help='Export structure')
@click.option('--formats', '-f', multiple=True, help='Formats to generate (ttf, otf, woff2)')
@click.pass_context
def export(ctx, input_path: str, export_to: Optional[str], structure: str, formats: tuple):
    """
    Convert fonts and export to FontBase-friendly directory

    Simplified workflow: Convert → Export (no complex organization)

    INPUT_PATH can be:
    - A single font file
    - A directory with font files (uses directory name as family)
    - A directory of family directories (processes each separately)
    """
    config = ctx.obj['config']
    input_path = Path(input_path)

    # Determine export directory
    export_dir = Path(export_to) if export_to else Path(config.get('export.default_path', 'Export'))

    # Get formats to generate
    output_formats = list(formats) if formats else config.formats

    console.print(Panel(
        f"[bold]Exporting fonts for FontBase[/bold]\n"
        f"Input: {input_path}\n"
        f"Export to: {export_dir}\n"
        f"Structure: {structure}\n"
        f"Formats: {', '.join(output_formats)}",
        title="HOLE Fonts Exporter"
    ))

    # Initialize converter and exporter
    temp_dir = Path('Output')
    converter = FontConverter(temp_dir)
    exporter = FontExporter(export_dir, structure)

    # Check if input is directory of directories (batch mode)
    if input_path.is_dir():
        subdirs = [d for d in input_path.iterdir() if d.is_dir()]
        if subdirs:
            # Batch mode - process each subdirectory as a family
            console.print(f"\n[cyan]Found {len(subdirs)} font families[/cyan]\n")
            _export_batch(converter, exporter, subdirs, output_formats)
            return

    # Single family mode
    _export_family(converter, exporter, input_path, output_formats, None)

    console.print("\n[bold green]Export complete![/bold green]")
    console.print(f"\n[cyan]→ Add this folder to FontBase: {export_dir}[/cyan]")


def _export_batch(converter, exporter, family_dirs, output_formats):
    """Export multiple families in batch"""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Exporting families...", total=len(family_dirs))

        for family_dir in family_dirs:
            family_name = family_dir.name
            progress.update(task, description=f"Processing {family_name}...")

            try:
                _export_family(converter, exporter, family_dir, output_formats, family_name)
                console.print(f"[green]✓[/green] {family_name}")
            except Exception as e:
                console.print(f"[red]✗[/red] {family_name}: {e}")
                logging.error(f"Failed to export {family_name}: {e}")

            progress.advance(task)


def _export_family(converter, exporter, input_path, output_formats, family_name_override):
    """Export a single family"""
    # Collect font files
    font_files = _collect_font_files(input_path)

    if not font_files:
        return

    # Use folder name as family if directory
    family_name = family_name_override or (input_path.name if input_path.is_dir() else None)

    # Convert and collect results
    converted_by_font = {}

    for font_file in font_files:
        try:
            # Convert font
            converted = converter.convert(font_file, output_formats)

            # Remove variable font info from export dict
            var_info = converted.pop('variable_font_info', None)

            # Store converted files by base name
            base_name = font_file.stem
            converted_by_font[base_name] = converted

            # Log variable fonts
            if var_info:
                axes_str = ", ".join([f"{ax['tag']}: {ax['min']}-{ax['max']}" for ax in var_info.axes])
                logging.info(f"Variable font: {font_file.name} ({axes_str})")

        except Exception as e:
            logging.error(f"Failed to convert {font_file.name}: {e}")
            continue

    # Export to directory
    if converted_by_font:
        exporter.export_fonts(converted_by_font, family_name)


@main.command()
@click.pass_context
def list(ctx):
    """List all font families in library"""
    config = ctx.obj['config']
    organizer = FontOrganizer(config.library_path)

    families = organizer.list_families()

    if not families:
        console.print("[yellow]No fonts found in library[/yellow]")
        return

    table = Table(title="Font Library", show_header=True, header_style="bold magenta")
    table.add_column("Family", style="cyan")
    table.add_column("TTF", justify="center")
    table.add_column("OTF", justify="center")
    table.add_column("WOFF2", justify="center")

    for family in families:
        info = organizer.get_family_info(family)
        table.add_row(
            family,
            str(len(info.get('ttf', []))) if 'ttf' in info else "-",
            str(len(info.get('otf', []))) if 'otf' in info else "-",
            str(len(info.get('woff2', []))) if 'woff2' in info else "-",
        )

    console.print(table)
    console.print(f"\n[cyan]Total families: {len(families)}[/cyan]")


@main.command()
@click.argument('family_name')
@click.pass_context
def info(ctx, family_name: str):
    """Show detailed information about a font family"""
    config = ctx.obj['config']
    organizer = FontOrganizer(config.library_path)

    family_path = organizer.get_family_path(family_name)

    if not family_path:
        console.print(f"[red]Font family not found: {family_name}[/red]")
        return

    info = organizer.get_family_info(family_name)

    console.print(Panel(
        f"[bold]{family_name}[/bold]\n"
        f"Location: {family_path}",
        title="Font Family Information"
    ))

    for fmt in ['ttf', 'otf', 'woff2']:
        if fmt in info:
            console.print(f"\n[cyan]{fmt.upper()} files:[/cyan]")
            for file in info[fmt]:
                console.print(f"  • {file}")


@main.command()
@click.pass_context
def validate(ctx):
    """Validate library structure"""
    config = ctx.obj['config']
    organizer = FontOrganizer(config.library_path)

    console.print("[cyan]Validating library structure...[/cyan]\n")

    issues = organizer.validate_structure()

    # Check for issues
    has_issues = any(issues.values())

    if not has_issues:
        console.print("[bold green]✓ Library structure is valid![/bold green]")
        return

    # Report issues
    if issues['missing_formats']:
        console.print("[yellow]Missing formats:[/yellow]")
        for item in issues['missing_formats']:
            console.print(f"  • {item['family']}: missing {', '.join(item['missing'])}")

    if issues['empty_directories']:
        console.print("\n[yellow]Empty directories:[/yellow]")
        for directory in issues['empty_directories']:
            console.print(f"  • {directory}")

    if issues['invalid_files']:
        console.print("\n[red]Invalid files:[/red]")
        for file in issues['invalid_files']:
            console.print(f"  • {file}")


def _collect_font_files(path: Path) -> List[Path]:
    """
    Collect font files from path

    Args:
        path: File or directory path

    Returns:
        List of font file paths
    """
    if path.is_file():
        if path.suffix.lower() in {'.ttf', '.otf', '.woff', '.woff2'}:
            return [path]
        return []

    # Collect from directory
    font_files = []
    for pattern in ['*.ttf', '*.otf', '*.woff', '*.woff2']:
        font_files.extend(path.rglob(pattern))

    return font_files


# ============================================================================
# v0.2 Commands - Metadata, Search, and Deduplication
# ============================================================================

@main.command()
@click.argument('directory', type=click.Path(exists=True))
@click.option('--output', '-o', default='font-database.json', help='Database output file')
@click.pass_context
def scan(ctx, directory: str, output: str):
    """
    Scan font directory and build metadata database

    Creates searchable database of all fonts with metadata
    """
    directory = Path(directory)
    db_path = Path(output)

    console.print(Panel(
        f"[bold]Scanning Font Library[/bold]\n"
        f"Directory: {directory}\n"
        f"Database: {db_path}",
        title="HOLE Fonts Metadata Scanner"
    ))

    # Create database
    db = FontDatabase(db_path)

    console.print("\n[cyan]Scanning fonts...[/cyan]\n")

    # Scan directory
    count = db.scan_directory(directory)

    # Save database
    db.save()

    console.print(f"\n[green]✓ Scanned {count} fonts[/green]")
    console.print(f"[cyan]Database saved to: {db_path}[/cyan]\n")


@main.command()
@click.argument('database', type=click.Path(exists=True))
@click.option('--min-confidence', default=0.60, help='Minimum confidence threshold')
@click.option('--output', '-o', default='dedup-report.json', help='Report output file')
@click.pass_context
def dedup(ctx, database: str, min_confidence: float, output: str):
    """
    Find duplicate fonts in database

    Analyzes fonts and identifies duplicates with confidence scoring
    """
    db_path = Path(database)
    report_path = Path(output)

    console.print(Panel(
        f"[bold]Font Deduplication Analysis[/bold]\n"
        f"Database: {db_path}\n"
        f"Min Confidence: {min_confidence}\n"
        f"Report: {report_path}",
        title="HOLE Fonts Dedup"
    ))

    # Load database
    db = FontDatabase(db_path)
    db.load()

    console.print(f"\n[cyan]Loaded {len(db.fonts)} fonts[/cyan]\n")
    console.print("[cyan]Analyzing for duplicates...[/cyan]\n")

    # Find duplicates
    detector = DuplicateDetector(db)
    report = detector.find_duplicates(min_confidence)

    # Display results
    console.print(f"[green]✓ Analysis complete[/green]\n")

    table = Table(title="Deduplication Summary")
    table.add_column("Category", style="cyan")
    table.add_column("Count", justify="right", style="green")

    table.add_row("Total fonts", str(report.total_fonts))
    table.add_row("Exact duplicates", str(report.exact_duplicates))
    table.add_row("High confidence (>0.85)", str(report.high_confidence_dupes))
    table.add_row("Medium confidence (0.60-0.85)", str(report.medium_confidence_dupes))
    table.add_row("Low confidence (<0.60)", str(report.low_confidence_dupes))
    table.add_row("Potential savings", f"{report.potential_savings_mb:.1f} MB")

    console.print(table)

    # Save report
    import json
    with open(report_path, 'w') as f:
        json.dump({
            'summary': {
                'total_fonts': report.total_fonts,
                'exact_duplicates': report.exact_duplicates,
                'high_confidence': report.high_confidence_dupes,
                'medium_confidence': report.medium_confidence_dupes,
                'low_confidence': report.low_confidence_dupes,
                'potential_savings_mb': report.potential_savings_mb
            },
            'matches': [
                {
                    'primary': m.primary_font.filename,
                    'duplicate': m.duplicate_font.filename,
                    'confidence': m.confidence,
                    'reason': m.reason,
                    'can_auto_delete': m.can_auto_delete
                }
                for m in report.matches
            ]
        }, f, indent=2)

    console.print(f"\n[cyan]Report saved to: {report_path}[/cyan]\n")


@main.command()
@click.argument('database', type=click.Path(exists=True))
@click.option('--classification', help='Filter by classification (sans-serif, serif, etc.)')
@click.option('--designer', help='Filter by designer name')
@click.option('--foundry', help='Filter by foundry/manufacturer name')
@click.option('--variable', is_flag=True, help='Only variable fonts')
@click.option('--weight-min', type=int, help='Minimum weight')
@click.option('--weight-max', type=int, help='Maximum weight')
@click.option('--italic', is_flag=True, help='Only italic fonts')
@click.option('--format', type=click.Choice(['ttf', 'otf', 'woff2']), help='Filter by format')
@click.option('--has-axis', help='Must have specific axis (wght, wdth, slnt, etc.)')
@click.pass_context
def search(ctx, database: str, **kwargs):
    """
    Search fonts by criteria

    Example: hole-fonts search db.json --designer "Adrian Frutiger"
    Example: hole-fonts search db.json --foundry "Monotype" --classification sans-serif
    """
    db_path = Path(database)

    # Load database
    db = FontDatabase(db_path)
    db.load()

    console.print(f"[cyan]Searching {len(db.fonts)} fonts...[/cyan]\n")

    # Build criteria
    criteria = SearchCriteria(
        classification=kwargs.get('classification'),
        designer=kwargs.get('designer'),
        foundry=kwargs.get('foundry'),
        weight_min=kwargs.get('weight_min'),
        weight_max=kwargs.get('weight_max'),
        italic=kwargs.get('italic'),
        variable=kwargs.get('variable'),
        has_axis=kwargs.get('has_axis'),
        format=kwargs.get('format')
    )

    # Search
    searcher = FontSearch(db, {})
    results = searcher.search(criteria)

    # Display results
    if not results:
        console.print("[yellow]No fonts found matching criteria[/yellow]\n")
        return

    console.print(f"[green]Found {len(results)} matching fonts:[/green]\n")

    # Group by family
    families = searcher.group_by_family(results)

    for family, fonts in sorted(families.items()):
        console.print(f"[cyan]{family}[/cyan] ({len(fonts)} fonts)")
        for font in fonts[:5]:  # Show first 5
            var_indicator = "🎨" if font.is_variable else ""
            console.print(f"  • {font.filename} {var_indicator}")
        if len(fonts) > 5:
            console.print(f"  ... and {len(fonts) - 5} more")
        console.print()


@main.command()
@click.argument('database', type=click.Path(exists=True))
@click.option('--typekit-key', required=True, help='Adobe Typekit API key')
@click.option('--output', '-o', default='enriched-database.json', help='Output file')
@click.pass_context
def enrich(ctx, database: str, typekit_key: str, output: str):
    """
    Enrich font metadata with Adobe Typekit data

    Queries Typekit API to add designer, foundry, classifications
    """
    db_path = Path(database)
    output_path = Path(output)

    console.print(Panel(
        f"[bold]Enriching Font Metadata[/bold]\n"
        f"Database: {db_path}\n"
        f"Output: {output_path}",
        title="HOLE Fonts Typekit Enrichment"
    ))

    # Load database
    db = FontDatabase(db_path)
    db.load()

    console.print(f"\n[cyan]Loaded {len(db.fonts)} fonts[/cyan]\n")

    # Create Typekit client
    client = TypekitClient(typekit_key)
    enricher = TypekitEnricher(client)

    console.print("[cyan]Querying Typekit API...[/cyan]\n")

    # Enrich fonts
    def progress_callback(current, total):
        console.print(f"  Progress: {current}/{total} fonts...", end='\r')

    enrichments = enricher.batch_enrich(
        list(db.fonts.values()),
        progress_callback=progress_callback
    )

    console.print(f"\n[green]✓ Enriched {len(enrichments)} fonts with Typekit data[/green]\n")

    # Save enriched database
    import json
    with open(output_path, 'w') as f:
        json.dump({
            'version': '0.2.0',
            'total_fonts': len(db.fonts),
            'enriched_count': len(enrichments),
            'fonts': [meta.to_dict() for meta in db.fonts.values()],
            'enrichments': enrichments
        }, f, indent=2)

    console.print(f"[cyan]Enriched database saved to: {output_path}[/cyan]\n")


if __name__ == '__main__':
    main()
