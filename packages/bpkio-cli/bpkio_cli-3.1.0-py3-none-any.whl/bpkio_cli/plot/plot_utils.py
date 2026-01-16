"""Common utilities for plotting validation scripts."""

from datetime import datetime
from pathlib import Path

import plotly.express as px
import plotly.graph_objects as go
from plotly.graph_objs import Figure

try:
    from bpkio_cli import __version__
except ImportError:
    __version__ = "unknown"


def extract_filename_from_uri(uri: str) -> str:
    """Extract just the filename (last path segment) from a URI, removing query parameters.

    Also removes any substring starting with '/bpk-sst/' from the path before extraction.
    """
    if not uri:
        return ""
    # Remove query parameters
    uri_without_query = uri.split("?")[0]

    # Remove any substring starting with '/bpk-sst/' from the path
    if "/bpk-sst/" in uri_without_query:
        # Find the position of '/bpk-sst/' and remove everything from that point
        bpk_sst_pos = uri_without_query.find("/bpk-sst/")
        if bpk_sst_pos != -1:
            # Keep everything before '/bpk-sst/'
            uri_without_query = uri_without_query[:bpk_sst_pos]

    # Get the last path segment
    filename = uri_without_query.split("/")[-1]
    return filename


def format_time_only(dt: datetime) -> str:
    """Format datetime to HH:MM:SS.ms format without date."""
    if dt is None:
        return ""
    return dt.strftime("%H:%M:%S.%f")[:-3]  # Remove last 3 digits to get milliseconds


def get_color_palette():
    """Get the custom color palette for periods/playlists.

    Returns:
        List of color strings from Plotly qualitative palettes
    """
    return [
        px.colors.qualitative.Plotly[0],
        px.colors.qualitative.Plotly[2],
        px.colors.qualitative.Plotly[3],
        # px.colors.qualitative.Plotly[4],
        px.colors.qualitative.Plotly[5],
        px.colors.qualitative.Plotly[6],
        px.colors.qualitative.G10[4],
    ]


def build_common_layout(title: str, subtitle: str | None, total_height: int) -> dict:
    """Build a common Plotly layout dict used by both MPD and HLS plots.

    Returns a dictionary suitable to pass to `fig.update_layout(**layout_dict)`.
    """
    layout_dict = {
        "height": total_height,
        "showlegend": True,
        "hovermode": "closest",
        "hoversubplots": "axis",
        "legend": dict(indentation=20),
        "modebar_add": [
            "toggleSpikeLines",
            "toggleSpikes",
            "toggleRangeSelector",
            "toggleHover",
            "toggleSpikey",
        ],
    }
    if subtitle:
        layout_dict["title"] = {"text": title, "subtitle": {"text": subtitle}}
    else:
        layout_dict["title"] = title
    return layout_dict


def build_subtitle(
    service_id: str | None,
    session_id: str | None,
    domain: str | None,
    path: str | None,
    fallback_url=None,
) -> str | None:
    """Build a subtitle string preferring service/session IDs when available.

    Rules:
    - If both `service_id` and `session_id` are present, return "Service ID: X | Session ID: Y".
    - Else if `domain` and `path` are present, return "Domain: D | Path: P".
    - Else if `fallback_url` (a yarl.URL-like object) is provided, attempt to extract query params and host/path.
    - Otherwise return None.
    """
    if service_id and session_id:
        return f"<b>Service ID</b>: {service_id} | <b>Session ID</b>: {session_id}"
    if domain and path:
        return f"<b>Domain</b>: {domain} | <b>Path</b>: {path}"
    if fallback_url is not None:
        try:
            bpkio_sessionid = fallback_url.query.get("bpkio_sessionid")
            bpkio_serviceid = fallback_url.query.get("bpkio_serviceid")
            if bpkio_serviceid and bpkio_sessionid:
                return f"<b>Service ID</b>: {bpkio_serviceid} | <b>Session ID</b>: {bpkio_sessionid}"
            # fallback to host/path if query params not both present
            return (
                f"<b>Domain</b>: {fallback_url.host} | <b>Path</b>: {fallback_url.path}"
            )
        except Exception:
            return None
    return None


def spike_config() -> dict:
    """Return a dict with standardized spike settings for axes."""
    return {
        "showspikes": True,
        "spikemode": "across",
        "spikesnap": "cursor",
        "spikedash": "solid",
        "spikethickness": 1,
        "spikecolor": "gray",
    }


