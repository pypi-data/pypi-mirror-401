"""Plot HLS sequence metrics over time from archive files.

This module provides functionality to extract and plot HLS playlist metrics
from archive files, showing how M3U8 attributes change over time.
"""

import sys
from datetime import datetime, timedelta

import m3u8
import plotly.graph_objects as go
from bpkio_cli.plot.plot_utils import (
    add_subplot_title,
    add_version_box,
    build_common_layout,
    build_subtitle,
    extract_filename_from_uri,
    format_time_only,
    get_color_palette,
    spike_config,
)
from plotly.subplots import make_subplots
from trace_shrink import Trace


def generate_path_pattern(paths: list[str]) -> str:
    """Generate a pattern from multiple paths by replacing variable parts with *.

    Args:
        paths: List of path strings to compare

    Returns:
        Pattern string with * replacing variable segments
    """
    if not paths:
        return ""

    if len(paths) == 1:
        return paths[0]

    # Split all paths into segments
    path_segments = [path.split("/") for path in paths]

    # Find the maximum number of segments
    max_segments = max(len(segments) for segments in path_segments)

    # Build pattern segment by segment
    pattern_segments = []
    for i in range(max_segments):
        # Get all segments at this position (if they exist)
        segments_at_pos = [segs[i] if i < len(segs) else None for segs in path_segments]

        # Filter out None values (paths shorter than this position)
        valid_segments = [s for s in segments_at_pos if s is not None]

        if not valid_segments:
            # All paths are shorter than this position, stop
            break

        # Check if all segments at this position are the same
        if len(set(valid_segments)) == 1:
            # All paths have the same segment at this position
            pattern_segments.append(valid_segments[0])
        else:
            # Segments differ, use * as wildcard
            pattern_segments.append("*")

    return "/".join(pattern_segments)


def extract_variant_playlist_info(playlist) -> dict:
    """Extract information about variant playlists and media playlists from a master playlist.

    Args:
        playlist: Parsed m3u8 playlist object

    Returns:
        Dictionary with variant playlist information:
        - is_variant: bool indicating if this is a master playlist
        - variant_count: number of variant playlists
        - media_types: dict with counts of media types (AUDIO, SUBTITLES, etc.)
    """
    result = {
        "is_variant": False,
        "variant_count": 0,
        "media_types": {},
    }

    # Check if this is a variant (master) playlist
    is_variant = getattr(playlist, "is_variant", False)
    result["is_variant"] = is_variant

    if not is_variant:
        return result

    # Count variant playlists
    playlists = getattr(playlist, "playlists", [])
    result["variant_count"] = len(playlists)

    # Count media playlists by type
    media = getattr(playlist, "media", [])
    for media_item in media:
        media_type = getattr(media_item, "type", None)
        if media_type:
            result["media_types"][media_type] = (
                result["media_types"].get(media_type, 0) + 1
            )

    return result


def format_variant_info_summary(variant_info: dict) -> str:
    """Format variant playlist information as a summary string for display.

    Args:
        variant_info: Dictionary from extract_variant_playlist_info

    Returns:
        Formatted string summary, or empty string if not a variant playlist
    """
    if not variant_info.get("is_variant"):
        return ""

    parts = []

    # Add variant count
    variant_count = variant_info.get("variant_count", 0)
    if variant_count > 0:
        parts.append(f"{variant_count} variant{'s' if variant_count != 1 else ''}")

    # Add media type counts
    media_types = variant_info.get("media_types", {})
    if media_types:
        media_parts = []
        for media_type, count in sorted(media_types.items()):
            media_parts.append(f"{count} {media_type.lower()}")
        if media_parts:
            parts.append(", ".join(media_parts))

    if parts:
        return f" ({', '.join(parts)})"
    return ""


def build_legend_name_with_variant_info(
    playlist_data: dict, playlist_key: str, master_variant_info: dict
) -> str:
    """Build legend name from playlist URL with variant information if available.

    Args:
        playlist_data: Dictionary containing 'url' key
        playlist_key: String key identifying the playlist URL
        master_variant_info: Dictionary mapping master playlist URLs to their variant info

    Returns:
        Formatted legend name with variant info appended if applicable
    """
    url_obj = playlist_data["url"]
    base_name = url_obj.path.split("/")[-1]

    # Check if this playlist is a master playlist with variant info
    variant_info = master_variant_info.get(playlist_key, {})
    variant_summary = format_variant_info_summary(variant_info)

    return base_name + variant_summary


def parse_m3u8_attributes(playlist_content: str) -> dict:
    """Parse M3U8 playlist using m3u8 library and extract relevant attributes."""
    try:
        playlist = m3u8.loads(playlist_content)
    except Exception as e:
        print(f"Error parsing M3U8 playlist with m3u8 library: {e}", file=sys.stderr)
        return {}

    result = {}

    # Extract variant playlist information (for master playlists)
    result["variant_info"] = extract_variant_playlist_info(playlist)

    # Extract MEDIA-SEQUENCE (may be None)
    result["media_sequence"] = getattr(playlist, "media_sequence", None)

    # Extract DISCONTINUITY-SEQUENCE (may be None)
    result["discontinuity_sequence"] = getattr(playlist, "discontinuity_sequence", None)

    # Extract segments with DISCONTINUITY marker and other markers in a single loop
    discontinuity_segments = []
    marked_segments = []

    for segment in playlist.segments:
        pdt = getattr(segment, "current_program_date_time", None)
        if pdt is None:
            continue

        has_discontinuity = getattr(segment, "discontinuity", False)
        segment_uri = getattr(segment, "uri", "")
        segment_duration = getattr(segment, "duration", None)

        # Collect non-discontinuity markers
        markers = []
        if getattr(segment, "cue_out_start", False):
            markers.append("CUE-OUT")
            if getattr(segment, "oatcls_scte35", None):
                markers.append("OATCLS-SCTE35")
        if getattr(segment, "cue_in", False):
            markers.append("CUE-IN")
        # dateranges might be a list or dict
        dateranges = getattr(segment, "dateranges", None)
        if dateranges:
            markers.append("DATERANGE")

        # Add to discontinuity_segments if it has DISCONTINUITY marker
        if has_discontinuity:
            discontinuity_segments.append(
                {
                    "pdt": pdt,
                    "uri": segment_uri,
                    "duration": segment_duration,
                }
            )

        # Add to marked_segments if it has other markers (excluding DISCONTINUITY-only segments)
        if markers:
            marked_segments.append(
                {
                    "pdt": pdt,
                    "uri": segment_uri,
                    "duration": segment_duration,
                    "markers": markers,
                }
            )

    result["discontinuity_segments"] = discontinuity_segments
    result["marked_segments"] = marked_segments

    # Extract all segments with their URIs and PDTs for comparison across manifests
    all_segments = []
    for segment in playlist.segments:
        pdt = getattr(segment, "current_program_date_time", None)
        if pdt is not None:
            segment_uri = getattr(segment, "uri", "")
            segment_duration = getattr(segment, "duration", None)
            is_ad = False
            if segment_uri and "bpkio-jitt" in segment_uri:
                is_ad = True

            all_segments.append(
                {
                    "pdt": pdt,
                    "uri": segment_uri,
                    "duration": segment_duration,
                    "is_ad": is_ad,
                }
            )
    result["all_segments"] = all_segments

    # Extract first and last segment PDTs and duration
    if playlist.segments:
        first_segment = playlist.segments[0]
        last_segment = playlist.segments[-1]

        first_pdt = getattr(first_segment, "current_program_date_time", None)
        last_pdt = getattr(last_segment, "current_program_date_time", None)

        # Calculate total duration and segment count
        total_duration = sum(
            getattr(seg, "duration", 0) or 0
            for seg in playlist.segments
            if getattr(seg, "duration", None) is not None
        )
        segment_count = len(playlist.segments)

        # Get last segment duration
        last_segment_duration = getattr(last_segment, "duration", None)
        if last_segment_duration is None:
            last_segment_duration = 0

        result["segment_span"] = {
            "first_pdt": first_pdt,
            "last_pdt": last_pdt,
            "duration": total_duration,
            "segment_count": segment_count,
            "last_segment_duration": last_segment_duration,
        }
    else:
        result["segment_span"] = None

    return result


