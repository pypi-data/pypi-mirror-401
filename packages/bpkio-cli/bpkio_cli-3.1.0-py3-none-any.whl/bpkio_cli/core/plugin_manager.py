import importlib
import importlib.metadata
import os
import site
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

import tomlkit
from bpkio_cli.core.paths import get_bpkio_home
from bpkio_cli.core.plugin_utils import (
    find_local_dev_pyproject,
    get_installed_distribution_version,
    normalize_plugin_package_candidates,
    parse_pyproject_metadata,
)
from loguru import logger

BPKIO_HOME = get_bpkio_home()
# Plugin environment mode:
# - "shared" (default): plugins are installed into the same Python environment as the CLI (sys.executable)
# - "isolated": plugins are installed into a dedicated venv under ~/.bpkio/plugins-env
#
# NOTE: "isolated" is still supported (and useful for strong isolation / dev),
# but "shared" is the recommended production default.
PLUGINS_ENV_MODE = os.getenv("BPKIO_PLUGINS_ENV_MODE", "shared").strip().lower()
# Allow override via environment variable for testing/isolated environments
PLUGINS_ENV_PATH = Path(
    os.getenv("BPKIO_PLUGINS_ENV_PATH", str(BPKIO_HOME / "plugins-env"))
).expanduser()
PLUGINS_SOURCE_DIR = "bpkio-cli-plugins"


