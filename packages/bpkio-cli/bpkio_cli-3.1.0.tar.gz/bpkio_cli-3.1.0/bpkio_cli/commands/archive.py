from pathlib import Path, PosixPath
from typing import Optional

import click
import cloup
from media_muncher.handlers.dash import DASHHandler
from pydantic import FilePath, TypeAdapter
from rich.console import Console, Group
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.text import Text
from trace_shrink import Format, Trace, open_trace

import bpkio_cli.click_options as bic_options
from bpkio_cli.click_mods.resource_commands import ARG_TO_IGNORE, ResourceGroup
from bpkio_cli.click_options.archive import (
    archive_annotate_option,
    archive_format_option,
)
from bpkio_cli.core.app_context import AppContext
from bpkio_cli.core.exceptions import BroadpeakIoCliError
from bpkio_cli.core.models import Archive
from bpkio_cli.core.output_store import OutputStore
from bpkio_cli.display.display_mode import DisplayMode
from bpkio_cli.plot.plot_hls_sequence import extract_hls_data, plot_hls_metrics
from bpkio_cli.plot.plot_mpd_sequence import extract_mpd_data, plot_mpd_metrics
from bpkio_cli.plot.plot_utils import save_plot_with_crosshair
from bpkio_cli.plot.plotly_timelines import MpdTimelinePlotter, SubplotInfo
from bpkio_cli.utils import prompt
from bpkio_cli.utils.archive import (
    annotate_entries,
    create_handler_from_entry,
    export_entries,
    get_format_extension,
    normalize_format,
)
from bpkio_cli.utils.file_utils import count_files_in_directory, format_file_size
from bpkio_cli.writers.breadcrumbs import (
    display_error,
    display_info,
    display_ok,
    display_tip,
)
from bpkio_cli.writers.colorizer import Colorizer as CL
from bpkio_cli.writers.content_display import display_content

console = Console()


# === HELPER FUNCTIONS ===


def _get_archive_path(obj: AppContext) -> Optional[Archive]:
    """Get the archive path from the resource chain or cache.

    Returns:
        Archive object representing the archive file or directory, or None if not found
    """
    # First check current_resource (most recent resource in chain)
    current = obj.current_resource
    if isinstance(current, Archive):
        return current
    elif isinstance(current, str) and (
        current.endswith((".har", ".json")) or "/" in current or "\\" in current
    ):
        # Normalize and check if path exists (file or directory)
        current_path = Path(current).expanduser().resolve()
        if current_path.exists():
            return Archive(path=PosixPath(current_path))

    # Check cache for Archive objects (most recent first)
    # This will find both explicitly provided paths and paths saved from --save operations
    # Uses the same pattern as other resources (e.g., in resource_commands.py)
    if obj.cache:
        cached_path = obj.cache.last_by_type(Archive)
        if cached_path:
            return cached_path

    return None


def _get_archive(obj: AppContext) -> Trace:
    """Get the Trace instance from the resource chain."""
    archive_path_obj = _get_archive_path(obj)

    if not archive_path_obj:
        raise BroadpeakIoCliError(
            "No archive file or directory specified in resource chain"
        )

    # Convert Archive to string for open_trace
    archive_path = str(archive_path_obj.path)
    path = archive_path_obj.path

    # Build progress message with size/count information
    if path.is_file():
        try:
            file_size = path.stat().st_size
            size_str = format_file_size(file_size)
            progress_msg = f"Loading archive: {path.name} ({size_str})"
        except (OSError, PermissionError):
            progress_msg = f"Loading archive: {path.name}"
    elif path.is_dir():
        try:
            file_count = count_files_in_directory(path)
            progress_msg = f"Loading archive: {path.name} ({file_count} files)"
        except (OSError, PermissionError):
            progress_msg = f"Loading archive: {path.name}"
    else:
        progress_msg = f"Loading archive: {path.name}"

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            progress.add_task(progress_msg, total=None)
            trace = open_trace(archive_path)
            trace.abr_detector.ignore_query_params("bk-ml")
        return trace
    except Exception as e:
        raise BroadpeakIoCliError(f"Could not load archive: {e}")


def _get_entry_by_id(archive: Trace, request_id: str):
    """Get an entry from the archive by its ID."""
    try:
        entry = archive.get_entry_by_id(request_id)
        if entry is None:
            raise BroadpeakIoCliError(
                f"Request with ID '{request_id}' not found in archive"
            )
        return entry
    except BroadpeakIoCliError:
        raise
    except Exception as e:
        raise BroadpeakIoCliError(
            f"Request with ID '{request_id}' not found in archive: {e}"
        )