def extract_hls_data(
    archive: Trace, domain: str, deduplicate: bool = False
) -> tuple[dict, dict]:
    """Extract HLS data from archive entries matching the domain.

    Args:
        archive: The archive reader instance
        domain: Domain name to filter entries
        deduplicate: If True, filter out entries with duplicate media_sequence values

    Returns:
        tuple: (data_by_playlist, master_variant_info) where:
            - data_by_playlist: Dictionary mapping playlist URLs to their data points
            - master_variant_info: Dictionary mapping master playlist URLs to their variant info
    """
    from trace_shrink import Format

    # Filter entries by domain and HLS format
    hls_entries = []

    # Get all HLS manifest URLs
    hls_urls = archive.get_abr_manifest_urls(format=Format.HLS)

    # Filter by domain
    for hls_url in hls_urls:
        if domain in str(hls_url.url.host):
            entries = archive.get_entries_for_url(hls_url.url)
            hls_entries.extend(entries)

    # Sort by request time
    hls_entries.sort(key=lambda e: e.timeline.request_start or datetime.min)

    # Extract data from each playlist
    # Group by playlist URL to handle multiple variant playlists independently
    data_by_playlist = {}
    prev_media_sequences = {}  # Track previous media_sequence per playlist URL
    master_variant_info = {}  # Store variant info from master playlists (once per master)

    for entry in hls_entries:
        request_time = entry.timeline.request_start
        if request_time is None:
            continue

        playlist_url_obj = entry.request.url
        playlist_key = str(playlist_url_obj)  # Use full URL as key

        playlist_content = entry.content
        if isinstance(playlist_content, bytes):
            playlist_content = playlist_content.decode("utf-8", errors="ignore")

        playlist_attrs = parse_m3u8_attributes(playlist_content)

        if not playlist_attrs:
            continue

        # Check if this is a master/variant playlist
        variant_info = playlist_attrs.get("variant_info", {})
        is_variant = variant_info.get("is_variant", False)

        if is_variant:
            # Store variant info for this master playlist (once per unique master URL)
            if playlist_key not in master_variant_info:
                master_variant_info[playlist_key] = variant_info
            # Master playlists don't have media_sequence, so we include them always
            # (they are not deduplicated)
            # Skip rest of processing for variant playlists
            continue

        # Standard parsing for media playlists (is_variant=False)
        media_sequence = playlist_attrs.get("media_sequence")

        # Skip if deduplicate is enabled and media_sequence matches previous for this playlist
        if (
            deduplicate
            and playlist_key in prev_media_sequences
            and prev_media_sequences[playlist_key] == media_sequence
        ):
            continue

        if playlist_key not in data_by_playlist:
            data_by_playlist[playlist_key] = {
                "url": playlist_url_obj,
                "data_points": [],
            }

        data_by_playlist[playlist_key]["data_points"].append(
            {
                "request_time": request_time,
                "request_id": entry.id,
                "media_sequence": media_sequence,
                "discontinuity_sequence": playlist_attrs.get("discontinuity_sequence"),
                "discontinuity_segments": playlist_attrs.get(
                    "discontinuity_segments", []
                ),
                "marked_segments": playlist_attrs.get("marked_segments", []),
                "segment_span": playlist_attrs.get("segment_span"),
                "all_segments": playlist_attrs.get("all_segments", []),
            }
        )

        # Update previous media_sequence for next iteration
        prev_media_sequences[playlist_key] = media_sequence

    return data_by_playlist, master_variant_info


