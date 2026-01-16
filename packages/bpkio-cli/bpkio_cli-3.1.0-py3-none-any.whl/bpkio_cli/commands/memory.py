import click
import cloup

from bpkio_cli.core.app_context import AppContext


@cloup.group(aliases=["mem"], help="App resource registry comands")
@click.pass_obj
def memory(obj: AppContext):
    pass


@memory.command(help="Clear the app resource register")
@click.pass_obj
def clear(obj: AppContext):
    obj.cache.clear()


@memory.command(help="Check what is stored in the app's resource register")
@click.pass_obj
def read(obj: AppContext):
    click.secho("Last resources accessed", fg="yellow")
    for v in obj.cache.list_resources():
        click.secho(" · " + v.__class__.__name__ + " ", fg="green", nl=False)
        click.secho(v.summary if hasattr(v, "summary") else v)

    click.secho("Last lists retrieved", fg="yellow")
    for k, lst in obj.cache.list_lists().items():
        try:
            list_ids = [item.id for item in lst]
            click.secho(" · " + k + " ", fg="green", nl=False)
            click.secho(list_ids)
        except Exception:
            pass

    click.secho("Last Metadata", fg="yellow")
    for k, metadata in obj.cache.list_metadata().items():
        try:
            click.secho(" · " + k + " ", fg="green", nl=False)
            click.secho(metadata)
        except Exception:
            pass

    click.secho("Named Variables", fg="yellow")
    variables = obj.cache.list_variables()
    if variables:
        for name, entry in sorted(variables.items()):
            click.secho(f" · @{name} ", fg="green", nl=False)
            click.echo(entry["value"])
    else:
        click.echo(" (none)")


@memory.command(help="Clear the cache for a single resource")
@cloup.argument("id", help="The id of the resource", type=int)
@click.pass_obj
def forget(obj: AppContext, id: int):
    obj.cache.remove_by_id(id)


# === Named Variables ===


@memory.group(
    name="var",
    aliases=["variable", "variables"],
    help="Manage named variables for reuse across CLI invocations.",
)
def var_group():
    pass


@var_group.command(name="set", help="Set a named variable.")
@click.argument("name")
@click.argument("value")
@click.option(
    "--type", "-t",
    type=click.Choice(["id", "url", "path", "string"]),
    default="string",
    help="Type hint for the variable.",
)
@click.pass_obj
def var_set(obj: AppContext, name: str, value: str, type: str):
    """Set a named variable.

    Examples:
        bic memory var set my-source 12345
        bic memory var set archive /path/to/archive.tar.gz --type path
        bic memory var set prod-url https://example.com/stream --type url
    """
    metadata = {"type": type}
    obj.cache.set_variable(name, value, metadata)
    click.secho(f"✓ Variable '@{name}' set to '{value}'", fg="green")


@var_group.command(name="get", help="Get a named variable's value.")
@click.argument("name")
@click.pass_obj
def var_get(obj: AppContext, name: str):
    """Get a named variable's value."""
    value = obj.cache.get_variable(name)
    if value is None:
        raise click.ClickException(f"Variable '@{name}' not found.")
    click.echo(value)


@var_group.command(name="list", aliases=["ls"], help="List all named variables.")
@click.pass_obj
def var_list(obj: AppContext):
    """List all named variables for the current tenant."""
    variables = obj.cache.list_variables()

    if not variables:
        click.secho("No named variables defined.", fg="yellow")
        click.echo("Use 'bic memory var set <name> <value>' to create one.")
        return

    for name, entry in sorted(variables.items()):
        value = entry["value"]
        click.echo(f"  @{name} = {value}")


@var_group.command(name="delete", aliases=["rm", "del"], help="Delete a named variable.")
@click.argument("name")
@click.pass_obj
def var_delete(obj: AppContext, name: str):
    """Delete a named variable."""
    if obj.cache.delete_variable(name):
        click.secho(f"✓ Variable '@{name}' deleted.", fg="green")
    else:
        raise click.ClickException(f"Variable '@{name}' not found.")


@var_group.command(name="clear", help="Clear all named variables.")
@click.confirmation_option(prompt="Are you sure you want to clear all variables?")
@click.pass_obj
def var_clear(obj: AppContext):
    """Clear all named variables for the current tenant."""
    obj.cache.clear_variables()
    click.secho("✓ All variables cleared.", fg="green")
