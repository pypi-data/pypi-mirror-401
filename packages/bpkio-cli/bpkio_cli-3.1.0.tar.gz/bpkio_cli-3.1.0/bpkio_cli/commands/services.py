import click
import cloup
from bpkio_api.models import (
    AdaptiveStreamingCdnService,
    AdInsertionService,
    ContentReplacementService,
    ContentReplacementSlot,
    ServiceIn,
    VirtualChannelService,
    VirtualChannelSlot,
)
from bpkio_cli.click_mods.forwarder_group import create_forwarder_group
from bpkio_cli.commands.creators.ad_insertion import create_ad_insertion_service_command
from bpkio_cli.commands.creators.services import create_service_command
from bpkio_cli.commands.creators.slot_iterators import (
    clear_slots_command,
    replicate_slots_command,
)
from bpkio_cli.commands.creators.virtual_channel import (
    create_virtual_channel_service_command,
)
from bpkio_cli.commands.creators.virtual_channel_populate import (
    populate_virtual_channel_slots_command,
)
from bpkio_cli.commands.creators.virtual_channel_slot import create_slot_command
from bpkio_cli.commands.profiles import get_profile_group
from bpkio_cli.commands.sessions import session
from bpkio_cli.commands.sources import get_source_group
from bpkio_cli.commands.template_crud import create_resource_group
from bpkio_cli.commands.template_crud_slots import create_child_resource_group
from bpkio_cli.core.api_resource_helpers import retrieve_api_resource_from_chain
from bpkio_cli.core.app_context import AppContext
from bpkio_cli.writers.breadcrumbs import display_tip

default_fields = ["id", "name", "type", "hash", "state", "format"]


def get_services_commands():
    root_endpoint = "services"
    root: cloup.Group = create_resource_group(
        "service",
        resource_type=ServiceIn,
        endpoint_path=[root_endpoint],
        aliases=["svc", "services"],
        with_content_commands=["all"],
        default_fields=default_fields,
        traversal_commands=[source_commands],
        extra_commands=[
            hash_command,
            session,
            create_service_command(),
        ],
    )

    return [
        root,
        create_resource_group(
            "content-replacement",
            resource_type=ContentReplacementService,
            endpoint_path=[root_endpoint, "content_replacement"],
            aliases=["cr"],
            default_fields=default_fields,
            with_content_commands=["all"],
            traversal_commands=[source_commands],
            extra_commands=[
                hash_command,
                session,
                clear_slots_command(),
                replicate_slots_command(),
                add_slots_commands(
                    resource_type=ContentReplacementSlot,
                    parent_path=[root_endpoint, "content_replacement"],
                    default_fields=[
                        "id",
                        "name",
                        "relativeStartTime",
                        "relativeEndTime",
                        "duration",
                        "replacement.id",
                        "replacement.name",
                    ],
                ),
            ],
        ),
        create_resource_group(
            "ad-insertion",
            resource_type=AdInsertionService,
            endpoint_path=[root_endpoint, "ad_insertion"],
            aliases=["dai", "ssai"],
            default_fields=[
                "id",
                "name",
                "type",
                "sub_type",
                "hash",
                "state",
                "format",
            ],
            with_content_commands=["all"],
            traversal_commands=[source_commands],
            extra_commands=[
                hash_command,
                session,
                create_ad_insertion_service_command(),
            ],
        ),
        create_resource_group(
            "virtual-channel",
            resource_type=VirtualChannelService,
            endpoint_path=[root_endpoint, "virtual_channel"],
            aliases=["vc"],
            default_fields=default_fields,
            with_content_commands=["all"],
            traversal_commands=[source_commands],
            extra_commands=[
                hash_command,
                session,
                clear_slots_command(),
                create_virtual_channel_service_command(),
                populate_virtual_channel_slots_command(),
                replicate_slots_command(),
                add_slots_commands(
                    resource_type=VirtualChannelSlot,
                    parent_path=[root_endpoint, "virtual_channel"],
                    default_fields=[
                        "id",
                        "name",
                        "type",
                        "relativeStartTime",
                        "relativeEndTime",
                        "duration",
                        "replacement.id",
                        "replacement.name",
                        "category.id",
                        "category.name",
                    ],
                    extra_commands=[create_slot_command()],
                ),
            ],
        ),
        create_resource_group(
            "adaptive-streaming-cdn",
            resource_type=AdaptiveStreamingCdnService,
            endpoint_path=[root_endpoint, "adaptive_streaming_cdn"],
            aliases=["cdn"],
            default_fields=default_fields,
            extra_commands=[
                hash_command,
            ],
        ),
    ]


def add_slots_commands(resource_type, parent_path, default_fields, extra_commands=[]):
    return create_child_resource_group(
        "slot",
        resource_type=resource_type,
        endpoint_path=parent_path + ["slots"],
        aliases=["slots"],
        default_fields=default_fields,
        extra_commands=extra_commands,
    )


