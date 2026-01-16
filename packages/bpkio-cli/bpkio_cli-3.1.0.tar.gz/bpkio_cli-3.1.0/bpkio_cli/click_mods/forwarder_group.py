"""Forwarder Group - A Click group that forwards commands to another resource group.

This module provides a mechanism to create traversal commands that can forward
subcommands to the target resource's command group. For example:
    `bic ad-insertion 49946 ad-server url`
forwards the `url` command to the `ad-server` resource group.
"""

from typing import Any, Callable, List, Optional

import click
import cloup
from bpkio_cli.core.app_context import AppContext
from bpkio_cli.core.resource_chain import ResourceChain


class ForwarderGroup(cloup.Group):
    """A Click group that extracts a related resource and forwards commands to its group.

    This allows commands like:
        `bic ad-insertion 49946 ad-server url`
    to work by:
    1. Extracting the ad-server resource from the ad-insertion service
    2. Setting up the context with the ad-server resource
    3. Forwarding the `url` command to the ad-server resource group
    """

    def __init__(
        self,
        *args: Any,
        target_group: cloup.Group,
        resource_extractor: Callable[[AppContext], Any],
        default_callback: Optional[Callable] = None,
        takes_id_arg: bool = True,
        is_default: bool = False,
        **kwargs: Any,
    ):
        """Initialize the ForwarderGroup.

        Args:
            target_group: The resource group to forward commands to (e.g., ad-server group)
            resource_extractor: A callable that extracts the target resource from the context.
                               Should return the resource or None if not found.
            default_callback: Optional callback to run when no subcommand is provided.
                             If None, defaults to showing the extracted resource.
            takes_id_arg: Whether this command takes an ID argument (for ResourceSubCommand)
            is_default: Whether this is a default command (for ResourceSubCommand)
        """
        # Set ResourceSubCommand-like attributes
        self.takes_id_arg = takes_id_arg
        self.is_default = is_default

        super().__init__(*args, **kwargs)

        self.target_group = target_group
        self.resource_extractor = resource_extractor
        self.default_callback = default_callback
        self._plugins_copied = False

        # Copy commands from target group that make sense to forward
        self._copy_forwardable_commands()

    def _copy_forwardable_commands(self):
        """Copy commands from the target group, preserving section organization."""
        # Check if the target group has sections (cloup feature)
        if (
            hasattr(self.target_group, "_user_sections")
            and self.target_group._user_sections
        ):
            # Copy sections with forwarding wrappers for each command
            for section in self.target_group._user_sections:
                new_section_commands = []
                for cmd_name, cmd in section.commands.items():
                    if cmd is not None and getattr(cmd, "takes_id_arg", True):
                        forwarding_cmd = _create_forwarding_command(
                            cmd, self.resource_extractor
                        )
                        new_section_commands.append(forwarding_cmd)

                if new_section_commands:
                    new_section = cloup.Section(section.title, new_section_commands)
                    self.add_section(new_section)
        else:
            # Fallback: flat command list without sections
            for cmd_name in self.target_group.commands.keys():
                cmd = self.target_group.commands.get(cmd_name)
                if cmd is not None and getattr(cmd, "takes_id_arg", True):
                    forwarding_cmd = _create_forwarding_command(
                        cmd, self.resource_extractor
                    )
                    self.add_command(forwarding_cmd, name=cmd_name)

    def _copy_plugin_commands(self, ctx: click.Context):
        """Copy plugin commands from the target group after they've been discovered."""
        if self._plugins_copied:
            return

        # Trigger plugin discovery on the target group
        # We need to create a fake context that makes the target group's name
        # appear as the command name, so plugins with scopes matching the target
        # group (e.g., scope="profile") are discovered correctly.
        if hasattr(self.target_group, "discover_plugins"):
            # Create a mock context that looks like it's coming from the target group
            class MockContext:
                def __init__(self, target_group, real_ctx):
                    self.command = target_group
                    self.parent = (
                        None  # No parent - treat as top-level for scope matching
                    )
                    self.params = real_ctx.params if real_ctx else {}

            mock_ctx = MockContext(self.target_group, ctx)
            self.target_group.discover_plugins(mock_ctx)

        # Copy plugin sections if they exist and have commands
        for section_attr in ["plugin_section", "admin_plugin_section"]:
            if hasattr(self.target_group, section_attr):
                source_section = getattr(self.target_group, section_attr)
                if source_section.commands:
                    new_section_commands = []
                    for cmd_name, cmd in source_section.commands.items():
                        if cmd is not None and getattr(cmd, "takes_id_arg", True):
                            forwarding_cmd = _create_forwarding_command(
                                cmd, self.resource_extractor
                            )
                            new_section_commands.append(forwarding_cmd)

                    if new_section_commands:
                        new_section = cloup.Section(
                            source_section.title, new_section_commands
                        )
                        self.add_section(new_section)

        self._plugins_copied = True

    def invoke(self, ctx: click.Context):
        """Handle invocation - the default behavior runs through the callback."""
        # The callback will handle the "no subcommand" case
        # Just delegate to parent which will:
        # 1. Run our callback (which shows the resource if no subcommand)
        # 2. Then run the subcommand if there is one
        return super().invoke(ctx)

    def get_command(self, ctx: click.Context, name: str):
        """Get a command by name, discovering plugins if needed."""
        # First check if command exists in core commands
        cmd = super().get_command(ctx, name)
        if cmd is not None:
            return cmd

        # If not found, try discovering plugins from target group
        self._copy_plugin_commands(ctx)
        return super().get_command(ctx, name)

    def list_sections(self, ctx: click.Context):
        """List sections, including plugin sections after discovery."""
        # Discover and copy plugins before listing sections (for --help)
        self._copy_plugin_commands(ctx)
        return super().list_sections(ctx)

    def list_commands(self, ctx: click.Context) -> List[str]:
        """List available commands."""
        self._copy_plugin_commands(ctx)
        return list(self.commands.keys())


