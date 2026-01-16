"""Utility functions for annotating archive entries with parsed metadata."""

from pathlib import Path
from typing import Callable, List, Optional

from media_muncher.handlers import factory
from media_muncher.handlers.dash import DASHHandler
from media_muncher.handlers.hls import HLSHandler
from trace_shrink import Exporter
from trace_shrink.entries.trace_entry import TraceEntry

from bpkio_cli.core.exceptions import BroadpeakIoCliError


def create_handler_from_entry(entry) -> factory.ContentHandler:
    """Create an appropriate handler from an archive entry.

    Args:
        entry: The archive entry (TraceEntry) to create a handler for

    Returns:
        A ContentHandler instance appropriate for the entry's content

    Raises:
        BroadpeakIoCliError: If the handler type cannot be determined
    """
    url = str(entry.request.url)
    content = entry.content_bytes
    content_type = entry.response.content_type

    # Use factory to create handler with content type and content
    try:
        return factory.create_handler(
            url,
            content_type=content_type,
            content=content,
            from_url_only=True,  # Don't make HTTP request, we have content
        )
    except Exception as e:
        raise BroadpeakIoCliError(
            f"Could not determine handler type for request {entry.id}. "
            f"URL: {url}, Content-Type: {content_type}, Error: {e}"
        ) from e


def annotate_entry(entry, inline: bool = True) -> bool:
    """Annotate an archive entry with digest, content annotations, and facets as headers.

    This function:
    - Extracts digest information and sets it as a comment and annotation
    - Extracts facets and adds them as response headers
    - Optionally annotates content with inline comments (for HLS/DASH manifests)

    Args:
        entry: The archive entry (TraceEntry) to annotate
        inline: If True, modify the body content with inline annotations. If False, keep original body unchanged.

    Returns:
        bool: True if the entry was annotated, False otherwise
    """
    annotated = False
    try:
        handler = create_handler_from_entry(entry)
        if not handler:
            return False

        # Set digest as comment and annotation
        digest_text = handler.extract_digest()
        if digest_text:
            # Also add as annotation for Proxyman customPreviewerTabs
            entry.add_annotation("digest", digest_text)
            annotated = True

        # Add facets as response headers using the proper method
        try:
            facets = handler.extract_facets()
            if facets:
                for key, value in facets.items():
                    entry.add_response_header(key, str(value))
                annotated = True

                # Set highlight based on content type and facets
                # DASH: highlight yellow if more than 1 period
                if isinstance(handler, DASHHandler):
                    periods_count = facets.get("DASH-Periods", 0)
                    if periods_count and periods_count > 1:
                        entry.set_highlight("yellow")
                # HLS: highlight yellow if there are discontinuities
                elif isinstance(handler, HLSHandler):
                    discos_count = facets.get("HLS-Discos", 0)
                    if discos_count and discos_count > 0:
                        entry.set_highlight("yellow")

        except Exception:
            # Skip if facets extraction fails
            pass

        # Update content with annotations (inline comments) only if inline=True
        if inline:
            try:
                annotated_content = handler.annotate_content()
                # Check for None, empty bytes, or empty string
                if (
                    annotated_content is not None
                    and annotated_content != b""
                    and annotated_content != ""
                ):
                    if isinstance(annotated_content, bytes):
                        annotated_content = annotated_content.decode(
                            "utf-8", errors="replace"
                        )
                    # Use set_response_content method which clears caches properly
                    if annotated_content:
                        entry.set_response_content(annotated_content)
                        annotated = True
            except Exception:
                # Skip if content annotation fails
                pass

        return annotated
    except Exception:
        return False


def normalize_format(format: str) -> str:
    """Normalize format string, converting 'proxyman' to 'proxymanlogv2'.

    Args:
        format: The format string (e.g., "har", "proxyman", "proxymanlogv2")

    Returns:
        The normalized format string
    """
    if format == "proxyman":
        return "proxymanlogv2"
    return format


def export_entries(entries: List[TraceEntry], output_path: Path, format: str) -> None:
    """Export entries to the specified format.

    Args:
        entries: List of trace entries to export
        output_path: Path where the exported file should be written
        format: Output format ("har" or "proxymanlogv2")

    Raises:
        BroadpeakIoCliError: If the format is unsupported
    """
    format = normalize_format(format)

    if format == "har":
        Exporter.to_har(output_path, entries)
    elif format == "proxymanlogv2":
        Exporter.to_proxyman(output_path, entries)
    else:
        raise BroadpeakIoCliError(f"Unsupported format: {format}")


def get_format_extension(format: str) -> str:
    """Get the file extension for a given format.

    Args:
        format: The format string (e.g., "har", "proxyman", "proxymanlogv2")

    Returns:
        The file extension (e.g., ".har", ".proxymanlogv2")
    """
    format = normalize_format(format)
    format_extensions = {
        "har": ".har",
        "proxymanlogv2": ".proxymanlogv2",
    }
    return format_extensions.get(format, f".{format}")


def annotate_entries(
    entries: List[TraceEntry],
    inline: bool = True,
    progress_message: Optional[str] = None,
    display_info_func: Optional[Callable[[str], None]] = None,
) -> int:
    """Annotate a list of entries with parsed metadata.

    Args:
        entries: List of trace entries to annotate
        inline: If True, modify the body content with inline annotations. If False, keep original body unchanged.
        progress_message: Optional message to display before annotating (e.g., "Annotating entries..." or "Annotating manifest content...")
        display_info_func: Optional function to display progress messages (e.g., display_info from breadcrumbs)

    Returns:
        Number of entries that were successfully annotated
    """
    annotated_count = 0

    if progress_message and display_info_func:
        display_info_func(progress_message)

    for entry in entries:
        if annotate_entry(entry, inline=inline):
            annotated_count += 1

    if display_info_func:
        display_info_func(f"Annotated {annotated_count} entries")

    return annotated_count