# COMMAND: HASH
def hash_command(endpoint_path: str):
    @cloup.command(help="Show the service hash (bpkio_serviceid)")
    @click.pass_obj
    def hash(obj: AppContext, **kwargs):
        resource = retrieve_api_resource_from_chain(endpoint_path=endpoint_path)
        click.echo(resource.hash)

    return hash


def source_commands(endpoint_path: str):
    """Create traversal commands that can forward to source/ad-server groups.

    These commands extract related resources from a service and allow
    chaining to the full set of commands available on those resources.

    Example:
        bic ad-insertion 49946 ad-server url
        bic ad-insertion 49946 source read --top 10
    """

    def extract_main_source(obj: AppContext):
        """Extract the main source from a service."""
        resource = retrieve_api_resource_from_chain(endpoint_path=endpoint_path)
        resource = obj.api.services.retrieve(resource.id)

        source = None
        if hasattr(resource, "source") and resource.source:
            source = obj.api.sources.retrieve(resource.source.id)
        elif hasattr(resource, "baseLive") and resource.baseLive:
            source = obj.api.sources.retrieve(resource.baseLive.id)

        if source:
            # Record to cache so it can be referenced later (e.g., `bic source $` or `bic live $`)
            obj.cache.record(source)
            display_tip(
                f"Traversed to {source.__class__.__name__} {source.id} ({source.name})"
            )

        return source

    def extract_ad_server(obj: AppContext):
        """Extract the ad server source from a service."""
        resource = retrieve_api_resource_from_chain(endpoint_path=endpoint_path)

        keys = [
            "vodAdInsertion",
            "adBreakInsertion",
            "liveAdPreRoll",
            "liveAdReplacement",
        ]
        for k in keys:
            if hasattr(resource, k):
                o = getattr(resource, k)
                if o is not None and hasattr(o, "adServer"):
                    ad_server = obj.api.sources.retrieve(o.adServer.id)
                    # Record to cache so it can be referenced later (e.g., `bic ad-server $`)
                    obj.cache.record(ad_server)
                    display_tip(
                        f"Traversed to AdServerSource {ad_server.id} ({ad_server.name}) (from {k})"
                    )
                    return ad_server
        return None

    def extract_transcoding_profile(obj: AppContext):
        """Extract the transcoding profile from a service."""
        resource = retrieve_api_resource_from_chain(endpoint_path=endpoint_path)
        resource = obj.api.services.retrieve(resource.id)

        if hasattr(resource, "transcodingProfile") and resource.transcodingProfile:
            profile = obj.api.transcoding_profiles.retrieve(
                resource.transcodingProfile.id
            )
            # Record to cache so it can be referenced later (e.g., `bic profile $`)
            obj.cache.record(profile)
            display_tip(
                f"Traversed to TranscodingProfile {profile.id} ({profile.name})"
            )
            return profile
        return None

    # Get the target groups for forwarding
    source_group = get_source_group("source")
    ad_server_group = get_source_group("ad-server")
    profile_group = get_profile_group()

    # Create forwarder groups
    source_forwarder = create_forwarder_group(
        name="source",
        target_group=source_group,
        resource_extractor=extract_main_source,
        help="Access the main source used by the service (for command chaining). "
        "Subcommands like 'url', 'read', 'info' are forwarded to the source.",
        aliases=["src", "live"],
    )

    ad_server_forwarder = create_forwarder_group(
        name="ad-server",
        target_group=ad_server_group,
        resource_extractor=extract_ad_server,
        help="Access the ad server behind the service (for command chaining). "
        "Subcommands like 'url', 'read', 'info' are forwarded to the ad-server.",
        aliases=["ads"],
    )

    profile_forwarder = create_forwarder_group(
        name="transcoding-profile",
        target_group=profile_group,
        resource_extractor=extract_transcoding_profile,
        help="Access the transcoding profile used by the service (for command chaining). "
        "Subcommands like 'info', 'content', 'usage' are forwarded to the profile.",
        aliases=["profile", "prf"],
    )

    # COMMAND: DEPENDENCIES
    @cloup.command(
        help="Show the (primary) dependencies of the service",
        name="dependencies",
        aliases=["deps"],
    )
    @click.pass_obj
    def dependencies(obj: AppContext, **kwargs):
        """Show all primary dependencies of this service."""
        resource = retrieve_api_resource_from_chain(endpoint_path=endpoint_path)
        resource = obj.api.services.retrieve(resource.id)

        # Main source
        main_source = extract_main_source(obj)
        if main_source:
            click.secho("Main source:", fg="cyan", bold=True)
            obj.response_handler.treat_single_resource(main_source)

        # Ad server
        ad_server = extract_ad_server(obj)
        if ad_server:
            click.secho("\nAd server:", fg="cyan", bold=True)
            obj.response_handler.treat_single_resource(ad_server)

        # Transcoding profile
        profile_res = extract_transcoding_profile(obj)
        if profile_res:
            click.secho("\nTranscoding profile:", fg="cyan", bold=True)
            obj.response_handler.treat_single_resource(profile_res)

    return [source_forwarder, ad_server_forwarder, profile_forwarder, dependencies]
    return [source_forwarder, ad_server_forwarder, profile_forwarder, dependencies]
