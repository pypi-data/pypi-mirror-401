import os
from importlib.metadata import PackageNotFoundError, version
from importlib.util import find_spec
from pathlib import Path

import click
import tomlkit
from rich.console import Console, Group
from rich.panel import Panel
from rich.rule import Rule
from rich.text import Text

from bpkio_cli.core.app_context import AppContext
from bpkio_cli.core.paths import get_bpkio_home
from bpkio_cli.core.plugin_manager import plugin_manager

console = Console()


def get_package_version(dist_name: str, module_name: str) -> str:
    """
    Get package version from installed package metadata.

    Uses importlib.metadata to find the distribution, but filters to only
    use distributions installed in site-packages (not from source directories
    that might be on sys.path).
    """
    import sys
    from importlib.metadata import distributions

    # Find the distribution, preferring ones in site-packages
    site_packages_candidates = []
    other_candidates = []

    for dist in distributions():
        if dist.name == dist_name:
            # Get distribution path - try different methods depending on Python version
            try:
                if hasattr(dist, "_path"):
                    dist_path = str(dist._path)
                elif hasattr(dist, "locate_file"):
                    dist_path = str(dist.locate_file(""))
                else:
                    # Fallback: use the distribution's files to infer path
                    files = list(dist.files) if hasattr(dist, "files") else []
                    dist_path = str(files[0].locate().parent) if files else ""
            except Exception:
                dist_path = ""
            # Check if it's in a site-packages directory (the venv where we're installed)
            if "site-packages" in dist_path:
                site_packages_candidates.append((dist.version, dist_path))
            else:
                other_candidates.append((dist.version, dist_path))

    # Prefer site-packages versions, fall back to others if needed
    if site_packages_candidates:
        # If multiple site-packages versions, prefer the one matching our venv
        venv_site_packages = str(
            Path(sys.prefix)
            / "lib"
            / f"python{sys.version_info.major}.{sys.version_info.minor}"
            / "site-packages"
        )
        for ver, path in site_packages_candidates:
            if venv_site_packages in path:
                return ver
        # Return the first site-packages version if no venv match
        return site_packages_candidates[0][0]
    elif other_candidates:
        return other_candidates[0][0]

    # Fallback to standard version() call
    try:
        return version(dist_name)
    except PackageNotFoundError:
        pass

    # Last resort: try pyproject.toml
    try:
        module_spec = find_spec(module_name)
        if module_spec and module_spec.origin:
            module_path = Path(module_spec.origin).parent
            for candidate in [
                module_path.parent.parent / "pyproject.toml",
                module_path.parent / "pyproject.toml",
                module_path / "pyproject.toml",
            ]:
                if candidate.exists() and candidate.is_file():
                    try:
                        with open(candidate, "r") as f:
                            toml_data = tomlkit.parse(f.read())
                            pyproject_version = (
                                toml_data.get("tool", {})
                                .get("poetry", {})
                                .get("version")
                            )
                            if pyproject_version:
                                return str(pyproject_version)
                    except Exception:
                        continue
    except Exception:
        pass

    return "unknown"