def _get_prev_next_entry_id(
    archive: Trace, current_request_id: str, direction: str
) -> str:
    """Get the previous or next entry ID in the manifest sequence.

    Args:
        archive: The archive reader
        current_request_id: The current request ID
        direction: Either 'prev' or 'next'

    Returns:
        The ID of the previous or next entry

    Raises:
        BroadpeakIoCliError: If no prev/next entry is found
    """
    # Get the current entry
    current_entry = _get_entry_by_id(archive, current_request_id)

    # Get the URL of the current entry
    from yarl import URL

    current_url = URL(str(current_entry.request.url))

    # Get all entries for this URL (manifest sequence)
    entries = archive.get_entries_for_url(current_url)

    if not entries:
        raise BroadpeakIoCliError(f"No entries found for manifest URL: {current_url}")

    # Find the current entry in the list
    current_index = None
    for i, entry in enumerate(entries):
        if entry.id == current_request_id:
            current_index = i
            break

    if current_index is None:
        raise BroadpeakIoCliError(
            f"Current request ID '{current_request_id}' not found in manifest sequence"
        )

    # Get the prev/next index
    if direction == "prev":
        target_index = current_index - 1
        if target_index < 0:
            raise BroadpeakIoCliError(
                "Already at the first entry in the manifest sequence"
            )
    else:  # next
        target_index = current_index + 1
        if target_index >= len(entries):
            raise BroadpeakIoCliError(
                "Already at the last entry in the manifest sequence"
            )

    return entries[target_index].id


# === GROUP: Archive ===
@cloup.group(
    cls=ResourceGroup,
    help="Explore archive files, such as HAR captures",
    resource_type=Archive,
    aliases=["trace"],
)
@cloup.argument(
    "archive_path",
    help=("The local file or directory to work with"),
    metavar="<archive-file-or-directory>",
)
@click.pass_obj
def archive(obj: AppContext, archive_path: str):
    if archive_path and archive_path != ARG_TO_IGNORE:
        archive_path_obj = None

        if archive_path == "$":
            # Get from current_resource - could be Archive or string
            current = obj.current_resource
            if isinstance(current, Archive):
                # Already an Archive, use it directly
                archive_path_obj = current
                archive_path = str(current.path)
            else:
                archive_path = str(current)

        # If we don't already have an Archive, create one
        if archive_path_obj is None:
            # Normalize the path to handle any expansion/normalization issues
            normalized_path = Path(archive_path).expanduser().resolve()

            # Check if path is a directory (multifile archive) or a file
            if normalized_path.is_dir():
                # Directory: treat as multifile archive, store as Archive
                archive_path_obj = Archive(path=PosixPath(normalized_path))
            else:
                # File: validate as FilePath, then wrap in Archive
                # If validation fails, check if it's actually a directory (path might need normalization)
                try:
                    validated_path = TypeAdapter(FilePath).validate_python(
                        str(normalized_path)
                    )
                    archive_path_obj = Archive(path=validated_path)
                except Exception:
                    # If FilePath validation fails, check if it's a directory
                    if normalized_path.is_dir():
                        archive_path_obj = Archive(path=PosixPath(normalized_path))
                    else:
                        # Re-raise the original validation error
                        raise

        obj.resource_chain.add_resource(archive_path, archive_path_obj)
        obj.cache.record(archive_path_obj)
    elif archive_path == ARG_TO_IGNORE:
        # No argument provided: check if there's already an archive path in cache or resource chain
        existing_path = _get_archive_path(obj)
        if existing_path:
            # Archive path already available, nothing to do
            pass
        # If no existing path found, subcommands will handle the error via _get_archive()


# --- VAR Command (save archive path to a named variable)
@archive.command(
    aliases=["alias", "save-as"],
    help="Save this archive path as a named variable for later use",
)
@cloup.argument("name", help="Name of the variable (used with @name syntax)")
@click.pass_obj
def archive_var(obj: AppContext, name: str):
    """Save the current archive path to a named variable."""
    archive_path = obj.resource_chain.last_key()

    metadata = {"type": "path", "resource_type": "archive"}
    obj.cache.set_variable(name, str(archive_path), metadata)
    click.secho(f"✓ Saved archive path as '@{name}'", fg="green")