def plot_hls_metrics(
    data_by_playlist: dict,
    first_hls_url=None,
    master_variant_info: dict = None,
    service_id: str | None = None,
    session_id: str | None = None,
    domain: str | None = None,
    path: str | None = None,
    show_segments: bool = False,
    show_media_sequence: bool = True,
    show_discontinuity_sequence: bool = True,
    show_segment_spans: bool = True,
):
    """Plot HLS metrics using plotly express with subplots.

    Args:
        data_by_playlist: Dictionary mapping playlist URLs to their data points
        first_hls_url: Optional URL of the first playlist for subtitle
        master_variant_info: Dictionary mapping master playlist URLs to their variant info
        show_segments: If True, show individual segment dots in the Segment Range plot
        show_media_sequence: If True, show Media Sequence plot (default: True)
        show_discontinuity_sequence: If True, show Discontinuity Sequence plot (default: True)
        show_segment_spans: If True, show Segment Range plot (default: True)

    Returns:
        Plotly figure object
    """
    if master_variant_info is None:
        master_variant_info = {}
    if not data_by_playlist:
        print("No data points to plot.", file=sys.stderr)
        return None

    # Get all playlist keys and assign colors
    playlist_keys = list(data_by_playlist.keys())
    playlist_colors = get_color_palette()

    # Create color mapping for playlists
    playlist_color_map = {}
    for idx, playlist_key in enumerate(playlist_keys):
        playlist_color_map[playlist_key] = playlist_colors[idx % len(playlist_colors)]

    # Check which plots have data
    has_media_sequence = False
    has_discontinuity_sequence = False
    has_discontinuity_segments = False
    has_marked_segments = False
    has_segment_spans = False

    # Check Plot 1: MEDIA-SEQUENCE
    if show_media_sequence:
        for playlist_data in data_by_playlist.values():
            data_points = playlist_data["data_points"]
            media_sequences = [dp["media_sequence"] for dp in data_points]
            if any(ms is not None for ms in media_sequences):
                has_media_sequence = True
                break

    # Check Plot 2: DISCONTINUITY-SEQUENCE
    if show_discontinuity_sequence:
        for playlist_data in data_by_playlist.values():
            data_points = playlist_data["data_points"]
            discontinuity_sequences = [
                dp["discontinuity_sequence"] for dp in data_points
            ]
            if any(ds is not None for ds in discontinuity_sequences):
                has_discontinuity_sequence = True
                break

    # Check Plot 3: DISCONTINUITY segments
    for playlist_data in data_by_playlist.values():
        data_points = playlist_data["data_points"]
        for dp in data_points:
            if dp.get("discontinuity_segments"):
                has_discontinuity_segments = True
                break
        if has_discontinuity_segments:
            break

    # Check Plot 4: Marked segments
    for playlist_data in data_by_playlist.values():
        data_points = playlist_data["data_points"]
        for dp in data_points:
            if dp.get("marked_segments"):
                has_marked_segments = True
                break
        if has_marked_segments:
            break

    # Check Plot 5: Segment spans
    if show_segment_spans:
        for playlist_data in data_by_playlist.values():
            data_points = playlist_data["data_points"]
            for dp in data_points:
                if dp.get("segment_span"):
                    has_segment_spans = True
                    break
            if has_segment_spans:
                break

    # Build list of plots to include
    plots_to_include = []
    plot_metadata = {
        1: {
            "title": "Media Sequence",
            "height": 200,
            "enabled": has_media_sequence and show_media_sequence,
            "position": "top-left",
        },
        2: {
            "title": "Discontinuity Sequence",
            "height": 200,
            "enabled": has_discontinuity_sequence and show_discontinuity_sequence,
            "position": "top-left",
        },
        5: {
            "title": "Segment Range",
            "height": 500,
            "enabled": has_segment_spans and show_segment_spans,
            "position": "top-right",
        },
    }

    # Create mapping from logical plot number to actual row number
    plot_to_row = {}
    row_heights = []

    # Add default position to each plot metadata and build rows (user-editable)
    for plot_num in [1, 2, 5]:
        if plot_metadata[plot_num]["enabled"]:
            actual_row = len(plots_to_include) + 1
            plot_to_row[plot_num] = actual_row
            plots_to_include.append(plot_num)
            row_heights.append(plot_metadata[plot_num]["height"])

    num_rows = len(plots_to_include)
    if num_rows == 0:
        print("No data available for any plots.", file=sys.stderr)
        return None

    # Create subplots
    fig = make_subplots(
        rows=num_rows,
        cols=1,
        vertical_spacing=0.08,
        shared_xaxes=False,
        row_heights=row_heights,
    )

    # Left-align all subplot titles
    for annotation in fig.layout.annotations:
        if annotation.text:
            annotation.xanchor = "left"
            annotation.x = 0.0

    # Add annotations for each enabled plot using positions from plot_metadata
    add_subplot_title(fig, plots_to_include, plot_to_row, plot_metadata)

    def get_row(plot_num):
        row = plot_to_row.get(plot_num)
        if row is None:
            raise ValueError(
                f"Plot {plot_num} is not enabled. Cannot get row number. "
                f"Enabled plots: {list(plot_to_row.keys())}"
            )
        if row > num_rows:
            raise ValueError(
                f"Plot {plot_num} has row {row} but subplot only has {num_rows} rows."
            )
        return row

    # Plot 1: MEDIA-SEQUENCE
    if has_media_sequence and show_media_sequence:
        row_num = get_row(1)
        all_media_sequences = []

        # First pass: collect all values for y-axis range calculation
        for playlist_key, playlist_data in data_by_playlist.items():
            data_points = playlist_data["data_points"]
            media_sequences = [dp["media_sequence"] for dp in data_points]
            valid_media_sequences = [ms for ms in media_sequences if ms is not None]
            all_media_sequences.extend(valid_media_sequences)

        # Calculate y-axis range
        y_min = None
        y_max = None
        y_bottom = None
        y_top = None
        if all_media_sequences:
            y_min = min(all_media_sequences)
            y_max = max(all_media_sequences)
            y_range = y_max - y_min
            y_bottom = y_min - 0.1 * y_range if y_range > 0 else y_min - 1
            y_top = y_max + 0.1 * y_range if y_range > 0 else y_max + 1

        # Second pass: for each playlist, detect and plot errors, then plot data traces
        for playlist_key, playlist_data in data_by_playlist.items():
            data_points = playlist_data["data_points"]
            color = playlist_color_map[playlist_key]

            legend_name = build_legend_name_with_variant_info(
                playlist_data, playlist_key, master_variant_info
            )

            request_times = [dp["request_time"] for dp in data_points]
            media_sequences = [dp["media_sequence"] for dp in data_points]

            valid_indices = [
                i for i, ms in enumerate(media_sequences) if ms is not None
            ]

            if valid_indices:
                # Detect errors for this playlist
                playlist_error_lines_x = []
                playlist_error_details = []  # Store details for hover tooltips
                sorted_valid_indices = sorted(
                    valid_indices, key=lambda i: request_times[i]
                )
                prev_value = None
                prev_idx = None
                for idx in sorted_valid_indices:
                    current_value = media_sequences[idx]
                    if prev_value is not None and current_value < prev_value:
                        playlist_error_lines_x.append(request_times[idx])
                        playlist_error_details.append(
                            {
                                "request_time": request_times[idx],
                                "issue": "Media sequence decreased",
                                "prev_value": prev_value,
                                "current_value": current_value,
                            }
                        )
                    elif prev_value is not None and current_value > prev_value:
                        # Check if MEDIA-SEQUENCE increase matches removed segments
                        prev_dp = data_points[prev_idx]
                        curr_dp = data_points[idx]

                        prev_segments = prev_dp.get("all_segments", [])
                        curr_segments = curr_dp.get("all_segments", [])

                        # Create sets of segment URIs for comparison
                        prev_uris = {seg["uri"] for seg in prev_segments}
                        curr_uris = {seg["uri"] for seg in curr_segments}

                        # Find segments that were removed (in previous but not in current)
                        removed_segments = prev_uris - curr_uris
                        removed_count = len(removed_segments)

                        # Calculate MEDIA-SEQUENCE increase
                        sequence_increase = current_value - prev_value

                        # If increase doesn't match removed count, it's an error
                        if sequence_increase != removed_count:
                            playlist_error_lines_x.append(request_times[idx])
                            playlist_error_details.append(
                                {
                                    "request_time": request_times[idx],
                                    "issue": "Media sequence increase doesn't match removed segments",
                                    "prev_value": prev_value,
                                    "current_value": current_value,
                                    "sequence_increase": sequence_increase,
                                    "removed_count": removed_count,
                                }
                            )

                    prev_value = current_value
                    prev_idx = idx

                # Add vertical red lines for errors FIRST (so they appear behind the data)
                if (
                    playlist_error_lines_x
                    and y_bottom is not None
                    and y_top is not None
                ):
                    for error_detail in playlist_error_details:
                        error_x = error_detail["request_time"]
                        error_time_str = format_time_only(error_x)
                        issue = error_detail["issue"]

                        # Build hover template based on error type
                        if issue == "Media sequence decreased":
                            hovertemplate = (
                                "<b>Media Sequence Error</b><br>"
                                + "<b>Request Time:</b> "
                                + error_time_str
                                + "<br>"
                                + f"<b>Issue:</b> Media sequence decreased ({error_detail['prev_value']} -> {error_detail['current_value']})<br>"
                                + "<extra></extra>"
                            )
                        else:
                            hovertemplate = (
                                "<b>Media Sequence Error</b><br>"
                                + "<b>Request Time:</b> "
                                + error_time_str
                                + "<br>"
                                + "<b>Media sequence increase:</b> "
                                + f"{error_detail['sequence_increase']} ({error_detail['removed_count']} segments removed)"
                                + "<br>"
                                + "<b>Issue:</b> Media sequence increase doesn't match removed segments<br>"
                                + "<extra></extra>"
                            )

                        fig.add_trace(
                            go.Scatter(
                                x=[error_x, error_x],
                                y=[y_bottom, y_top],
                                mode="lines",
                                name="Error",
                                line=dict(color="rgba(255, 0, 0, 0.5)", width=5),
                                showlegend=False,
                                hoverinfo="all",
                                hovertemplate=hovertemplate,
                                legendgroup=playlist_key,
                                legendgrouptitle_text=legend_name,
                            ),
                            row=row_num,
                            col=1,
                        )

                # Now add the data traces (they will appear on top)
                hover_data = [
                    [
                        data_points[i]["request_id"],
                        format_time_only(request_times[i]),
                        media_sequences[i],
                    ]
                    for i in valid_indices
                ]

                fig.add_trace(
                    go.Scatter(
                        x=[request_times[i] for i in valid_indices],
                        y=[media_sequences[i] for i in valid_indices],
                        mode="markers+lines",
                        name="Playlist",
                        marker=dict(size=6, color=color),
                        line=dict(color=color),
                        hovertemplate="<b>Request ID:</b> %{customdata[0]}<br>"
                        + "<b>Request Time:</b> %{customdata[1]}<br>"
                        + "<b>MEDIA-SEQUENCE:</b> %{customdata[2]}<extra></extra>",
                        customdata=hover_data,
                        legendgroup=playlist_key,
                        legendgrouptitle_text=legend_name,
                    ),
                    row=row_num,
                    col=1,
                )

    # Plot 2: DISCONTINUITY-SEQUENCE
    if has_discontinuity_sequence and show_discontinuity_sequence:
        row_num = get_row(2)
        all_discontinuity_sequences = []

        # First pass: collect all values for y-axis range calculation
        for playlist_key, playlist_data in data_by_playlist.items():
            data_points = playlist_data["data_points"]
            discontinuity_sequences = [
                dp["discontinuity_sequence"] for dp in data_points
            ]
            valid_discontinuity_sequences = [
                ds for ds in discontinuity_sequences if ds is not None
            ]
            all_discontinuity_sequences.extend(valid_discontinuity_sequences)

        # Calculate y-axis range
        y_min = None
        y_max = None
        y_bottom = None
        y_top = None
        if all_discontinuity_sequences:
            y_min = min(all_discontinuity_sequences)
            y_max = max(all_discontinuity_sequences)
            y_range = y_max - y_min
            y_bottom = y_min - 0.1 * y_range if y_range > 0 else y_min - 1
            y_top = y_max + 0.1 * y_range if y_range > 0 else y_max + 1

        # Second pass: for each playlist, detect and plot errors, then plot data traces
        for playlist_key, playlist_data in data_by_playlist.items():
            data_points = playlist_data["data_points"]
            color = playlist_color_map.get(playlist_key, "blue")

            legend_name = build_legend_name_with_variant_info(
                playlist_data, playlist_key, master_variant_info
            )

            request_times = [dp["request_time"] for dp in data_points]
            discontinuity_sequences = [
                dp["discontinuity_sequence"] for dp in data_points
            ]

            valid_indices = [
                i for i, ds in enumerate(discontinuity_sequences) if ds is not None
            ]

            if valid_indices:
                # Detect errors for this playlist
                playlist_error_lines_x = []
                sorted_valid_indices = sorted(
                    valid_indices, key=lambda i: request_times[i]
                )
                prev_value = None
                for idx in sorted_valid_indices:
                    current_value = discontinuity_sequences[idx]
                    if prev_value is not None and current_value < prev_value:
                        playlist_error_lines_x.append(request_times[idx])
                    prev_value = current_value

                # Add vertical red lines for errors FIRST (so they appear behind the data)
                if (
                    playlist_error_lines_x
                    and y_bottom is not None
                    and y_top is not None
                ):
                    for error_x in playlist_error_lines_x:
                        error_time_str = format_time_only(error_x)
                        fig.add_trace(
                            go.Scatter(
                                x=[error_x, error_x],
                                y=[y_bottom, y_top],
                                mode="lines",
                                name="Error",
                                line=dict(color="rgba(255, 0, 0, 0.5)", width=5),
                                showlegend=False,
                                hoverinfo="all",
                                hovertemplate="<b>Discontinuity Sequence Error</b><br>"
                                + "<b>Request Time:</b> "
                                + error_time_str
                                + "<br>"
                                + "<b>Issue:</b> Discontinuity sequence decreased<br>"
                                + "<extra></extra>",
                                legendgroup=playlist_key,
                                legendgrouptitle_text=legend_name,
                            ),
                            row=row_num,
                            col=1,
                        )

                # Now add the data traces (they will appear on top)
                hover_data = [
                    [
                        data_points[i]["request_id"],
                        format_time_only(request_times[i]),
                        discontinuity_sequences[i],
                    ]
                    for i in valid_indices
                ]

                fig.add_trace(
                    go.Scatter(
                        x=[request_times[i] for i in valid_indices],
                        y=[discontinuity_sequences[i] for i in valid_indices],
                        mode="markers+lines",
                        name="Discontinuity Seq",
                        marker=dict(size=6, color=color),
                        line=dict(color=color),
                        hovertemplate="<b>Request ID:</b> %{customdata[0]}<br>"
                        + "<b>DISCONTINUITY-SEQUENCE:</b> %{customdata[2]}<extra></extra>",
                        customdata=hover_data,
                        legendgroup=playlist_key,
                        legendgrouptitle_text=legend_name,
                    ),
                    row=row_num,
                    col=1,
                )

    # Plot 5: Segment Range (first and last segment PDTs)
    # Also includes discontinuity and marked segments as overlay markers
    if has_segment_spans and show_segment_spans:
        row_num = get_row(5)
        for playlist_key, playlist_data in data_by_playlist.items():
            data_points = playlist_data["data_points"]
            color = playlist_color_map.get(playlist_key, "blue")
            legend_name = build_legend_name_with_variant_info(
                playlist_data, playlist_key, master_variant_info
            )

            # Extract segment spans
            segment_spans = []
            for dp in data_points:
                segment_span = dp.get("segment_span")
                if segment_span:
                    segment_spans.append(
                        {
                            "request_time": dp["request_time"],
                            "request_id": dp["request_id"],
                            "first_pdt": segment_span["first_pdt"],
                            "last_pdt": segment_span["last_pdt"],
                            "duration": segment_span.get("duration", 0),
                            "segment_count": segment_span.get("segment_count", 0),
                            "last_segment_duration": segment_span.get(
                                "last_segment_duration", 0
                            ),
                        }
                    )

            if segment_spans:
                # Sort by request_time
                segment_spans.sort(key=lambda x: x["request_time"])

                # Detect when first or last segment PDT goes backwards in time
                segment_range_errors = []
                if len(segment_spans) > 1:
                    for i in range(1, len(segment_spans)):
                        prev_span = segment_spans[i - 1]
                        curr_span = segment_spans[i]

                        # Check if first segment PDT went backwards
                        if prev_span["first_pdt"] > curr_span["first_pdt"]:
                            segment_range_errors.append(
                                {
                                    "request_time": curr_span["request_time"],
                                    "request_id": curr_span["request_id"],
                                    "pdt": curr_span["first_pdt"],
                                    "prev_pdt": prev_span["first_pdt"],
                                    "type": "first",
                                }
                            )

                        # Check if last segment PDT went backwards
                        if prev_span["last_pdt"] > curr_span["last_pdt"]:
                            segment_range_errors.append(
                                {
                                    "request_time": curr_span["request_time"],
                                    "request_id": curr_span["request_id"],
                                    "pdt": curr_span["last_pdt"],
                                    "prev_pdt": prev_span["last_pdt"],
                                    "type": "last",
                                }
                            )

                # Collect all individual segments for y-axis range calculation
                all_segment_pdts = []
                for dp in data_points:
                    for seg in dp.get("all_segments", []):
                        all_segment_pdts.append(seg["pdt"])

                # Add vertical red error lines for segment range errors FIRST (so they appear behind the data)
                if segment_range_errors:
                    # Calculate y-axis range from all individual segment PDTs
                    if all_segment_pdts:
                        y_min = min(all_segment_pdts)
                        y_max = max(all_segment_pdts)
                        y_range = (y_max - y_min).total_seconds()
                        if y_range == 0:
                            y_range = 1  # Default to 1 second if all PDTs are the same
                        y_range_td = timedelta(seconds=y_range)
                        y_bottom = y_min - y_range_td * 0.05
                        y_top = y_max + y_range_td * 0.05
                    else:
                        # Fallback to segment spans if no individual segments available
                        all_pdts = []
                        for span in segment_spans:
                            all_pdts.append(span["first_pdt"])
                            all_pdts.append(span["last_pdt"])
                        if all_pdts:
                            y_min = min(all_pdts)
                            y_max = max(all_pdts)
                            y_range = (y_max - y_min).total_seconds()
                            if y_range == 0:
                                y_range = 1
                            y_range_td = timedelta(seconds=y_range)
                            y_bottom = y_min - y_range_td * 0.05
                            y_top = y_max + y_range_td * 0.05
                        else:
                            y_bottom = None
                            y_top = None

                    if y_bottom is not None and y_top is not None:
                        for err in segment_range_errors:
                            err_pdt_str = format_time_only(err["pdt"])
                            prev_pdt_str = format_time_only(err["prev_pdt"])
                            segment_type = err["type"].capitalize()

                            fig.add_trace(
                                go.Scatter(
                                    x=[err["request_time"], err["request_time"]],
                                    y=[y_bottom, y_top],
                                    mode="lines",
                                    name="Error",
                                    line=dict(color="rgba(255, 0, 0, 0.5)", width=5),
                                    showlegend=False,
                                    legendgroup=playlist_key,
                                    legendgrouptitle_text=legend_name,
                                    hoverinfo="all",
                                    hovertemplate="<b>Segment Range Error</b><br>"
                                    + "<b>Segment Type:</b> "
                                    + segment_type
                                    + "<br>"
                                    + "<b>Current PDT:</b> "
                                    + err_pdt_str
                                    + "<br>"
                                    + "<b>Previous PDT:</b> "
                                    + prev_pdt_str
                                    + "<br>"
                                    + "<b>Issue:</b> "
                                    + segment_type
                                    + " segment PDT went backwards in time<br>"
                                    + "<extra></extra>",
                                ),
                                row=row_num,
                                col=1,
                            )

                # Add vertical lines from first_pdt to last_pdt + last_segment_duration for each span
                # Line width: 2px when segments are hidden, 6px (semi-transparent) when shown
                if show_segments:
                    line_width = 6
                    line_opacity = 0.3
                else:
                    line_width = 2
                    line_opacity = 1.0

                # Extract playlist name from URL
                playlist_url = playlist_data["url"]
                playlist_name = extract_filename_from_uri(str(playlist_url))

                for idx, span in enumerate(segment_spans):
                    first_pdt_str = format_time_only(span["first_pdt"])
                    last_pdt = span["last_pdt"]
                    last_segment_duration = span.get("last_segment_duration", 0)
                    # Calculate end point: last_pdt + duration of last segment
                    end_pdt = last_pdt + timedelta(seconds=last_segment_duration)
                    end_pdt_str = format_time_only(end_pdt)
                    segment_count = span.get("segment_count", 0)
                    duration = span.get("duration", 0)
                    duration_str = f"{duration:.2f}s"

                    fig.add_trace(
                        go.Scatter(
                            x=[span["request_time"], span["request_time"]],
                            y=[span["first_pdt"], end_pdt],
                            mode="lines",
                            name="Segments and Markers",
                            line=dict(width=line_width, color=color),
                            opacity=line_opacity,
                            showlegend=False,
                            legendgroup=playlist_key,
                            legendgrouptitle_text=legend_name,
                            hovertemplate="<b><u>Playlist:</u></b> "
                            + playlist_name
                            + "<br>"
                            + "<b>Request ID:</b> "
                            + span["request_id"]
                            + "<br>"
                            + "<b>Number of Segments:</b> "
                            + str(segment_count)
                            + "<br>"
                            + "<b>Segments:</b> "
                            + first_pdt_str
                            + " -> "
                            + end_pdt_str
                            + "<br>"
                            + "<b>Duration:</b> "
                            + duration_str
                            + "<extra></extra>",
                        ),
                        row=row_num,
                        col=1,
                    )

                # Plot ad spans for this playlist (before segment dots so they appear behind)
                ad_spans_shown_in_legend_for_playlist = False
                for dp in data_points:
                    request_time = dp["request_time"]
                    all_segments = dp.get("all_segments", [])

                    # Group consecutive ad segments into spans
                    ad_spans = []
                    current_ad_span = None

                    for seg in all_segments:
                        if seg.get("is_ad", False):
                            seg_pdt = seg.get("pdt")

                            if seg_pdt is not None:
                                if current_ad_span is None:
                                    # Start new ad span
                                    current_ad_span = {
                                        "start": seg_pdt,
                                        "end": seg_pdt,
                                    }
                                else:
                                    # Extend current ad span
                                    current_ad_span["end"] = seg_pdt
                        else:
                            # Non-ad segment - close current span if any
                            if current_ad_span is not None:
                                ad_spans.append(current_ad_span)
                                current_ad_span = None

                    # Close any remaining span
                    if current_ad_span is not None:
                        ad_spans.append(current_ad_span)

                    # Plot ad spans
                    for ad_span in ad_spans:
                        span_start = ad_span["start"]
                        span_end = ad_span["end"]

                        # Plot as semi-transparent gold vertical line (like events, but no markers)
                        fig.add_trace(
                            go.Scatter(
                                x=[request_time, request_time],
                                y=[span_start, span_end],
                                mode="lines",
                                name="Ad",
                                line=dict(color="gold", width=11),
                                opacity=0.9,
                                showlegend=not ad_spans_shown_in_legend_for_playlist,
                                hoverinfo="skip",
                                legendgroup=playlist_key,
                                legendgrouptitle_text=legend_name,
                            ),
                            row=row_num,
                            col=1,
                        )
                        ad_spans_shown_in_legend_for_playlist = True

                # Collect all individual segments to plot as dots (only if show_segments is True)
                if show_segments:
                    all_segment_dots = []
                    for dp in data_points:
                        request_time = dp["request_time"]
                        request_id = dp["request_id"]
                        for seg_idx, seg in enumerate(dp.get("all_segments", [])):
                            all_segment_dots.append(
                                {
                                    "request_time": request_time,
                                    "request_id": request_id,
                                    "pdt": seg["pdt"],
                                    "uri": seg.get("uri", ""),
                                    "duration": seg.get("duration"),
                                    "position": seg_idx + 1,  # 1-based position
                                }
                            )

                    # Plot individual segments as dots
                    if all_segment_dots:
                        hover_data = [
                            [
                                dot["position"],
                                extract_filename_from_uri(dot["uri"]),
                                format_time_only(dot["pdt"]),
                                f"{dot['duration']:.2f}s"
                                if dot.get("duration") is not None
                                else "N/A",
                            ]
                            for dot in all_segment_dots
                        ]

                        fig.add_trace(
                            go.Scatter(
                                x=[dot["request_time"] for dot in all_segment_dots],
                                y=[dot["pdt"] for dot in all_segment_dots],
                                mode="markers",
                                name="Segments",
                                marker=dict(size=3, color=color),
                                showlegend=True,
                                legendgroup=playlist_key,
                                legendgrouptitle_text=legend_name,
                                hovertemplate="<b>Segment</b> #%{customdata[0]}<br>"
                                + "<b>Segment URL:</b> %{customdata[1]}<br>"
                                + "<b>PDT:</b> %{customdata[2]}<br>"
                                + "<b>Duration:</b> %{customdata[3]}<extra></extra>",
                                customdata=hover_data,
                            ),
                            row=row_num,
                            col=1,
                        )

                # Add lines connecting consecutive first_pdt points
                if len(segment_spans) > 1:
                    request_times = [span["request_time"] for span in segment_spans]
                    first_pdts = [span["first_pdt"] for span in segment_spans]

                    fig.add_trace(
                        go.Scatter(
                            x=request_times,
                            y=first_pdts,
                            mode="lines",
                            name=f"{legend_name} (first)",
                            line=dict(width=1, color=color, dash="dot"),
                            showlegend=False,
                            legendgroup=playlist_key,
                            legendgrouptitle_text=legend_name,
                            hoverinfo="skip",
                        ),
                        row=row_num,
                        col=1,
                    )

                # Add lines connecting consecutive last_pdt + last_segment_duration points
                if len(segment_spans) > 1:
                    request_times = [span["request_time"] for span in segment_spans]
                    # Calculate end points: last_pdt + duration of last segment
                    last_pdts = [
                        span["last_pdt"]
                        + timedelta(seconds=span.get("last_segment_duration", 0))
                        for span in segment_spans
                    ]

                    fig.add_trace(
                        go.Scatter(
                            x=request_times,
                            y=last_pdts,
                            mode="lines",
                            name=f"{legend_name} (last)",
                            line=dict(width=1, color=color, dash="dot"),
                            showlegend=False,
                            legendgroup=playlist_key,
                            legendgrouptitle_text=legend_name,
                            hoverinfo="skip",
                        ),
                        row=row_num,
                        col=1,
                    )

            # Detect segments with changed PDT between successive manifests
            pdt_change_errors = []
            if len(data_points) > 1:
                # Sort data points by request time
                sorted_data_points = sorted(
                    data_points, key=lambda dp: dp["request_time"]
                )

                for i in range(1, len(sorted_data_points)):
                    prev_dp = sorted_data_points[i - 1]
                    curr_dp = sorted_data_points[i]

                    prev_segments = prev_dp.get("all_segments", [])
                    curr_segments = curr_dp.get("all_segments", [])

                    # Create a map of URI -> PDT for previous manifest
                    prev_segment_map = {seg["uri"]: seg["pdt"] for seg in prev_segments}

                    # Check each segment in current manifest
                    for seg_idx, seg in enumerate(curr_segments):
                        uri = seg["uri"]
                        curr_pdt = seg["pdt"]

                        # If this segment existed in previous manifest, compare PDTs
                        if uri in prev_segment_map:
                            prev_pdt = prev_segment_map[uri]

                            # Compare PDTs using timestamp to handle timezone/microsecond differences
                            # Only flag as error if difference is significant (> 1 millisecond)
                            pdt_changed = False
                            if prev_pdt is None or curr_pdt is None:
                                pdt_changed = prev_pdt != curr_pdt
                            else:
                                try:
                                    # Convert to timestamps for robust comparison
                                    prev_ts = prev_pdt.timestamp()
                                    curr_ts = curr_pdt.timestamp()
                                    # Only flag as error if difference is more than 1 millisecond
                                    pdt_changed = abs(curr_ts - prev_ts) > 0.001
                                except (AttributeError, TypeError, OSError):
                                    # Fallback to direct comparison if timestamp conversion fails
                                    pdt_changed = prev_pdt != curr_pdt

                            if pdt_changed:
                                # PDT changed - this is an error
                                pdt_change_errors.append(
                                    {
                                        "request_time": curr_dp["request_time"],
                                        "request_id": curr_dp["request_id"],
                                        "pdt": curr_pdt,
                                        "uri": uri,
                                        "prev_pdt": prev_pdt,
                                        "position": seg_idx + 1,  # 1-based position
                                    }
                                )

            # Add red error dots for segments with changed PDT
            if pdt_change_errors:
                hover_data = [
                    [
                        extract_filename_from_uri(err["uri"]),
                        format_time_only(err["prev_pdt"]),
                        format_time_only(err["pdt"]),
                        err["position"],
                    ]
                    for err in pdt_change_errors
                ]

                fig.add_trace(
                    go.Scatter(
                        x=[err["request_time"] for err in pdt_change_errors],
                        y=[err["pdt"] for err in pdt_change_errors],
                        mode="markers",
                        name="PDT Errors",
                        marker=dict(size=12, color="orange", symbol="star-diamond"),
                        showlegend=True,
                        legendgroup=playlist_key,
                        legendgrouptitle_text=legend_name,
                        hovertemplate="<b>Segment URI:</b> %{customdata[0]}<br>"
                        + "<b>Position:</b> %{customdata[3]}<br>"
                        + "<b>PDT:</b> was: %{customdata[1]} -> now: %{customdata[2]}<br>"
                        + "<b>Issue:</b> Segment PDT changed between manifests<extra></extra>",
                        customdata=hover_data,
                    ),
                    row=row_num,
                    col=1,
                )

            # Detect segments appearing out of order (new segment with PDT before last segment of previous manifest)
            out_of_order_errors = []
            if len(data_points) > 1:
                # Sort data points by request time
                sorted_data_points = sorted(
                    data_points, key=lambda dp: dp["request_time"]
                )

                for i in range(1, len(sorted_data_points)):
                    prev_dp = sorted_data_points[i - 1]
                    curr_dp = sorted_data_points[i]

                    prev_segments = prev_dp.get("all_segments", [])
                    curr_segments = curr_dp.get("all_segments", [])

                    if not prev_segments or not curr_segments:
                        continue

                    # Get the last segment's PDT from previous manifest
                    prev_last_pdt = prev_segments[-1]["pdt"]

                    # Create a set of URIs from previous manifest
                    prev_uris = {seg["uri"] for seg in prev_segments}

                    # Check each segment in current manifest
                    for seg_idx, seg in enumerate(curr_segments):
                        uri = seg["uri"]
                        curr_pdt = seg["pdt"]

                        # If this segment is new (not in previous manifest)
                        if uri not in prev_uris:
                            # Check if its PDT is before the last segment's PDT in previous manifest
                            if curr_pdt < prev_last_pdt:
                                # This is an error - segment appearing out of order
                                out_of_order_errors.append(
                                    {
                                        "request_time": curr_dp["request_time"],
                                        "request_id": curr_dp["request_id"],
                                        "pdt": curr_pdt,
                                        "uri": uri,
                                        "prev_last_pdt": prev_last_pdt,
                                        "position": seg_idx + 1,  # 1-based position
                                    }
                                )

            # Add red cross markers for out-of-order segments
            if out_of_order_errors:
                hover_data = [
                    [
                        extract_filename_from_uri(err["uri"]),
                        format_time_only(err["pdt"]),
                        format_time_only(err["prev_last_pdt"]),
                        err["position"],
                    ]
                    for err in out_of_order_errors
                ]

                fig.add_trace(
                    go.Scatter(
                        x=[err["request_time"] for err in out_of_order_errors],
                        y=[err["pdt"] for err in out_of_order_errors],
                        mode="markers",
                        name="Out-of-Order Errors",
                        marker=dict(size=12, color="red", symbol="x"),
                        showlegend=True,
                        legendgroup=playlist_key,
                        legendgrouptitle_text=legend_name,
                        hovertemplate="<b>Segment URI:</b> %{customdata[0]}<br>"
                        + "<b>Position:</b> %{customdata[3]}<br>"
                        + "<b>Segment PDT:</b> %{customdata[1]}<br>"
                        + "<b>Previous Last Segment PDT:</b> %{customdata[2]}<br>"
                        + "<b>Issue:</b> Segment appears with a path that wasn't in the previous version, at a time before the last segment in the previous version<extra></extra>",
                        customdata=hover_data,
                    ),
                    row=row_num,
                    col=1,
                )

            # Add discontinuity segments as overlay markers (toggleable from legend)
            if has_discontinuity_segments:
                discontinuity_data = []
                for dp in data_points:
                    request_time = dp["request_time"]
                    request_id = dp["request_id"]
                    for seg in dp.get("discontinuity_segments", []):
                        discontinuity_data.append(
                            {
                                "request_time": request_time,
                                "request_id": request_id,
                                "pdt": seg["pdt"],
                                "uri": seg.get("uri", ""),
                            }
                        )

                if discontinuity_data:
                    # Add connecting lines between successive manifests for same segments
                    if len(data_points) > 1:
                        sorted_data_points = sorted(
                            data_points, key=lambda dp: dp["request_time"]
                        )

                        for i in range(1, len(sorted_data_points)):
                            prev_dp = sorted_data_points[i - 1]
                            curr_dp = sorted_data_points[i]

                            # Create maps of URI -> (request_time, pdt) for both manifests
                            prev_discontinuities = {
                                seg["uri"]: (prev_dp["request_time"], seg["pdt"])
                                for seg in prev_dp.get("discontinuity_segments", [])
                            }
                            curr_discontinuities = {
                                seg["uri"]: (curr_dp["request_time"], seg["pdt"])
                                for seg in curr_dp.get("discontinuity_segments", [])
                            }

                            # Draw lines for segments that appear in both manifests
                            for uri in (
                                prev_discontinuities.keys()
                                & curr_discontinuities.keys()
                            ):
                                prev_time, prev_pdt = prev_discontinuities[uri]
                                curr_time, curr_pdt = curr_discontinuities[uri]

                                fig.add_trace(
                                    go.Scatter(
                                        x=[prev_time, curr_time],
                                        y=[prev_pdt, curr_pdt],
                                        mode="lines",
                                        name="Discontinuity Connection",
                                        line=dict(width=1, color=color, dash="dot"),
                                        showlegend=False,
                                        legendgroup=playlist_key,
                                        legendgrouptitle_text=legend_name,
                                        hoverinfo="skip",
                                    ),
                                    row=row_num,
                                    col=1,
                                )

                    hover_data = [
                        [
                            format_time_only(d["pdt"]),
                            extract_filename_from_uri(d["uri"]),
                        ]
                        for d in discontinuity_data
                    ]

                    fig.add_trace(
                        go.Scatter(
                            x=[d["request_time"] for d in discontinuity_data],
                            y=[d["pdt"] for d in discontinuity_data],
                            mode="markers",
                            name="Discontinuities",
                            marker=dict(
                                size=10, color=color, symbol="diamond-wide-open"
                            ),
                            hovertemplate="<b>Discontinuity</b><br>"
                            + "<b>PDT:</b> %{customdata[0]}<br>"
                            + "<b>Segment URI:</b> %{customdata[1]}<extra></extra>",
                            customdata=hover_data,
                            legendgroup=playlist_key,
                            legendgrouptitle_text=legend_name,
                        ),
                        row=row_num,
                        col=1,
                    )

            # Add marked segments as overlay markers (toggleable from legend)
            if has_marked_segments:
                marked_data = []
                for dp in data_points:
                    request_time = dp["request_time"]
                    request_id = dp["request_id"]
                    for seg in dp.get("marked_segments", []):
                        marked_data.append(
                            {
                                "request_time": request_time,
                                "request_id": request_id,
                                "pdt": seg["pdt"],
                                "uri": seg.get("uri", ""),
                                "markers": ", ".join(seg.get("markers", [])),
                            }
                        )

                if marked_data:
                    # Add connecting lines between successive manifests for same segments
                    if len(data_points) > 1:
                        sorted_data_points = sorted(
                            data_points, key=lambda dp: dp["request_time"]
                        )

                        for i in range(1, len(sorted_data_points)):
                            prev_dp = sorted_data_points[i - 1]
                            curr_dp = sorted_data_points[i]

                            # Create maps of URI -> (request_time, pdt) for both manifests
                            prev_marked = {
                                seg["uri"]: (prev_dp["request_time"], seg["pdt"])
                                for seg in prev_dp.get("marked_segments", [])
                            }
                            curr_marked = {
                                seg["uri"]: (curr_dp["request_time"], seg["pdt"])
                                for seg in curr_dp.get("marked_segments", [])
                            }

                            # Draw lines for segments that appear in both manifests
                            for uri in prev_marked.keys() & curr_marked.keys():
                                prev_time, prev_pdt = prev_marked[uri]
                                curr_time, curr_pdt = curr_marked[uri]

                                fig.add_trace(
                                    go.Scatter(
                                        x=[prev_time, curr_time],
                                        y=[prev_pdt, curr_pdt],
                                        mode="lines",
                                        name="Marker Connection",
                                        line=dict(width=1, color=color, dash="dot"),
                                        showlegend=False,
                                        legendgroup=playlist_key,
                                        legendgrouptitle_text=legend_name,
                                        hoverinfo="skip",
                                    ),
                                    row=row_num,
                                    col=1,
                                )

                    hover_data = [
                        [
                            format_time_only(d["pdt"]),
                            extract_filename_from_uri(d["uri"]),
                            d["markers"],
                        ]
                        for d in marked_data
                    ]

                    fig.add_trace(
                        go.Scatter(
                            x=[d["request_time"] for d in marked_data],
                            y=[d["pdt"] for d in marked_data],
                            mode="markers",
                            name="Markers",
                            marker=dict(size=8, color=color, symbol="square"),
                            hovertemplate="<b>Markers:</b> %{customdata[2]}<br>"
                            + "<b>PDT:</b> %{customdata[0]}<br>"
                            + "<b>Segment URI:</b> %{customdata[1]}<extra></extra>",
                            customdata=hover_data,
                            legendgroup=playlist_key,
                            legendgrouptitle_text=legend_name,
                        ),
                        row=row_num,
                        col=1,
                    )

    subtitle = build_subtitle(
        service_id, session_id, domain, path, fallback_url=first_hls_url
    )

    total_height = sum(row_heights)
    # Use shared layout builder to align styles with MPD plots
    fig.update_layout(
        **build_common_layout("HLS Live Timeline Analysis", subtitle, total_height)
    )

    # Update x-axis labels
    first_request_time_row = None
    # Determine first row that uses request-time x-axis
    for plot_num in [1, 2, 5]:
        if plot_num in plot_to_row:
            first_request_time_row = plot_to_row[plot_num]
            break

    for plot_num in [1, 2, 5]:
        if plot_num not in plot_to_row:
            continue
        actual_row = plot_to_row[plot_num]

        if plot_num == 5:
            # Plot 5: gets "Request Time" title (last request-time plot)
            if first_request_time_row and actual_row != first_request_time_row:
                matches_ref = (
                    f"x{first_request_time_row}" if first_request_time_row > 1 else "x"
                )
                fig.update_xaxes(
                    title_text="Request Time",
                    title_standoff=0,
                    matches=matches_ref,
                    row=actual_row,
                    col=1,
                    **spike_config(),
                )
            else:
                fig.update_xaxes(
                    title_text="Request Time",
                    title_standoff=0,
                    row=actual_row,
                    col=1,
                    **spike_config(),
                )
        else:
            # Plots 1, 2: empty title, match to first request-time row
            if first_request_time_row and actual_row != first_request_time_row:
                matches_ref = (
                    f"x{first_request_time_row}" if first_request_time_row > 1 else "x"
                )
                fig.update_xaxes(
                    title_text="",
                    matches=matches_ref,
                    row=actual_row,
                    col=1,
                    **spike_config(),
                )
            else:
                fig.update_xaxes(
                    title_text="",
                    row=actual_row,
                    col=1,
                    **spike_config(),
                )

    # Update y-axis labels
    if has_media_sequence and show_media_sequence and 1 in plot_to_row:
        fig.update_yaxes(
            title_text="Sequence Number",
            title_standoff=0,
            row=get_row(1),
            col=1,
        )
    if has_discontinuity_sequence and show_discontinuity_sequence and 2 in plot_to_row:
        fig.update_yaxes(
            title_text="Sequence Number",
            title_standoff=0,
            row=get_row(2),
            col=1,
        )
    if has_segment_spans and show_segment_spans and 5 in plot_to_row:
        fig.update_yaxes(
            title_text="Media Timeline",
            title_standoff=0,
            row=get_row(5),
            col=1,
            autorange="reversed",
        )

    # Add version box in bottom right corner
    add_version_box(fig)

    return fig
