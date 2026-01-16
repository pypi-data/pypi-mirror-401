import bpkio_api.models as models
import click
import cloup

import bpkio_cli.click_options as bic_options
from bpkio_cli.commands.creators.sources import create
from bpkio_cli.commands.misc.compatibility_check import check_compatibility
from bpkio_cli.commands.template_crud import create_resource_group
from bpkio_cli.core.app_context import AppContext
from bpkio_cli.utils.progress import list_with_progress

# Registry to store source groups for forwarding from services
_source_groups_registry = {}


def get_source_group(name: str) -> cloup.Group:
    """Get a source group by name for command forwarding.

    Args:
        name: The name of the source group (e.g., 'ad-server', 'source', 'live')

    Returns:
        The cloup.Group for the specified source type
    """
    if not _source_groups_registry:
        # Lazily populate the registry
        get_sources_commands()
    return _source_groups_registry.get(name)


def get_sources_commands():
    """Generate all source-related command groups.

    Returns a list of Click command groups for managing different source types
    (assets, live, catalogs, ad servers, slates, origins).
    """
    global _source_groups_registry

    root_endpoint = "sources"

    # Create the main source group (used both for CLI and for forwarding)
    source_group: cloup.Group = create_resource_group(
        "source",
        resource_type=models.SourceIn,
        endpoint_path=[root_endpoint],
        aliases=["src", "sources"],
        with_content_commands=["all"],
        traversal_commands=[usage],
        default_fields=["id", "name", "type", "format", "url"],
        extra_commands=[create, check_compatibility],
    )

    ad_server_group = create_resource_group(
        "ad-server",
        resource_type=models.AdServerSource,
        endpoint_path=[root_endpoint, "ad_server"],
        aliases=["ads"],
        with_content_commands=["info", "url", "check", "table", "read"],
        default_fields=["id", "name", "url"],
        traversal_commands=[usage],
    )

    # Populate the registry for forwarding from services
    # Only source types actually used in service traversal commands need to be registered
    _source_groups_registry["ad-server"] = ad_server_group
    _source_groups_registry["source"] = source_group

    return [
        source_group,
        create_resource_group(
            "asset",
            resource_type=models.AssetSource,
            endpoint_path=[root_endpoint, "asset"],
            aliases=["assets"],
            default_fields=["id", "name", "format", "url"],
            with_content_commands=[
                "info",
                "url",
                "check",
                "table",
                "read",
                "play",
                "profile",
                "download",
            ],
            traversal_commands=[usage],
            extra_commands=[check_compatibility],
        ),
        create_resource_group(
            "live",
            resource_type=models.LiveSource,
            endpoint_path=[root_endpoint, "live"],
            default_fields=["id", "name", "format", "url"],
            with_content_commands=["all"],
            traversal_commands=[usage],
            extra_commands=[check_compatibility],
        ),
        create_resource_group(
            "asset-catalog",
            resource_type=models.AssetCatalogSource,
            endpoint_path=[root_endpoint, "asset_catalog"],
            aliases=["catalog", "catalogs"],
            default_fields=["id", "name", "url"],
            with_content_commands=[
                "info",
                "url",
                "check",
                "table",
                "read",
                "play",
                "profile",
                "download",
            ],
            traversal_commands=[usage],
            extra_commands=[check_compatibility],
        ),
        ad_server_group,
        create_resource_group(
            "slate",
            resource_type=models.SlateSource,
            endpoint_path=[root_endpoint, "slate"],
            aliases=["slates"],
            default_fields=["id", "name", "format", "url"],
            with_content_commands=["url", "check", "play"],
            traversal_commands=[usage],
        ),
        create_resource_group(
            "origin",
            resource_type=models.OriginSource,
            endpoint_path=[root_endpoint, "origin"],
            aliases=["origins"],
            default_fields=["id", "name", "url"],
        ),
    ]


# COMMAND: USAGE
@cloup.command(help="Find all Services that use the source")
@bic_options.list(default_fields=["id", "name", "type"])
@bic_options.output_formats
@click.pass_obj
def usage(
    obj: AppContext,
    list_format,
    select_fields,
    sort_fields,
    id_only,
    return_first,
    **kwargs
):
    """Find all services that use this source.

    Scans all services to find which ones reference the current source.
    """
    select_fields = list(select_fields)
    id = obj.current_resource.id
    source = obj.api.sources.retrieve(id)

    services = list_with_progress(
        obj.api.services, hydrate=True, label="Scanning services..."
    )

    selected_services = []
    for service in services:
        # svc = obj.api.services.retrieve(service.id)
        svc = service

        if hasattr(svc, "source") and getattr(svc.source, "id") == id:
            selected_services.append(svc)
            select_fields.append("source")

        if hasattr(svc, "replacement") and getattr(svc.replacement, "id") == id:
            selected_services.append(svc)
            select_fields.append("replacement")

        if isinstance(source, models.LiveSource):
            if isinstance(svc, models.VirtualChannelService):
                if svc.baseLive.id == id:
                    selected_services.append(svc)
                    select_fields.append("baseLive")

        if isinstance(source, models.AdServerSource):
            if isinstance(svc, models.AdInsertionService):
                if svc.vodAdInsertion and svc.vodAdInsertion.adServer.id == id:
                    selected_services.append(svc)
                    select_fields.append("vodAdInsertion.adServer.id")
                if svc.liveAdPreRoll and svc.liveAdPreRoll.adServer.id == id:
                    selected_services.append(svc)
                    select_fields.append("liveAdPreRoll.adServer.id")
                if svc.liveAdReplacement and svc.liveAdReplacement.adServer.id == id:
                    selected_services.append(svc)
                    select_fields.append("liveAdReplacement.adServer.id")

            if isinstance(svc, models.VirtualChannelService):
                if svc.adBreakInsertion and svc.adBreakInsertion.adServer.id == id:
                    selected_services.append(svc)
                    select_fields.append("adBreakInsertion.adServer.id")

        if isinstance(source, models.SlateSource):
            if isinstance(svc, models.AdInsertionService):
                if (
                    svc.liveAdReplacement
                    and svc.liveAdReplacement.gapFiller
                    and svc.liveAdReplacement.gapFiller.id == id
                ):
                    selected_services.append(svc)
                    select_fields.append("liveAdReplacement.gapFiller.id")

            if isinstance(svc, models.VirtualChannelService):
                if (
                    svc.adBreakInsertion
                    and svc.adBreakInsertion.gapFiller
                    and svc.adBreakInsertion.gapFiller.id == id
                ):
                    selected_services.append(svc)
                    select_fields.append("adBreakInsertion.gapFiller.id")

    if len(selected_services):
        obj.response_handler.treat_list_resources(
            selected_services,
            select_fields=select_fields,
            sort_fields=sort_fields,
            format=list_format,
            id_only=id_only,
            return_first=return_first,
        )
    else:
        click.secho("No services found that use this source")