# --- INFO Command (display archive information)
@archive.command(
    help="Display essential information about the archive",
    name="info",
)
@click.pass_obj
def archive_info(obj: AppContext):
    """Display essential information about the archive, including number of entries and manifest URLs."""
    archive_trace = _get_archive(obj)

    # Get archive format and path from Trace metadata
    archive_format = archive_trace.format or "unknown"
    archive_path = archive_trace.path

    # Get total number of entries
    entries = archive_trace.entries
    total_entries = len(entries)

    # Get manifest URLs
    dash_urls = archive_trace.get_abr_manifest_urls(format=Format.DASH)
    hls_urls = archive_trace.get_abr_manifest_urls(format=Format.HLS)

    # Build information text with consistent alignment
    info_texts = []

    # Archive path - use fixed width for alignment
    path_label = "Path:"
    if archive_path:
        info_texts.append(
            Text.from_markup(
                f"[bold]{path_label:<15}[/bold] [cyan]{archive_path}[/cyan]"
            )
        )
    else:
        info_texts.append(
            Text.from_markup(f"[bold]{path_label:<15}[/bold] [yellow]unknown[/yellow]")
        )

    # Format
    format_label = "Format:"
    info_texts.append(
        Text.from_markup(
            f"[bold]{format_label:<15}[/bold] [cyan]{archive_format}[/cyan]"
        )
    )

    # Total entries
    entries_label = "Total entries:"
    info_texts.append(
        Text.from_markup(
            f"[bold]{entries_label:<15}[/bold] [cyan]{total_entries}[/cyan]"
        )
    )

    # DASH manifests table
    if dash_urls:
        info_texts.append(Text(""))  # Empty line for spacing
        info_texts.append(
            Text.from_markup(
                f"[bold green]DASH Manifests ({len(dash_urls)}):[/bold green]"
            )
        )
        dash_table = Table(
            show_header=True,
            header_style="bold green",
            border_style="dim",
            show_edge=True,
        )
        dash_table.add_column("#", style="dim white", width=4, justify="right")
        dash_table.add_column("URL", style="white", overflow="fold")
        for idx, dash_url in enumerate(dash_urls, 1):
            dash_table.add_row(str(idx), str(dash_url.url))
        info_texts.append(dash_table)
    else:
        info_texts.append(Text(""))  # Empty line for spacing
        info_texts.append(Text.from_markup("[dim]DASH Manifests: None[/dim]"))

    # HLS manifests table
    if hls_urls:
        info_texts.append(Text(""))  # Empty line for spacing
        info_texts.append(
            Text.from_markup(
                f"[bold green]HLS Manifests ({len(hls_urls)}):[/bold green]"
            )
        )
        hls_table = Table(
            show_header=True,
            header_style="bold green",
            border_style="dim",
            show_edge=True,
        )
        hls_table.add_column("#", style="dim white", width=4, justify="right")
        hls_table.add_column("URL", style="white", overflow="fold")
        for idx, hls_url in enumerate(hls_urls, 1):
            hls_table.add_row(str(idx), str(hls_url.url))
        info_texts.append(hls_table)
    else:
        info_texts.append(Text(""))  # Empty line for spacing
        info_texts.append(Text.from_markup("[dim]HLS Manifests: None[/dim]"))

    # Display information in a panel
    info_panel = Panel(
        Group(*info_texts),
        title="Archive Information",
        expand=False,
        border_style="blue",
        title_align="left",
    )
    console.print()
    console.print(info_panel)
    console.print()