# Command: DOCTOR
@click.command(hidden=True)
@click.pass_obj
def doctor(obj: AppContext):
    print()

    # Home directory check
    bpkio_home = get_bpkio_home()
    bpkio_home_env = os.environ.get("BPKIO_HOME")
    if bpkio_home_env:
        home_text = Text.from_markup(
            f"[bold]BPKIO_HOME[/bold]: [bold blue]{bpkio_home}[/bold blue]\n"
            f" -> Set via [yellow]BPKIO_HOME[/yellow] environment variable: [magenta]{bpkio_home_env}[/magenta]"
        )
    else:
        default_home = Path.home() / ".bpkio"
        home_text = Text.from_markup(
            f"[bold]BPKIO_HOME[/bold]: [bold blue]{bpkio_home}[/bold blue]\n"
            f" -> Using default location: [magenta]{default_home}[/magenta]"
        )

    home_panel = Panel(
        home_text,
        title="Configuration",
        expand=False,
        border_style="blue",
        title_align="left",
    )
    console.print(home_panel)

    # Module check
    texts = []
    # Map: (display_name, distribution_name, module_name)
    for display_name, dist_name, module_name in [
        ("bpkio_cli", "bpkio-cli", "bpkio_cli"),
        ("bpkio_python_sdk", "bpkio-python-sdk", "bpkio_api"),
        ("media_muncher", "media-muncher", "media_muncher"),
    ]:
        module_spec = find_spec(module_name)
        pkg_version = get_package_version(dist_name, module_name)
        texts.append(
            Text.from_markup(
                f"[bold]{display_name}[/bold] - version: [bold blue]{pkg_version}[/bold blue] \n -> [magenta]{module_spec.origin}[/magenta]"
            )
        )

    module_panel = Panel(
        Group(*texts),
        title="Installed modules",
        expand=False,
        border_style="green",
        title_align="left",
    )
    console.print(module_panel)

    # Mode check
    admin_texts = []
    module_spec = find_spec("bpkio_api_admin")
    if module_spec and module_spec.origin:
        try:
            pkg_version = get_package_version(
                "bpkio-python-sdk-admin", "bpkio_api_admin"
            )
            admin_text = Text.from_markup(
                f"[bold]bpkio-python-sdk-admin[/bold] - version: [bold blue]{pkg_version}[/bold blue] \n -> [magenta]{module_spec.origin}[/magenta]"
            )
            admin_texts.append(admin_text)
        except Exception:
            pass

    module_spec = find_spec("bpkio_cli_admin")
    if module_spec and module_spec.origin:
        try:
            pkg_version = get_package_version("bpkio-cli-admin", "bpkio_cli_admin")
            admin_text = Text.from_markup(
                f"[bold]bpkio-cli-admin[/bold] - version: [bold blue]{pkg_version}[/bold blue] \n -> [magenta]{module_spec.origin}[/magenta]"
            )
            admin_texts.append(admin_text)
        except Exception:
            pass

    if admin_texts:
        admin_panel = Panel(
            Group(*admin_texts),
            title="Admin mode",
            expand=False,
            border_style="red",
            title_align="left",
        )
        console.print(admin_panel)

    if os.environ.get("BIC_MM_ONLY"):
        console.print(
            Panel(
                "Running in Media Muncher only mode",
                width=80,
                border_style="yellow",
                title_align="left",
            )
        )

    # Plugin check - include environment info inside the Plugins panel
    plugin_info = plugin_manager.list_plugins_info()
    plugin_texts = []

    # Add environment info as the first entry
    try:
        if plugin_manager.use_isolated_env:
            env_path = plugin_manager.venv_path or "(unknown)"
            env_markup = (
                f"Plugin env: [bold]isolated[/bold]\n -> [magenta]{env_path}[/magenta]"
            )
        else:
            env_markup = "Plugin env: [bold]shared[/bold] (current Python environment)"
        plugin_texts.append(Text.from_markup(env_markup))
        plugin_texts.append(Rule(style="dim"))
    except Exception:
        # If anything goes wrong fetching env details, continue without env info
        pass

    # Add discovered plugins (if any)
    for plugin_name, plugin_version, status, location in sorted(
        plugin_info, key=lambda x: x[0]
    ):
        status_color = "yellow" if status == "dev" else "green"
        status_label = "[dev]" if status == "dev" else "[installed]"
        if location:
            plugin_texts.append(
                Text.from_markup(
                    f"[bold]{plugin_name}[/bold] - version: [bold blue]{plugin_version}[/bold blue] "
                    f"[{status_color}]{status_label}[/{status_color}] \n -> [magenta]{location}[/magenta]"
                )
            )
        else:
            plugin_texts.append(
                Text.from_markup(
                    f"[bold]{plugin_name}[/bold] - version: [bold blue]{plugin_version}[/bold blue] "
                    f"[{status_color}]{status_label}[/{status_color}]"
                )
            )

    plugin_panel = Panel(
        Group(*plugin_texts),
        title="Plugins",
        expand=False,
        border_style="cyan",
        title_align="left",
    )
    console.print(plugin_panel)