def _create_forwarding_command(
    target_cmd: click.Command,
    resource_extractor: Callable[[AppContext], Any],
) -> click.Command:
    """Create a wrapper command that forwards to the target command.

    The wrapper:
    1. Extracts the target resource using resource_extractor
    2. Sets up the context (resource chain, current_resource)
    3. Invokes the target command
    """

    @click.pass_context
    def forwarding_callback(ctx, **kwargs):
        obj: AppContext = ctx.obj

        # Extract the target resource
        resource = resource_extractor(obj)
        if resource is None:
            click.secho("No resource found to forward to", fg="red")
            return

        # Reset the resource chain to only contain the extracted resource
        # This is important because the forwarded command expects to operate
        # on this resource as if it was accessed directly (not nested under a service)
        chain: ResourceChain = obj.resource_chain
        chain._chain.clear()
        chain.add_resource(key=resource.id, resource=resource)

        # Invoke the target command with the forwarded context
        ctx.invoke(target_cmd, **kwargs)

    # Create the new command with the same parameters as the target
    new_cmd = click.Command(
        name=target_cmd.name,
        callback=forwarding_callback,
        params=list(target_cmd.params),  # Copy the parameters
        help=target_cmd.help,
        epilog=getattr(target_cmd, "epilog", None),
        short_help=getattr(target_cmd, "short_help", None),
        options_metavar=getattr(target_cmd, "options_metavar", "[OPTIONS]"),
        add_help_option=True,
    )

    # Copy ResourceSubCommand attributes if present
    new_cmd.takes_id_arg = getattr(target_cmd, "takes_id_arg", True)
    new_cmd.is_default = getattr(target_cmd, "is_default", False)

    return new_cmd


def create_forwarder_group(
    name: str,
    target_group: cloup.Group,
    resource_extractor: Callable[[AppContext], Any],
    help: str = None,
    aliases: List[str] = None,
    default_callback: Optional[Callable] = None,
) -> ForwarderGroup:
    """Factory function to create a ForwarderGroup.

    Args:
        name: The name of the command
        target_group: The resource group to forward commands to
        resource_extractor: Callable that extracts the target resource from context
        help: Help text for the command
        aliases: Command aliases
        default_callback: Optional callback for when no subcommand is given

    Returns:
        A ForwarderGroup instance
    """

    @click.pass_context
    def group_callback(ctx):
        """Handle the group callback - show resource if no subcommand."""
        # invoked_subcommand is set by click DURING super().invoke()
        # At this point in the callback, it's already set correctly
        if ctx.invoked_subcommand is None:
            if default_callback:
                return ctx.invoke(default_callback)
            else:
                # Default: extract and display the resource
                obj: AppContext = ctx.obj
                resource = resource_extractor(obj)
                if resource:
                    # Update resource chain so current_resource works
                    obj.resource_chain.add_resource(key=resource.id, resource=resource)
                    obj.response_handler.treat_single_resource(resource)
                else:
                    click.secho("No resource found", fg="yellow")

    group = ForwarderGroup(
        name=name,
        callback=group_callback,
        target_group=target_group,
        resource_extractor=resource_extractor,
        default_callback=default_callback,
        help=help,
        invoke_without_command=True,
    )

    if aliases:
        group.aliases = aliases

    return group