# --- PLOT Command (archive-level) - Unified DASH/HLS Plotting
@archive.command(
    help="Plot ABR manifest sequence metrics over time from the archive", name="plot"
)
@cloup.option_group(
    "Common options",
    click.option(
        "--open/--no-open",
        "open_browser",
        is_flag=True,
        default=True,
        help="Show/Hide opening the plot in the browser",
    ),
    click.option(
        "--segments/--no-segments",
        "show_segments",
        is_flag=True,
        default=True,
        help="Show/Hide individual segment dots in the Segment Range / Period Segments plot",
    ),
)
@cloup.option_group(
    "DASH-specific options",
    click.option(
        "--pubt/--no-pubt",
        "show_publish_time",
        is_flag=True,
        default=True,
        help="[DASH] Show/Hide MPD Publish Time plot",
    ),
    click.option(
        "--ast/--no-ast",
        "show_availability_start_time",
        is_flag=True,
        default=True,
        help="[DASH] Show/Hide MPD Availability Start Time plot",
    ),
    click.option(
        "--pstart/--no-pstart",
        "show_period_starts",
        is_flag=True,
        default=True,
        help="[DASH] Show/Hide Period Start Time plot",
    ),
)
@cloup.option_group(
    "HLS-specific options",
    click.option(
        "--ms/--no-ms",
        "show_media_sequence",
        is_flag=True,
        default=True,
        help="[HLS] Show/Hide Media Sequence plot",
    ),
    click.option(
        "--ds/--no-ds",
        "show_discontinuity_sequence",
        is_flag=True,
        default=True,
        help="[HLS] Show/Hide Discontinuity Sequence plot",
    ),
)
@bic_options.save
@click.pass_obj
def plot(
    obj: AppContext,
    # Common options
    open_browser: bool = True,
    show_segments: bool = True,
    # DASH-specific options
    show_publish_time: bool = True,
    show_availability_start_time: bool = True,
    show_period_starts: bool = True,
    # HLS-specific options
    show_media_sequence: bool = True,
    show_discontinuity_sequence: bool = True,
    # Save option
    output_directory: Optional[str] = None,
    **kwargs,
):
    """Plot ABR manifest sequence metrics over time from the archive.

    This command finds all DASH and HLS manifest URLs in the archive and prompts
    the user to select one if multiple are found. It then extracts and plots the
    appropriate metrics based on the manifest format.
    """
    archive_trace = _get_archive(obj)

    # Get all ABR manifest URLs
    dash_urls = archive_trace.get_abr_manifest_urls(format=Format.DASH)
    hls_urls = archive_trace.get_abr_manifest_urls(format=Format.HLS)

    # Build selection choices
    choices = []
    manifest_info = {}  # Maps choice value to (format, url_or_domain)

    # Add DASH manifests
    for dash_url in dash_urls:
        url_str = str(dash_url.url)
        choice_value = f"dash:{url_str}"
        choices.append(
            dict(
                value=choice_value,
                name=f"[DASH] {dash_url.url}",
            )
        )
        manifest_info[choice_value] = ("dash", url_str)

    # Group HLS URLs by domain
    hls_domains = {}
    for hls_url in hls_urls:
        domain = hls_url.url.host
        if domain not in hls_domains:
            hls_domains[domain] = []
        hls_domains[domain].append(hls_url.url)

    # Add HLS domains
    for domain, urls in hls_domains.items():
        choice_value = f"hls:{domain}"
        choices.append(
            dict(
                value=choice_value,
                name=f"[HLS] {domain} ({len(urls)} playlist{'s' if len(urls) != 1 else ''})",
            )
        )
        manifest_info[choice_value] = ("hls", domain)

    if not choices:
        display_error("No ABR manifest URLs found in the archive")
        return

    # Select manifest
    selected_choice = None
    if len(choices) == 1:
        selected_choice = choices[0]["value"]
        display_info(f"Found 1 manifest: {choices[0]['name']}")
    else:
        display_info(f"Found {len(choices)} manifest(s). Please select one:")
        selected_choice = prompt.fuzzy(
            message="Select a manifest to plot",
            choices=choices,
        )

    if not selected_choice:
        display_error("No manifest selected")
        return

    # Extract format and identifier
    format_type, identifier = manifest_info[selected_choice]

    # Route to appropriate plotting function
    if format_type == "dash":
        _plot_dash(
            archive_trace,
            identifier,
            show_segments,
            show_publish_time,
            show_availability_start_time,
            show_period_starts,
            open_browser,
            output_directory,
        )
    elif format_type == "hls":
        _plot_hls(
            archive_trace,
            identifier,
            hls_domains,
            show_segments,
            show_media_sequence,
            show_discontinuity_sequence,
            open_browser,
            output_directory,
        )


def _plot_dash(
    archive_trace: Trace,
    manifest_url: str,
    show_segments: bool,
    show_publish_time: bool,
    show_availability_start_time: bool,
    show_period_starts: bool,
    open_browser: bool,
    output_directory: Optional[str],
):
    """Plot DASH manifest metrics."""
    # Extract MPD data
    display_info(f"Extracting MPD data from manifest: {manifest_url}")
    data_points, first_mpd_url = extract_mpd_data(
        archive_trace,
        manifest_url,
        show_segments=show_segments,
    )

    if not data_points:
        display_error(f"No MPD entries found for manifest: {manifest_url}")
        return

    display_info(f"Found {len(data_points)} MPD entries")
    display_info("Generating plot...")

    # Generate plot
    fig = plot_mpd_metrics(
        data_points,
        first_mpd_url=first_mpd_url,
        service_id=first_mpd_url.query.get("bpkio_serviceid")
        if first_mpd_url
        else None,
        session_id=first_mpd_url.query.get("bpkio_sessionid")
        if first_mpd_url
        else None,
        domain=first_mpd_url.host if first_mpd_url else None,
        path=first_mpd_url.path if first_mpd_url else None,
        show_segments=show_segments,
        show_publish_time=show_publish_time,
        show_availability_start_time=show_availability_start_time,
        show_period_starts=show_period_starts,
    )

    if fig is None:
        display_error("Failed to generate plot")
        return

    # Save plot
    if output_directory is None:
        output_directory = "."

    output_store = OutputStore(output_directory)
    output_store.path(ensure=True)

    filename = "mpd_sequence_plot.html"
    output_path = output_store.path(ensure=True) / filename

    output_file = save_plot_with_crosshair(fig, output_path)
    display_ok(f"Plot saved to: {output_file}")

    if open_browser:
        click.launch("file://" + str(output_file))