# JavaScript code for vertical crosshair functionality (spans all subplots)
CROSSHAIR_JS = """
    <script>
    (function() {
        function addCrosshair() {
            const plotDivs = document.querySelectorAll('.plotly');
            plotDivs.forEach(function(plotDiv) {
                // Check if crosshair already exists
                if (plotDiv.querySelector('#crosshair-line-vertical')) return;
                
                // Create vertical crosshair line element
                const crosshairVertical = document.createElement('div');
                crosshairVertical.id = 'crosshair-line-vertical';
                crosshairVertical.style.position = 'absolute';
                crosshairVertical.style.width = '2px';
                crosshairVertical.style.backgroundColor = 'rgba(128, 128, 128, 0.5)';
                crosshairVertical.style.pointerEvents = 'none';
                crosshairVertical.style.display = 'none';
                crosshairVertical.style.zIndex = '1000';
                crosshairVertical.style.top = '0px';
                
                plotDiv.style.position = 'relative';
                plotDiv.appendChild(crosshairVertical);
                
                // Track mouse position
                plotDiv.addEventListener('mousemove', function(e) {
                    const rect = plotDiv.getBoundingClientRect();
                    const mouseX = e.clientX - rect.left;
                    
                    // Update vertical line (full height)
                    crosshairVertical.style.left = mouseX + 'px';
                    crosshairVertical.style.height = plotDiv.offsetHeight + 'px';
                    crosshairVertical.style.display = 'block';
                });
                
                plotDiv.addEventListener('mouseleave', function() {
                    crosshairVertical.style.display = 'none';
                });
            });
        }
        
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', addCrosshair);
        } else {
            addCrosshair();
        }
        
        // Also try after a short delay in case Plotly hasn't rendered yet
        setTimeout(addCrosshair, 500);
    })();
    </script>
    """


def save_plot_with_crosshair(fig: Figure, output_path: str | None = None):
    """Save plot to file with crosshair functionality.

    Args:
        fig: Plotly figure object
        output_path: Optional path to save HTML file. If None, saves to mpd_sequence_plot.html
    """
    if output_path is None:
        output_path = "mpd_sequence_plot.html"

    html_str = fig.to_html(
        include_plotlyjs="cdn",
        config={
            "scrollZoom": True,
            "modeBarButtonsToAdd": [
                "drawline",
                "drawopenpath",
                "drawclosedpath",
                "drawcircle",
                "drawrect",
                "eraseshape",
                "v1hovermode",
                "hoverclosest",
                "hovercompare",
                "togglespikelines",
            ],
        },
    )
    html_str = html_str.replace("</body>", CROSSHAIR_JS + "</body>")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_str)

    return Path(output_path).absolute()


def add_error_line(
    fig,
    error_x,
    y_bottom,
    y_top,
    row,
    col=1,
    error_message: str = None,
    error_time_str: str = None,
):
    """Add a vertical error line to a plot with consistent styling.

    Args:
        fig: Plotly figure object
        error_x: X coordinate for the error line
        y_bottom: Bottom Y coordinate
        y_top: Top Y coordinate
        row: Subplot row number
        col: Subplot column number (default: 1)
        error_message: Optional error message for hover tooltip
        error_time_str: Optional formatted time string for hover tooltip
    """
    if error_message and error_time_str:
        hovertemplate = (
            f"<b>{error_message}</b><br>"
            + "<b>Request Time:</b> "
            + error_time_str
            + "<br>"
            + "<extra></extra>"
        )
    else:
        hovertemplate = "<extra></extra>"

    fig.add_trace(
        go.Scatter(
            x=[error_x, error_x],
            y=[y_bottom, y_top],
            mode="lines",
            name="Error",
            line=dict(color="rgba(255, 0, 0, 0.5)", width=5),
            showlegend=False,
            hovertemplate=hovertemplate,
        ),
        row=row,
        col=col,
    )


