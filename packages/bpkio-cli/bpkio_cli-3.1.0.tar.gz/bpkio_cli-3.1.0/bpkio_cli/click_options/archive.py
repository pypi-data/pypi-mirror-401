import functools

import click
from cloup import option, option_group


def _get_default_archive_format() -> str:
    """Get the default archive format from config, falling back to 'har' if not set."""
    try:
        from bpkio_cli.core.config_provider import CONFIG

        return CONFIG.get("preferred-format", section="archives") or "har"
    except Exception:
        return "har"


def _format_option(required: bool = False, default: str = None):
    """Helper function that creates a format option definition.

    Args:
        required: Whether the format option is required (default: False)
        default: Default format value. If None, uses config value from archives.preferred-format

    Returns:
        An option definition for the format option
    """
    if default is None:
        default = _get_default_archive_format()
    return option(
        "--format",
        "-f",
        type=click.Choice(["har", "proxyman", "proxymanlogv2"]),
        required=required,
        default=default,
        help="Output format for the exported archive",
    )


def _annotate_option():
    """Helper function that creates an annotate option definition.

    Returns:
        An option definition for the annotate option
    """
    return option(
        "--annotate",
        "-a",
        is_flag=True,
        default=False,
        help="Annotate manifest content with parsed metadata (adds comments to HLS/DASH files)",
    )


def _inline_option():
    """Helper function that creates an inline option definition.

    Returns:
        An option definition for the inline option
    """
    return option(
        "--inline/--no-inline",
        "inline",
        is_flag=True,
        default=True,
        help="Insert annotations inline in the body content (default: True). Use --no-inline to keep original body unchanged.",
    )


def archive_format_option(required: bool = False, default: str = None):
    """Decorator that adds a --format option for archive export formats.

    Args:
        required: Whether the format option is required (default: False)
        default: Default format value. If None, uses config value from archives.preferred-format

    Returns:
        A decorator function that adds the format option
    """

    def decorator(fn):
        @_format_option(required=required, default=default)
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)

        return wrapper

    return decorator


def archive_annotate_option(fn):
    """Decorator that adds --annotate and --inline options for annotating archive entries.

    Adds metadata annotations (comments) to HLS/DASH manifest content.
    """

    @_inline_option()
    @_annotate_option()
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)

    return wrapper


def archive_options(required_format: bool = False, default_format: str = None):
    """Decorator that adds --format, --annotate, and --inline options for archive commands.

    Args:
        required_format: Whether the format option is required (default: False)
        default_format: Default format value. If None, uses config value from archives.preferred-format

    Returns:
        A decorator function that adds archive options
    """

    def decorator(fn):
        @option_group(
            "Archive export options",
            _format_option(required=required_format, default=default_format),
            _annotate_option(),
            _inline_option(),
        )
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)

        return wrapper

    return decorator