def _plot_hls(
    archive_trace: Trace,
    selected_domain: str,
    domains: dict,
    show_segments: bool,
    show_media_sequence: bool,
    show_discontinuity_sequence: bool,
    open_browser: bool,
    output_directory: Optional[str],
):
    """Plot HLS manifest metrics."""
    # Extract HLS data
    playlist_count = len(domains[selected_domain])
    display_info(f"Extracting HLS data from domain: {selected_domain}")
    display_info(f"Found {playlist_count} HLS playlist(s) from this domain")

    data_by_playlist, master_variant_info = extract_hls_data(
        archive_trace,
        selected_domain,
        deduplicate=False,
    )

    if not data_by_playlist:
        display_error(f"No HLS playlist entries found for domain: {selected_domain}")
        return

    # Calculate total data points
    total_data_points = sum(
        len(playlist_data["data_points"]) for playlist_data in data_by_playlist.values()
    )
    display_info(
        f"Found {len(data_by_playlist)} playlist(s) with {total_data_points} total entries"
    )
    display_info("Generating plot...")

    # Get first HLS URL from selected domain for subtitle
    first_hls_url = domains[selected_domain][0] if selected_domain in domains else None

    # Generate plot
    fig = plot_hls_metrics(
        data_by_playlist,
        first_hls_url=first_hls_url,
        service_id=first_hls_url.query.get("bpkio_serviceid")
        if first_hls_url
        else None,
        session_id=first_hls_url.query.get("bpkio_sessionid")
        if first_hls_url
        else None,
        domain=first_hls_url.host if first_hls_url else None,
        path=first_hls_url.path if first_hls_url else None,
        master_variant_info=master_variant_info,
        show_segments=show_segments,
        show_media_sequence=show_media_sequence,
        show_discontinuity_sequence=show_discontinuity_sequence,
        show_segment_spans=True,
    )

    if fig is None:
        display_error("Failed to generate plot")
        return

    # Save plot
    if output_directory is None:
        output_directory = "."

    output_store = OutputStore(output_directory)
    output_store.path(ensure=True)

    filename = "hls_sequence_plot.html"
    output_path = output_store.path(ensure=True) / filename

    output_file = save_plot_with_crosshair(fig, output_path)
    display_ok(f"Plot saved to: {output_file}")

    if open_browser:
        click.launch("file://" + str(output_file))


# --- ANNOTATE Command (archive-level)
@archive.command(
    help="Annotate all entries in the archive and save to a new file",
    name="annotate",
)
@archive_format_option()
@click.option(
    "--output",
    "-o",
    help="Output file path. If not specified, will be generated based on input filename",
)
@click.option(
    "--inline/--no-inline",
    "inline",
    is_flag=True,
    default=True,
    help="Insert annotations inline in the body content (default: True). Use --no-inline to keep original body unchanged.",
)
@bic_options.save
@click.pass_obj
def annotate_archive(
    obj: AppContext,
    format: str,
    output: Optional[str] = None,
    inline: bool = True,
    output_directory: Optional[str] = None,
    **kwargs,
):
    """Annotate all entries in the archive and save to a new file.

    This command iterates through all entries in the archive, annotates manifest
    content with parsed metadata (adds comments to HLS/DASH files), and exports
    the annotated entries to a new archive file.
    """
    # Normalize format (proxyman -> proxymanlogv2)
    format = normalize_format(format)

    archive_trace = _get_archive(obj)

    # Get all entries from the archive
    entries = archive_trace.entries

    if not entries:
        display_error("No entries found in the archive")
        return

    display_info(f"Found {len(entries)} entries to annotate")

    # Annotate entries
    annotate_entries(
        entries,
        inline=inline,
        progress_message="Annotating entries...",
        display_info_func=display_info,
    )

    # Determine output file path
    if output_directory is None:
        output_directory = "."

    output_store = OutputStore(output_directory)
    output_store.path(ensure=True)

    if output is None:
        # Generate filename from input archive path
        archive_path_obj = _get_archive_path(obj)

        if archive_path_obj:
            archive_path = archive_path_obj.to_posix_path()
            if archive_path.is_dir():
                # For directories, use the directory name as the base name
                base_name = archive_path.name
            else:
                base_name = archive_path.stem
        else:
            base_name = "archive"
        extension = get_format_extension(format)
        output = f"{base_name}_annotated{extension}"

    output_path = output_store.path(ensure=True) / output

    # Export entries using trace-shrink Exporter
    try:
        display_info(f"Exporting {len(entries)} entries to {output_path}...")
        export_entries(entries, output_path, format)
        display_ok(
            f"Successfully exported {len(entries)} annotated entries to: {output_path}"
        )

    except Exception as e:
        display_error(f"Failed to export entries: {e}")
        raise BroadpeakIoCliError(f"Export failed: {e}") from e


