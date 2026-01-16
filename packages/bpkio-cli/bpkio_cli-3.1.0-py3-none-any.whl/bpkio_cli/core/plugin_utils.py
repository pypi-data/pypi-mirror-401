import importlib.metadata
from pathlib import Path
from typing import Optional

import tomlkit
from loguru import logger


def parse_pyproject_metadata(pyproject_path: Path) -> dict[str, str | list[str]]:
    """
    Parse a pyproject.toml file (Poetry-format) and return a metadata dict.
    Keeps the same shape used by existing code: keys like 'name', 'version',
    'summary', 'author', 'requires-python', 'requires-dist', 'description'.
    """
    metadata: dict[str, str | list[str]] = {}
    try:
        with open(pyproject_path, "r") as f:
            toml = tomlkit.parse(f.read())

        poetry_data = toml.get("tool", {}).get("poetry", {})

        if poetry_data.get("name"):
            metadata["name"] = poetry_data["name"]
        if poetry_data.get("version"):
            metadata["version"] = poetry_data["version"]
        if poetry_data.get("description"):
            metadata["summary"] = poetry_data["description"]
        if poetry_data.get("authors"):
            authors = poetry_data["authors"]
            if isinstance(authors, list) and authors:
                # Poetry authors often look like: ["Name <email>"]
                first = authors[0]
                if "<" in first and ">" in first:
                    name, email = first.rsplit("<", 1)
                    metadata["author"] = name.strip()
                    metadata["author-email"] = email.strip().rstrip(">")
                else:
                    metadata["author"] = ", ".join(authors)
            else:
                metadata["author"] = str(authors)

        deps = poetry_data.get("dependencies", {})
        if "python" in deps:
            metadata["requires-python"] = deps["python"]

        requires_dist = []
        runtime_packages = [
            "bpkio-cli",
            "bpkio-cli-admin",
            "bpkio-python-sdk",
            "bpkio-python-sdk-admin",
        ]
        for dep_name, dep_spec in deps.items():
            if dep_name not in runtime_packages and dep_name != "python":
                requires_dist.append(f"{dep_name} {dep_spec}" if dep_spec else dep_name)
        if requires_dist:
            metadata["requires-dist"] = requires_dist

        # Try to load README as description if configured
        readme_file = poetry_data.get("readme")
        if readme_file:
            readme_path = pyproject_path.parent / readme_file
            if readme_path.exists():
                try:
                    with open(readme_path, "r") as rf:
                        metadata["description"] = rf.read()
                except Exception:
                    pass

        return metadata
    except Exception as e:
        logger.debug(f"Error parsing pyproject.toml at {pyproject_path}: {e}")
        return {}


def find_local_dev_pyproject(
    site_packages: Path, plugin_name: str | None = None
) -> Optional[Path]:
    """
    Scan `site_packages` for `bpkio-dev-*.pth` files and return the matching
    plugin's `pyproject.toml` path. If `plugin_name` is None, returns the first
    pyproject found.
    """
    if not site_packages or not site_packages.is_dir():
        return None

    for pth_file in site_packages.glob("bpkio-dev-*.pth"):
        try:
            pth_plugin_name = pth_file.stem.replace("bpkio-dev-", "")
            if (
                plugin_name
                and pth_plugin_name != plugin_name
                and (
                    plugin_name.startswith("bpkio-cli-plugin-")
                    and pth_plugin_name != plugin_name[len("bpkio-cli-plugin-") :]
                )
            ):
                continue
            src_path_str = pth_file.read_text().strip()
            if not src_path_str:
                continue
            src_path = Path(src_path_str)
            pyproject_path = src_path.parent / "pyproject.toml"
            if pyproject_path.exists():
                return pyproject_path
        except Exception:
            continue
    return None


def normalize_plugin_package_candidates(entry_point_name: str) -> list[str]:
    """
    Given an entry point/name (e.g., 'transcode' or 'mme_support'), return a
    list of plausible distribution package names to try when resolving versions.
    """
    candidates = []
    name = entry_point_name
    if name.startswith("bpkio-cli-plugin-"):
        candidates.append(name)
        base = name[len("bpkio-cli-plugin-") :]
        candidates.append(base)
        candidates.append(base.replace("_", "-"))
    else:
        candidates.append(f"bpkio-cli-plugin-{name}")
        candidates.append(f"bpkio-cli-plugin-{name.replace('_', '-')}")
        candidates.append(name)
        candidates.append(name.replace("_", "-"))
    # keep unique while preserving order
    seen = set()
    out = []
    for c in candidates:
        if c not in seen:
            seen.add(c)
            out.append(c)
    return out


def ensure_plugin_package_name(plugin_name: str) -> tuple[str, str]:
    """
    Given a plugin name (user-provided or entry point), return a tuple of
    (canonical_package_name, base_name).

    Examples:
        - 'transcode' -> ('bpkio-cli-plugin-transcode', 'transcode')
        - 'bpkio-cli-plugin-admin-services' -> ('bpkio-cli-plugin-admin-services', 'admin-services')
    """
    prefix = "bpkio-cli-plugin-"
    if plugin_name.startswith(prefix):
        base = plugin_name[len(prefix) :]
        return plugin_name, base
    return f"{prefix}{plugin_name}", plugin_name


def get_installed_distribution_version(package_name: str) -> Optional[str]:
    """
    Return the installed distribution version for `package_name`, or None if not found.
    """
    try:
        dist = importlib.metadata.distribution(package_name)
        return dist.version
    except Exception:
        return None
