from __future__ import annotations

import re
import subprocess
import sys
import urllib
from dataclasses import dataclass

from loguru import logger
from packaging.utils import canonicalize_name
from packaging.version import InvalidVersion, Version

DEFAULT_EXTRA_INDEX_URL = "https://pypi.org/simple"


def get_cli_pip_command() -> list[str]:
    """Pip command for the *current* interpreter environment (the CLI env)."""
    return [sys.executable, "-m", "pip"]


def normalize_pep503_repo_url(repo_url: str) -> str:
    """
    Normalize a PEP 503 repository URL.
    - Remove /index.html if present
    - Ensure it ends with a single trailing slash
    """
    normalized = repo_url.rstrip("/")
    if normalized.endswith("/index.html"):
        normalized = normalized[:-10]
    return normalized + "/"


@dataclass(frozen=True)
class PipRunResult:
    returncode: int
    stdout: str
    stderr: str


def run_pip(
    pip_cmd: list[str],
    args: list[str],
    *,
    check: bool = False,
    timeout: float | None = None,
) -> PipRunResult:
    cmd = [*pip_cmd, *args]
    logger.debug(f"Running pip: {' '.join(cmd)}")
    proc = subprocess.run(
        cmd,
        text=True,
        capture_output=True,
        check=False,
        timeout=timeout,
    )
    if check and proc.returncode != 0:
        raise subprocess.CalledProcessError(
            proc.returncode, cmd, output=proc.stdout, stderr=proc.stderr
        )
    return PipRunResult(proc.returncode, proc.stdout or "", proc.stderr or "")


def get_latest_version_from_pip_index(pip_cmd: list[str], package: str) -> str | None:
    """
    Best-effort "latest version" by asking pip which versions are available.

    Notes:
    - Respects user pip configuration (indexes, auth, etc.)
    - Output format varies across pip versions; we parse a few common patterns.
    """
    res = run_pip(pip_cmd, ["index", "versions", package], check=False, timeout=30)
    if res.returncode != 0:
        return None

    text = "\n".join([res.stdout, res.stderr])

    # Common pip output patterns:
    # - "AVAILABLE VERSIONS: 3.2.1, 3.2.0, ..."
    # - "Available versions: 3.2.1, 3.2.0, ..."
    m = re.search(
        r"available versions:\s*(.+)$", text, flags=re.IGNORECASE | re.MULTILINE
    )
    if m:
        versions_part = m.group(1).strip()
        first = versions_part.split(",")[0].strip()
        return first or None

    # Some pip versions print:
    # "bpkio-cli (3.2.1) - ..." or "LATEST: 3.2.1"
    m = re.search(r"\bLATEST:\s*([0-9][^\s,)]*)", text, flags=re.IGNORECASE)
    if m:
        return m.group(1).strip()

    m = re.search(
        rf"^{re.escape(package)}\s*\(([^)]+)\)",
        text,
        flags=re.IGNORECASE | re.MULTILINE,
    )
    if m:
        return m.group(1).strip()

    return None


def pip_install_from_repos(
    *,
    pip_cmd: list[str],
    package_spec: str,
    repos: dict[str, str] | None,
    upgrade: bool = True,
    isolated: bool = True,
    constraints_file: str | None = None,
    extra_index_url: str = DEFAULT_EXTRA_INDEX_URL,
) -> None:
    """
    Install/upgrade a package, trying configured PEP503 repos in order.

    If repos is empty/None, falls back to default pip indexes.
    """
    base_args = ["install"]
    if upgrade:
        base_args.append("--upgrade")
    if isolated:
        base_args.append("--isolated")
    if constraints_file:
        base_args += ["-c", constraints_file]

    if not repos:
        args = [*base_args, package_spec]
        if extra_index_url:
            args += ["--extra-index-url", extra_index_url]
        run_pip(pip_cmd, args, check=True)
        return

    # Allow callers to pass an ordered dict of preferred repositories
    last_err: subprocess.CalledProcessError | None = None
    for repo_label, repo_url in repos.items():
        normalized = normalize_pep503_repo_url(repo_url)
        args = [*base_args, "--index-url", normalized, package_spec]
        if extra_index_url:
            args += ["--extra-index-url", extra_index_url]
        try:
            run_pip(pip_cmd, args, check=True)
            return
        except subprocess.CalledProcessError as e:
            last_err = e
            continue

    assert last_err is not None
    raise last_err


def get_package_versions(
    pip_cmd: list[str], package_name: str, repo_url: str | None = None
) -> list[str]:
    """
    Fetch available versions for a package from a PEP 503 repository using pip.
    Returns a list of version strings, sorted in descending order.

    If repo_url is None, uses default pip indexes.
    """
    args = ["index", "versions", package_name]
    if repo_url:
        normalized = normalize_pep503_repo_url(repo_url)
        args += ["--index-url", normalized]

    res = run_pip(pip_cmd, args, check=False, timeout=30)
    if res.returncode != 0:
        repo_info = f" in repo {repo_url}" if repo_url else ""
        logger.debug(f"Package '{package_name}' not found{repo_info}")
        return []

    text = "\n".join([res.stdout, res.stderr])

    # Parse versions from pip output
    # Common patterns:
    # - "AVAILABLE VERSIONS: 3.2.1, 3.2.0, 2.1.0"
    # - "Available versions: 3.2.1, 3.2.0, 2.1.0"
    m = re.search(
        r"available versions:\s*(.+)$", text, flags=re.IGNORECASE | re.MULTILINE
    )
    if m:
        versions_part = m.group(1).strip()
        # Split by comma and clean up
        version_strings = [v.strip() for v in versions_part.split(",")]
        versions = []
        for v_str in version_strings:
            try:
                Version(v_str)
                versions.append(v_str)
            except InvalidVersion:
                continue
        # Sort in descending order
        if versions:
            versions.sort(key=lambda v: Version(v), reverse=True)
        repo_info = f" in repo {repo_url}" if repo_url else ""
        logger.debug(
            f"Found {len(versions)} version(s) for '{package_name}'{repo_info}: {', '.join(versions[:5])}"
            + (f" ... ({len(versions)} total)" if len(versions) > 5 else "")
        )
        return versions

    repo_info = f" in repo {repo_url}" if repo_url else ""
    logger.debug(f"Package '{package_name}' found but no versions parsed{repo_info}")
    return []