# --- CONVERT Command (archive-level)
@archive.command(
    help="Convert an archive file from one format to another",
    name="convert",
)
@archive_format_option(required=True)
@click.option(
    "--output",
    "-o",
    help="Output file path. If not specified, will be generated based on input filename",
)
@bic_options.save
@click.pass_obj
def convert_archive(
    obj: AppContext,
    format: str,
    output: Optional[str] = None,
    output_directory: Optional[str] = None,
    **kwargs,
):
    """Convert an archive file from one format to another.

    This command reads all entries from the archive and exports them to a new
    archive file in the specified format. The output filename will use the same
    basename as the input file with the appropriate extension for the output format.
    """
    # Normalize format (proxyman -> proxymanlogv2)
    format = normalize_format(format)

    archive_trace = _get_archive(obj)

    # Get input format from Trace metadata
    input_format = archive_trace.format

    if not input_format:
        raise BroadpeakIoCliError("Could not determine archive format from trace")

    # Check if conversion is needed
    if input_format == format:
        display_info(f"Archive is already in {format} format. No conversion needed.")
        return

    # Get all entries from the archive
    entries = archive_trace.entries

    if not entries:
        display_error("No entries found in the archive")
        return

    display_info(f"Found {len(entries)} entries to convert")

    # Determine output file path
    if output_directory is None:
        output_directory = "."

    output_store = OutputStore(output_directory)
    output_store.path(ensure=True)

    if output is None:
        # Generate filename from input archive path with same basename
        archive_path_str = archive_trace.path or "archive"
        archive_path_obj = Path(archive_path_str)
        if archive_path_obj.is_dir():
            # For directories, use the directory name as the base name
            base_name = archive_path_obj.name
        else:
            base_name = archive_path_obj.stem
        # Map format to extension
        extension = get_format_extension(format)
        output = f"{base_name}{extension}"

    output_path = output_store.path(ensure=True) / output

    # Export entries using trace-shrink Exporter
    try:
        display_info(
            f"Converting {len(entries)} entries from {input_format} to {format}..."
        )
        display_info(f"Exporting to {output_path}...")
        export_entries(entries, output_path, format)

        display_ok(
            f"Successfully converted {len(entries)} entries from {input_format} to {format}: {output_path}"
        )

    except Exception as e:
        display_error(f"Failed to convert entries: {e}")
        raise BroadpeakIoCliError(f"Conversion failed: {e}") from e