def add_subplot_title(
    fig: Figure, enabled_plots: list, plot_to_row: dict, plot_metadata: dict
):
    """Add annotations for each subplot using positions from plot_metadata.

    Position in plot_metadata should be one of:
    - "top-left": top-left corner of subplot
    - "top-right": top-right corner of subplot
    - "bottom-left": bottom-left corner of subplot
    - "bottom-right": bottom-right corner of subplot
    - "above-left": above the subplot, aligned left
    - "above-right": above the subplot, aligned right

    Args:
        fig: Plotly figure object
        enabled_plots: List of plot numbers that are enabled
        plot_to_row: Dict mapping plot number to subplot row number
        plot_metadata: Dict with plot configuration including 'position' and 'title'
    """
    for plot_num in enabled_plots:
        position = plot_metadata[plot_num].get("position", "top-right")
        title = plot_metadata[plot_num].get("title", "")
        row = plot_to_row[plot_num]

        # Get subplot's domain in paper coordinates
        # For row 1, axis is 'xaxis' and 'yaxis'; for row 2+, it's 'xaxis2', 'yaxis2', etc.
        xaxis_name = f"xaxis{row}" if row > 1 else "xaxis"
        yaxis_name = f"yaxis{row}" if row > 1 else "yaxis"

        xaxis_domain = fig.layout[xaxis_name].domain or [0, 1]
        yaxis_domain = fig.layout[yaxis_name].domain or [0, 1]

        # Parse position string and set coordinates, anchors, and shifts
        if position == "top-right":
            rel_x, rel_y = 1.0, 1.0
            xanchor, yanchor = "right", "top"
            xshift, yshift = -8, -8
        elif position == "top-left":
            rel_x, rel_y = 0.0, 1.0
            xanchor, yanchor = "left", "top"
            xshift, yshift = 8, -8
        elif position == "bottom-right":
            rel_x, rel_y = 1.0, 0.0
            xanchor, yanchor = "right", "bottom"
            xshift, yshift = -8, 8
        elif position == "bottom-left":
            rel_x, rel_y = 0.0, 0.0
            xanchor, yanchor = "left", "bottom"
            xshift, yshift = 8, 8
        elif position == "above-left":
            rel_x, rel_y = 0.0, 1.0
            xanchor, yanchor = "left", "bottom"
            xshift, yshift = 8, -4
        elif position == "above-right":
            rel_x, rel_y = 1.0, 1.0
            xanchor, yanchor = "right", "bottom"
            xshift, yshift = -8, -4
        elif position == "left":
            # Place annotation to the left of the subplot, vertically centered
            rel_x, rel_y = 0.0, 0.5
            xanchor, yanchor = "right", "middle"
            xshift, yshift = -8, 0
        else:
            # Default to top-right if unknown position
            rel_x, rel_y = 1.0, 1.0
            xanchor, yanchor = "right", "top"
            xshift, yshift = -8, -8

        # Calculate position in paper coordinates relative to subplot domain
        paper_x = xaxis_domain[0] + rel_x * (xaxis_domain[1] - xaxis_domain[0])
        paper_y = yaxis_domain[0] + rel_y * (yaxis_domain[1] - yaxis_domain[0])

        fig.add_annotation(
            text=title,
            x=paper_x,
            y=paper_y,
            xref="paper",
            yref="paper",
            xanchor=xanchor,
            yanchor=yanchor,
            showarrow=False,
            font=dict(size=14, color="rgba(0, 0, 0, 0.8)"),
            bgcolor="rgba(255, 255, 255, 0.85)",
            bordercolor="rgba(0, 0, 0, 0.3)",
            borderwidth=1,
            borderpad=4,
            xshift=xshift,
            yshift=yshift,
        )


def add_version_box(fig: Figure):
    """Add a version box annotation in the bottom right corner of the entire plot area.

    The annotation appears below the legend area, positioned at the bottom right
    of the whole figure, not within any subplot.

    Args:
        fig: Plotly figure object to add the version box to
    """
    # Get existing annotations or create empty list
    existing_annotations = (
        list(fig.layout.annotations) if fig.layout.annotations else []
    )

    # Create the version annotation as a dictionary
    version_annotation = dict(
        text=f"bpkio-cli v{__version__}",
        xref="paper",
        yref="paper",
        x=1.0,  # Slightly inset from right edge
        y=0.0,  # Slightly above bottom edge
        # xshift=150,  # push into the right margin (pixels)
        xshift=10,
        yshift=-50,
        xanchor="left",
        yanchor="bottom",
        showarrow=False,
        bgcolor="rgba(255, 255, 255, 0.85)",
        bordercolor="rgba(0, 0, 0, 0.3)",
        borderwidth=1,
        borderpad=5,
        font=dict(size=10, color="rgba(0, 0, 0, 0.7)"),
    )

    # Add to existing annotations and update layout
    existing_annotations.append(version_annotation)
    fig.update_layout(annotations=existing_annotations)