class PluginManager:
    """
    Manages the plugin virtual environment, discovery of plugins,
    and installation of dependencies.

    Provides utilities to locate site-packages, discover entry points,
    and query installed plugin metadata (including local dev plugins).
    """

    def get_installed_plugin_version(self, package_name: str) -> str | None:
        """
        Get the installed version of a plugin, checking both installed packages and local dev.
        Returns the version string or None if not found.
        """
        # First check if it's a local dev plugin
        site_packages = self.get_site_packages_path()
        pyproject_path = (
            find_local_dev_pyproject(site_packages, package_name)
            if site_packages
            else None
        )
        if pyproject_path:
            metadata = parse_pyproject_metadata(pyproject_path)
            if metadata and metadata.get("version"):
                return metadata["version"]

        # Otherwise, try to get from installed package using plausible candidates
        for candidate in normalize_plugin_package_candidates(package_name):
            try:
                self._add_plugin_env_to_path()
                v = get_installed_distribution_version(candidate)
                if v:
                    return v
            except Exception:
                continue
        return None

    def _find_local_dev_plugin(self, plugin_name: str) -> Path | None:
        # Deprecated: use find_local_dev_pyproject in plugin_utils instead.
        site_packages = self.get_site_packages_path()
        return (
            find_local_dev_pyproject(site_packages, plugin_name)
            if site_packages
            else None
        )

    def _get_metadata_from_pyproject(
        self, pyproject_path: Path
    ) -> dict[str, str | list[str]]:
        # Deprecated: delegate to parse_pyproject_metadata
        return parse_pyproject_metadata(pyproject_path)

    def __init__(self, env_path: str | Path = PLUGINS_ENV_PATH):
        self.env_mode = PLUGINS_ENV_MODE
        self.use_isolated_env = self.env_mode != "shared"

        self.venv_path: Path | None = None
        self.python_executable: Path | None = None

        if self.use_isolated_env:
            self.venv_path = Path(env_path).expanduser()
            self.python_executable = self.venv_path / "bin" / "python"
            self.ensure_venv()
        else:
            # Shared mode: use the current interpreter environment.
            self.python_executable = Path(sys.executable)
        self._services = None

    def get_pip_path(self) -> Path:
        """Returns the path to the pip executable in the venv."""
        if not self.use_isolated_env:
            # In shared mode we intentionally do not return a "pip" path, because
            # installing should be done via: [sys.executable, -m, pip, ...]
            return Path()
        assert self.venv_path is not None
        return self.venv_path / "bin" / "pip"

    def get_pip_command(self) -> list[str]:
        """
        Returns the pip invocation to use for installing plugins.
        - isolated: ["<plugins-venv>/bin/pip"]
        - shared:   ["<sys.executable>", "-m", "pip"]
        """
        if self.use_isolated_env:
            pip_exe = self.get_pip_path()
            return [str(pip_exe)]
        return [sys.executable, "-m", "pip"]

    def ensure_venv(self):
        """
        Ensures that the virtual environment exists, creating it if necessary.
        """
        if not self.use_isolated_env:
            return
        assert self.venv_path is not None
        assert self.python_executable is not None

        if not self.venv_path.is_dir() or not self.python_executable.is_file():
            logger.warning(
                f"Plugin virtual environment not found. Creating at: {self.venv_path}"
            )
            try:
                # Using the current python executable to create the venv
                subprocess.run(
                    [sys.executable, "-m", "venv", str(self.venv_path)], check=True
                )
                logger.info("Plugin virtual environment created successfully.")
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to create virtual environment: {e}")
                sys.exit(1)

    def get_site_packages_path(self) -> Path | None:
        """
        Gets the site-packages path for the plugin venv by asking the venv's python.
        This is more reliable than using the main process's `site` module.
        """
        if not self.python_executable or not self.python_executable.is_file():
            return None

        # Shared mode: use current env site-packages.
        if not self.use_isolated_env:
            try:
                return Path(site.getsitepackages()[0])
            except Exception:
                # Fall back to sys.path heuristic (best-effort).
                for p in sys.path:
                    if p.endswith("site-packages"):
                        return Path(p)
                return None

        command = [
            str(self.python_executable),
            "-c",
            "import site; print(site.getsitepackages()[0])",
        ]
        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            return Path(result.stdout.strip())
        except subprocess.CalledProcessError as e:
            logger.error(
                f"Could not determine site-packages for {self.venv_path}: {e.stderr}"
            )
            return None

    def _add_plugin_env_to_path(self):
        """
        Adds the plugin environment's site-packages directory to sys.path
        to make installed plugins importable. Also discovers .pth files for dev mode.
        """
        site_packages = self.get_site_packages_path()
        if site_packages and site_packages.is_dir():
            # In shared mode, site-packages is already on sys.path; in isolated mode, we need to add it.
            if self.use_isolated_env and str(site_packages) not in sys.path:
                logger.debug(
                    f"Adding plugin site-packages to sys.path: {site_packages}"
                )
                sys.path.insert(0, str(site_packages))

            # Discover .pth files for dev mode plugins
            for pth_file in site_packages.glob("*.pth"):
                if pth_file.name.startswith("bpkio-dev-"):
                    try:
                        dev_path_str = pth_file.read_text().strip()
                        if dev_path_str and dev_path_str not in sys.path:
                            logger.debug(
                                f"Found dev plugin path in {pth_file.name}: {dev_path_str}"
                            )
                            sys.path.insert(0, dev_path_str)
                    except Exception as e:
                        logger.warning(
                            f"Could not read or process .pth file {pth_file}: {e}"
                        )

    def _discover_entry_points_from_pth(self, entry_point_group: str):
        """
        A generic generator that discovers entry points from local development
        plugins by parsing their .pth and pyproject.toml files.

        Args:
            entry_point_group (str): The entry point group to scan for (e.g., 'bic.plugins').

        Yields:
            A tuple of (name, loaded_object) for each discovered entry point.
        """
        site_packages = self.get_site_packages_path()
        if not site_packages or not site_packages.is_dir():
            return

        logger.debug(
            f"Scanning for local dev .pth files for group '{entry_point_group}'..."
        )
        for pth_file in site_packages.glob("bpkio-dev-*.pth"):
            try:
                src_path_str = pth_file.read_text().strip()
                if not src_path_str:
                    continue

                src_path = Path(src_path_str)
                pyproject_path = src_path.parent / "pyproject.toml"
                if not pyproject_path.exists():
                    continue

                with open(pyproject_path, "r") as pf:
                    toml = tomlkit.parse(pf.read())
                    entry_points = (
                        toml.get("tool", {})
                        .get("poetry", {})
                        .get("plugins", {})
                        .get(entry_point_group, {})
                    )
                    for name, path_str in entry_points.items():
                        module_path, obj_name = path_str.split(":")
                        if str(src_path) not in sys.path:
                            sys.path.insert(0, str(src_path))

                        module = importlib.import_module(module_path)
                        loaded_obj = getattr(module, obj_name)
                        logger.debug(
                            f"Manually discovered dev entry point: {name} in group {entry_point_group}"
                        )
                        yield name, loaded_obj
            except Exception as e:
                logger.warning(
                    f"Could not manually parse entry points from {pth_file} for group {entry_point_group}: {e}"
                )

    def _discover_from_pth_files(self) -> list:
        """
        Fallback discovery method for local development commands.
        """
        commands = []
        for name, loaded_obj in self._discover_entry_points_from_pth("bic.plugins"):
            if isinstance(loaded_obj, list):
                commands.extend(loaded_obj)
            else:
                commands.append(loaded_obj)
        return commands

    def _discover_services_from_pth_files(self) -> dict:
        """
        Fallback discovery for local development services.
        """
        services = {}
        for name, loaded_obj in self._discover_entry_points_from_pth("bic.services"):
            services[name] = loaded_obj
        return services

    @lru_cache(maxsize=None)
    def discover_services(self) -> dict:
        """
        Discovers all services by looking for entry points in the 'bic.services' group.
        It first ensures the venv path is added to the system path.
        """
        self._add_plugin_env_to_path()
        all_services = {}

        logger.debug("Discovering services via 'bic.services' entry points...")
        try:
            for ep in importlib.metadata.entry_points(group="bic.services"):
                logger.debug(f"Loading service: {ep.name}")
                all_services[ep.name] = ep.load()
        except Exception as e:
            logger.error(f"Error discovering services via entry points: {e}")

        # Fallback for local development plugins
        try:
            manual_services = self._discover_services_from_pth_files()
            for name, func in manual_services.items():
                if name not in all_services:
                    all_services[name] = func
        except Exception as e:
            logger.error(f"Error in manual service discovery: {e}")

        logger.debug(f"Discovered {len(all_services)} total services.")
        self._services = all_services
        return self._services

    def get_service(self, name: str, optional: bool = False):
        """
        Retrieves a shared function (service) provided by an installed plugin.
        Services are discovered on the first call and cached.
        """
        if self._services is None:
            self.discover_services()

        service_func = self._services.get(name)
        if not service_func and not optional:
            from bpkio_cli.core.exceptions import BroadpeakIoCliError

            raise BroadpeakIoCliError(f"Required service '{name}' could not be found.")
        return service_func

    @lru_cache(maxsize=None)
    def discover_commands(self) -> list:
        """
        Discovers all plugins by looking for entry points in the 'bic.plugins' group.
        It first ensures the venv path is added to the system path.
        """
        self._add_plugin_env_to_path()

        all_commands = []
        discovered_names = set()

        # Standard discovery for installed packages
        logger.debug("Discovering plugins via 'bic.plugins' entry points...")
        try:
            for ep in importlib.metadata.entry_points(group="bic.plugins"):
                loaded_obj = ep.load()
                if isinstance(loaded_obj, list):
                    all_commands.extend(loaded_obj)
                else:
                    all_commands.append(loaded_obj)
                discovered_names.add(ep.name)
        except Exception as e:
            logger.error(f"Error discovering plugins via entry points: {e}")

        # Fallback discovery for local dev plugins linked by .pth files
        try:
            manual_commands = self._discover_from_pth_files()
            # Create a set of names from already discovered commands for efficient checking
            discovered_command_names = {
                cmd.name for cmd in all_commands if hasattr(cmd, "name")
            }
            for command in manual_commands:
                if (
                    hasattr(command, "name")
                    and command.name not in discovered_command_names
                ):
                    all_commands.append(command)
                    # No need to add to discovered_names, as that's for entry point names
        except Exception as e:
            logger.error(f"Error in manual plugin discovery: {e}")

        logger.debug(f"Discovered {len(all_commands)} total plugin commands.")
        return all_commands

    def list_plugins_info(self) -> list:
        """
        Return a list of plugin information tuples: (plugin_name, version, status, location)
        where status is 'installed' or 'dev'. This consolidates logic previously in
        the doctor command and provides a single source of truth.
        """
        plugin_info = []

        # Installed plugins via entry points
        try:
            self._add_plugin_env_to_path()
            for ep in importlib.metadata.entry_points(group="bic.plugins"):
                plugin_name = ep.name
                # Try common package names
                version_str = self.get_installed_plugin_version(
                    f"bpkio-cli-plugin-{plugin_name}"
                )
                if not version_str:
                    version_str = self.get_installed_plugin_version(plugin_name)
                dist_location = None
                try:
                    dist = importlib.metadata.distribution(
                        f"bpkio-cli-plugin-{plugin_name}"
                    )
                    if hasattr(dist, "_path"):
                        dist_location = str(dist._path)
                    elif hasattr(dist, "locate_file"):
                        dist_location = str(dist.locate_file(""))
                except Exception:
                    pass
                plugin_info.append(
                    (plugin_name, version_str or "unknown", "installed", dist_location)
                )
        except Exception:
            pass

        # Dev plugins via .pth files
        site_packages = self.get_site_packages_path()
        if site_packages and site_packages.is_dir():
            for pth_file in site_packages.glob("bpkio-dev-*.pth"):
                try:
                    pth_plugin_name = pth_file.stem.replace("bpkio-dev-", "")
                    src_path_str = pth_file.read_text().strip()
                    if not src_path_str:
                        continue

                    src_path = Path(src_path_str)
                    pyproject_path = src_path.parent / "pyproject.toml"
                    if not pyproject_path.exists():
                        continue

                    try:
                        # Use the shared pyproject parser to extract metadata
                        metadata = parse_pyproject_metadata(pyproject_path)
                        plugin_version = metadata.get("version", "unknown")
                        package_name = metadata.get("name")

                        # Try to extract entry point names as a best-effort fallback
                        entry_point_names = []
                        try:
                            with open(pyproject_path, "r") as pf:
                                toml = tomlkit.parse(pf.read())
                                entry_points = (
                                    toml.get("tool", {})
                                    .get("poetry", {})
                                    .get("plugins", {})
                                    .get("bic.plugins", {})
                                )
                                if entry_points:
                                    entry_point_names = list(entry_points.keys())
                        except Exception:
                            entry_point_names = []

                        # Check existing entries and prefer to mark them as 'dev'
                        existing_idx = None
                        for idx, (name, _, status, _) in enumerate(plugin_info):
                            if (
                                name == pth_plugin_name
                                or (package_name and name in package_name)
                                or name in entry_point_names
                            ):
                                existing_idx = idx
                                break

                        plugin_version_str = (
                            str(plugin_version) if plugin_version else "unknown"
                        )
                        location = str(src_path.parent)
                        display_name = (
                            entry_point_names[0]
                            if entry_point_names
                            else (metadata.get("name") or pth_plugin_name)
                        )

                        if existing_idx is not None:
                            plugin_info[existing_idx] = (
                                display_name,
                                plugin_version_str,
                                "dev",
                                location,
                            )
                        else:
                            plugin_info.append(
                                (display_name, plugin_version_str, "dev", location)
                            )
                    except Exception:
                        plugin_info.append(
                            (pth_plugin_name, "unknown", "dev", str(src_path.parent))
                        )
                except Exception:
                    continue

        return plugin_info


# Create a single, shared instance of the PluginManager for the entire application.
# This ensures that it's available early in the startup process and that all
# parts of the CLI use the same instance, avoiding circular dependencies.
plugin_manager = PluginManager()