# --- PLUCK Command (archive-level)
@archive.command(
    help="Extract entries related to a playlist and export them to a new archive file",
    name="prune",
)
@bic_options.archive()
@click.option(
    "--output",
    "-o",
    help="Output file path. If not specified, will be generated based on manifest URL",
)
@bic_options.save
@click.pass_obj
def prune(
    obj: AppContext,
    format: str,
    output: Optional[str] = None,
    annotate: bool = False,
    output_directory: Optional[str] = None,
    **kwargs,
):
    """Extract entries related to a playlist and export them to a new archive file.

    This command finds all manifest URLs (DASH or HLS) in the archive and prompts the user
    to select one if multiple manifests are found. It then extracts all entries related
    to that manifest and exports them to a new .har or .proxymanlogv2 file.
    Note: "proxyman" can be used as an alias for "proxymanlogv2".
    """
    # Normalize format (proxyman -> proxymanlogv2)
    format = normalize_format(format)

    archive_trace = _get_archive(obj)

    # Get all manifest URLs (both DASH and HLS)
    dash_urls = archive_trace.get_abr_manifest_urls(format=Format.DASH)
    hls_urls = archive_trace.get_abr_manifest_urls(format=Format.HLS)

    all_manifests = []
    if dash_urls:
        all_manifests.extend([(str(url.url), "DASH") for url in dash_urls])
    if hls_urls:
        all_manifests.extend([(str(url.url), "HLS") for url in hls_urls])

    if not all_manifests:
        display_error("No manifest URLs found in the archive")
        return

    # If multiple manifests, prompt user to select one
    manifest_url = None
    if len(all_manifests) == 1:
        manifest_url = all_manifests[0][0]
        display_info(f"Found 1 manifest: {manifest_url}")
    else:
        display_info(f"Found {len(all_manifests)} manifests. Please select one:")
        choices = [
            dict(value=url, name=f"{format_type}: {url}")
            for url, format_type in all_manifests
        ]
        manifest_url = prompt.fuzzy(
            message="Select a manifest URL to prune",
            choices=choices,
        )

    if not manifest_url:
        display_error("No manifest URL selected")
        return

    # Extract entries related to this manifest
    from yarl import URL

    display_info(f"Extracting entries for manifest: {manifest_url}")
    target_url = URL(manifest_url)
    entries = archive_trace.get_entries_for_url(target_url)

    if not entries:
        display_error(f"No entries found for manifest: {manifest_url}")
        return

    display_info(f"Found {len(entries)} entries to export")

    # Determine output file path
    if output_directory is None:
        output_directory = "."

    output_store = OutputStore(output_directory, bundle=False)

    if output is None:
        # Generate filename from manifest URL
        from urllib.parse import urlparse

        parsed = urlparse(manifest_url)
        path_parts = [p for p in parsed.path.split("/") if p]
        if path_parts:
            base_name = path_parts[-1].split(".")[0] or "manifest"
        else:
            base_name = "manifest"
        extension = get_format_extension(format)
        output = f"{base_name}_pruned{extension}"

    output_path = output_store.path(ensure=True) / output

    # Annotate entries if requested
    if annotate:
        inline = kwargs.get("inline", True)
        annotate_entries(
            entries,
            inline=inline,
            progress_message="Annotating manifest content...",
            display_info_func=display_info,
        )

    # Export entries using trace-shrink Exporter
    try:
        display_info(f"Exporting {len(entries)} entries to {output_path}...")
        export_entries(entries, output_path, format)
        display_ok(f"Successfully exported {len(entries)} entries to: {output_path}")

    except Exception as e:
        display_error(f"Failed to export entries: {e}")
        raise BroadpeakIoCliError(f"Export failed: {e}") from e


# === GROUP: Request ===
@archive.group(
    cls=ResourceGroup,
    aliases=["req"],
    help="Work with a specific request from the archive",
    resource_type=str,
    resource_id_type=str,
)
@cloup.argument(
    "request_id",
    help="The ID of the request to work with",
    metavar="<request-id>",
)
@click.pass_obj
def request(obj: AppContext, request_id: str):
    if request_id and request_id != ARG_TO_IGNORE:
        if request_id == "$":
            request_id = obj.current_resource

        # Pre-compute archive, entry, and handler for subcommands
        archive_trace = _get_archive(obj)

        # Get archive path from resource chain for metadata storage
        archive_path_obj = _get_archive_path(obj)
        archive_path = archive_path_obj.id if archive_path_obj else None

        # Handle prev/next navigation
        if request_id in ["prev", "next"]:
            # Get the last accessed request_id from metadata
            last_request_ids = obj.cache.get_metadata(archive_path, "last_request_id")

            if not last_request_ids:
                raise BroadpeakIoCliError(
                    f"No previous request found. Please access a request first before using '{request_id}'."
                )

            last_request_id = last_request_ids[0]

            # Get the prev/next entry ID
            try:
                request_id = _get_prev_next_entry_id(
                    archive_trace, last_request_id, request_id
                )
                display_tip(f"Navigated to request ID: {request_id}")
            except BroadpeakIoCliError as e:
                raise e

        entry = _get_entry_by_id(archive_trace, request_id)
        handler = create_handler_from_entry(entry)

        # Store entry in resource chain (so obj.current_resource returns the entry)
        obj.resource_chain.add_resource(request_id, entry)
        obj.cache.record(request_id)

        # Store the request_id as metadata for prev/next navigation
        obj.cache.record_metadata(archive_path, "last_request_id", request_id)

        # Store handler for subcommands to access
        obj.archive_handler = handler


# --- VAR Command (save request ID to a named variable)
@request.command(
    name="var",
    aliases=["alias", "save-as"],
    help="Save this request ID as a named variable for later use",
)
@cloup.argument("name", help="Name of the variable (used with @name syntax)")
@click.pass_obj
def request_var(obj: AppContext, name: str):
    """Save the current request ID to a named variable."""
    request_id = obj.resource_chain.last_key()

    metadata = {"type": "id", "resource_type": "archive-request"}
    obj.cache.set_variable(name, str(request_id), metadata)
    click.secho(f"✓ Saved request ID '{request_id}' as '@{name}'", fg="green")


