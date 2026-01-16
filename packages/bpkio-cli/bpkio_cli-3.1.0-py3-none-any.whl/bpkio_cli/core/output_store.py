import json
import os
from datetime import datetime, timezone
from pathlib import Path

import click
import requests
from bpkio_api.models.common import BaseResource
from bpkio_cli.utils.strings import strip_ansi
from bpkio_cli.writers.breadcrumbs import display_error
from pydantic import HttpUrl


class OutputStore:
    """
    Lazy output store that materializes its output bundle folder only when something
    is actually written.

    Instances can act as "pointers" to sub-folders within the same output bundle.
    Use `subfolder(...)` to create nested pointers; all pointers share the same
    root bundle directory (bic-outputs-*), and the same resource.json (created once).
    """

    def __init__(
        self,
        output_directory: str | None = None,
        bundle: bool = True,
        *,
        bundle_prefix: str = "bic-outputs",
    ):
        self._base_dir = output_directory or os.getcwd()
        datetime_str = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        self._bundle_name = f"{bundle_prefix}-{datetime_str}" if bundle else None

        # Pointer state
        self._rel_parts: tuple[str, ...] = ()
        self._root: "OutputStore" = self
        self._root_materialized = False

        # Per-pointer request index (keeps request_1.. in each pointer folder)
        self._request_index = 0

    def path(self, *, ensure: bool = False) -> Path:
        """Return the current pointer folder path; optionally ensure it exists."""
        if ensure:
            self._ensure_folder()
        return Path(self.folder)

    def subfolder(self, *sub_folders: str) -> "OutputStore":
        """Create a new OutputStore pointer to a sub-folder under the same root."""
        sub_folders = tuple(s for s in sub_folders if s)
        child = OutputStore.__new__(OutputStore)
        child._base_dir = self._root._base_dir
        child._bundle_name = self._root._bundle_name
        child._root = self._root
        child._rel_parts = self._rel_parts + sub_folders
        child._root_materialized = False  # unused for children, but keep attribute
        child._request_index = 0
        return child

    @property
    def root_folder(self) -> str:
        """Top-level output bundle folder (bic-support-*), regardless of pointer depth."""
        return (
            os.path.join(self._base_dir, self._bundle_name)
            if self._bundle_name
            else self._base_dir
        )

    @property
    def folder(self) -> str:
        """Current pointer folder (root_folder + relative parts)."""
        return os.path.join(self.root_folder, *self._rel_parts)

    def _ensure_folder(self) -> None:
        """Materialize the root bundle folder + resource.json once, then pointer folder."""
        root = self._root
        if not root._root_materialized:
            os.makedirs(root.root_folder, exist_ok=True)
            root._save_resource_info()
            root._root_materialized = True
        os.makedirs(self.folder, exist_ok=True)

    def _extract_resource_metadata(self):
        """Extract metadata from the current resource for storage in resource.json"""
        metadata = {
            "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        }

        try:
            ctx = click.get_current_context()
            if res := ctx.obj.current_resource:
                if isinstance(res, BaseResource):
                    metadata["resource_type"] = res.__class__.__name__
                    metadata["resource_id"] = res.id
                    # Include name if available
                    if hasattr(res, "name"):
                        metadata["resource_name"] = res.name
                elif isinstance(res, HttpUrl):
                    metadata["url"] = str(res)
        except Exception:
            # If we can't get the resource, just leave metadata with timestamp
            pass

        return metadata

    def _save_resource_info(self):
        """Save resource.json file with resource information in the root folder."""
        metadata = self._extract_resource_metadata()
        resource_json_path = os.path.join(self.root_folder, "resource.json")
        with open(resource_json_path, "w") as f:
            f.write(json.dumps(metadata, indent=2))

    def save_text(self, filename: str, content: str):
        self._ensure_folder()
        with open(os.path.join(self.folder, filename), "w") as f:
            f.write(content)

    def append_text(self, filename: str, content: str, new_line: bool = True):
        self._ensure_folder()
        file_path = os.path.join(self.folder, filename)
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                pass
        with open(file_path, "a") as f:
            f.write(strip_ansi(content) + "\n" if new_line else content)

    def save_request_response(
        self,
        response: requests.Response,
        facets: dict = {},
        content_override: str = None,
        digest: str = None,
    ):
        basename = f"request_{self._request_index + 1}"
        self._request_index += 1
        self._last_request_basename = basename

        # Use content_override if provided (e.g., for annotated content)
        content_to_save = (
            content_override if content_override is not None else response.text
        )

        try:
            from trace_shrink.entries import RequestsResponseTraceEntry
            from trace_shrink.writers import MultiFileWriter

            # Create a TraceEntry from the Response
            entry = RequestsResponseTraceEntry(
                response=response,
                index=self._request_index,
                entry_id=str(self._request_index),
            )

            # Add annotations using standard TraceEntry methods
            if digest:
                entry.add_annotation("digest", digest)

            # Add facets as response headers
            for facet_key, facet_value in facets.items():
                entry.add_response_header(facet_key, str(facet_value))

            # Prepare bytes for body
            try:
                body_bytes = (
                    content_to_save.encode("utf-8")
                    if content_to_save is not None
                    else response.content
                )
            except Exception:
                body_bytes = None

            # Write the entry using MultiFileWriter
            writer = MultiFileWriter(self.path(ensure=True))
            writer.add_entry(entry, self._request_index, body_bytes=body_bytes)
        except Exception as e:
            display_error(f"Failed to save request and response: {e}")