def parse_metadata(metadata_content: str) -> dict[str, str | list[str]]:
    """
    Parse PKG-INFO/METADATA format into a dict.
    Fields that can appear multiple times (like Requires-Dist) are stored as lists.
    """
    metadata = {}
    lines = metadata_content.splitlines()

    # Find where description body starts (after empty line following Description-Content-Type)
    description_start_idx = None
    for i, line in enumerate(lines):
        if line.strip().lower().startswith("description-content-type"):
            # Look for empty line after this
            for j in range(i + 1, len(lines)):
                if not lines[j].strip():
                    description_start_idx = j + 1
                    break
            break

    # Parse header fields (before description body)
    parse_end = description_start_idx if description_start_idx else len(lines)
    current_field = None
    current_value = []

    for i, line in enumerate(lines[:parse_end]):
        if not line.strip():
            continue
        if line.startswith(" ") or line.startswith("\t"):
            # Continuation line
            if current_field:
                current_value.append(line.strip())
        else:
            # New field
            if current_field:
                field_value = " ".join(current_value) if current_value else ""
                if current_field in ["requires-dist", "classifier"]:
                    if current_field not in metadata:
                        metadata[current_field] = []
                    if field_value:
                        metadata[current_field].append(field_value)
                else:
                    metadata[current_field] = field_value

            if ":" in line:
                current_field, value = line.split(":", 1)
                current_field = current_field.strip().lower()
                current_value = [value.strip()]
            else:
                current_field = None
                current_value = []

    # Don't forget the last field before description
    if current_field:
        field_value = " ".join(current_value) if current_value else ""
        if current_field in ["requires-dist", "classifier"]:
            if current_field not in metadata:
                metadata[current_field] = []
            if field_value:
                metadata[current_field].append(field_value)
        else:
            metadata[current_field] = field_value

    # Parse description body (everything after empty line)
    if description_start_idx and description_start_idx < len(lines):
        description_lines = lines[description_start_idx:]
        description_body = "\n".join(description_lines).strip()
        if description_body:
            metadata["description"] = description_body

    return metadata


def get_package_metadata(
    repo_url: str, package_name: str, version: str | None = None
) -> dict[str, str | list[str]]:
    """
    Fetch package metadata (description, etc.) from a PEP 503 repository using PEP 658.
    Returns a dict with metadata fields like 'summary', 'author', etc.
    """
    normalized_name = canonicalize_name(package_name)
    wheel_dist_name = normalized_name.replace("-", "_")
    package_dir_url = repo_url + normalized_name + "/"

    # Get the latest version if not specified
    if not version:
        # Use pip to get versions
        pip_cmd = get_cli_pip_command()
        versions = get_package_versions(pip_cmd, package_name, repo_url)
        if not versions:
            return {}
        version = versions[0]

    # Try PEP 658 metadata file (lightweight)
    # Try common wheel filename patterns
    metadata_urls = [
        f"{package_dir_url}{wheel_dist_name}-{version}-py3-none-any.whl.metadata",
        f"{package_dir_url}{wheel_dist_name}-{version}-py3-any-none.whl.metadata",
    ]

    for metadata_url in metadata_urls:
        try:
            with urllib.request.urlopen(metadata_url, timeout=5) as response:
                metadata_content = response.read().decode("utf-8")
                return parse_metadata(metadata_content)
        except urllib.error.HTTPError:
            continue
        except Exception as e:
            logger.debug(f"Error fetching metadata from {metadata_url}: {e}")
            continue

    return {}


def probe_repos(
    repos: dict[str, str], package_name: str, *, timeout: float = 5.0
) -> list[str]:
    """
    Probe configured repositories to detect which ones advertise wheel files
    for `package_name`. Returns a list of repository labels (keys from `repos`) in
    the same order as `repos` that appear to provide the package. If none advertise
    the package, returns an empty list.

    This is a light-weight PEP 503 index inspection (fetching index.html for
    <index>/<normalized-name>/index.html and looking for .whl links).
    """
    from urllib.error import HTTPError
    from urllib.request import urlopen

    from packaging.utils import canonicalize_name

    normalized_package = canonicalize_name(package_name)
    providers: list[str] = []
    for label, url in repos.items():
        try:
            normalized_repo = normalize_pep503_repo_url(url)
            index_url = normalized_repo + normalized_package + "/index.html"
            with urlopen(index_url, timeout=timeout) as resp:
                content = resp.read().decode("utf-8")
                if ".whl" in content:
                    providers.append(label)
        except HTTPError:
            # Forbidden/404/etc - skip but keep checking other repos
            continue
        except Exception:
            continue
    return providers