# --- READ Command
@request.command(
    help="Load and display the content of a request from the archive",
    aliases=["content"],
)
@bic_options.display_mode
@bic_options.read
@bic_options.save
@bic_options.dash
@click.pass_obj
def read(
    obj: AppContext,
    display_mode: DisplayMode,
    top: int,
    tail: int,
    trim: int,
    ad_pattern: str,
    pager: bool,
    output_directory: Optional[str] = None,
    **kwargs,
):
    handler = obj.archive_handler

    display_content(
        handler=handler,
        max=1,
        interval=0,
        display_mode=display_mode,
        top=top,
        tail=tail,
        trim=trim,
        ad_pattern=ad_pattern,
        pager=pager,
        output_directory=output_directory,
        **kwargs,
    )


# --- PLOT Command
@request.command(help="Plot a visual timeline of the request content", name="plot")
@bic_options.dash
@click.option(
    "--open/--no-open",
    "-o",
    is_flag=True,
    default=True,
    help="Open the timeline in the browser",
)
@click.option(
    "--per-period",
    "-p",
    is_flag=True,
    help="Show individual representation timelines for each period",
)
@click.option(
    "--debug",
    "-d",
    is_flag=True,
    help="Show debug information",
)
@click.pass_obj
def plot_request(
    obj: AppContext,
    open: bool = False,
    per_period: bool = False,
    interval: Optional[int] = None,
    debug: bool = False,
    ad_pattern: Optional[str] = "bpkio-jitt",
    **kwargs,
):
    entry = obj.current_resource
    handler = obj.archive_handler

    if not isinstance(handler, DASHHandler):
        display_error("This command is only implemented with MPEG-DASH content")
        return

    plotter = MpdTimelinePlotter()
    plotter.set_filters(
        {
            "selected_periods": kwargs.get("mpd_period"),
            "selected_adaptation_sets": kwargs.get("mpd_adaptation_set"),
            "selected_representations": kwargs.get("mpd_representation"),
            "selected_segments": kwargs.get("mpd_segments"),
            "ad_pattern": ad_pattern,
        }
    )
    # Use consistent Plotly config (modebar + scrollZoom) to match other plots
    plotter.set_config(
        {
            "scrollZoom": True,
            "modeBarButtonsToAdd": [
                "toggleSpikeLines",
                "toggleSpikes",
                "toggleRangeSelector",
                "toggleHover",
                "toggleSpikey",
            ],
        }
    )
    resource_name = str(entry.request.url)
    plotter.add_subplot(
        SubplotInfo(
            title=resource_name,
            handler=handler,
        )
    )

    plotter.plot(interval=interval, open=open, debug=debug)


# --- SAVE Command
@request.command(help="Save the content of the request to a local file")
@archive_annotate_option
@bic_options.save
@click.pass_obj
def save(
    obj: AppContext,
    annotate: bool = False,
    inline: bool = True,
    output_directory: Optional[str] = None,
    **kwargs,
):
    request_id = obj.resource_chain.last_key()
    handler = obj.archive_handler

    # Get the file extension from the handler
    extension = ""
    if hasattr(handler, "file_extensions") and handler.file_extensions:
        extension = handler.file_extensions[0]
    elif hasattr(handler, "media_format"):
        # Fallback: try to determine extension from media format
        if handler.media_format.value == "HLS":
            extension = ".m3u8"
        elif handler.media_format.value == "DASH":
            extension = ".mpd"

    # Get content from handler - optionally annotated
    if annotate and inline:
        try:
            content = handler.annotate_content()
            if isinstance(content, bytes):
                content = content.decode("utf-8", errors="replace")
            display_info("Content annotated with metadata")
        except Exception as e:
            display_error(f"Failed to annotate content: {e}")
            content = handler.content
            if isinstance(content, bytes):
                content = content.decode("utf-8", errors="replace")
    else:
        content = handler.content
        if isinstance(content, bytes):
            content = content.decode("utf-8", errors="replace")
        elif content is None:
            content = ""

    # Create output store and save
    if output_directory is None:
        output_directory = "."

    output_store = OutputStore(output_directory, bundle=False)
    filename = f"{request_id}{extension}"
    output_store.save_text(filename, content)

    file_path = output_store.path(ensure=True) / filename
    click.secho(CL.ok(f"Saved request content to {file_path}"))
