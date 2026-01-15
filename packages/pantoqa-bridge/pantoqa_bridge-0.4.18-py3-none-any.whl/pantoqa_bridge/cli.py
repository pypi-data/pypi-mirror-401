import click

from pantoqa_bridge.config import PKG_NAME, SERVER_HOST, SERVER_PORT
from pantoqa_bridge.server import precheck_required_tools, start_bridge_server
from pantoqa_bridge.tasks.executor import AppiumExecutable, MaestroExecutable, QAExecutable
from pantoqa_bridge.utils.misc import make_sync
from pantoqa_bridge.utils.pkg import get_pkg_version


@click.group(help="PantoAI QA Extension CLI", invoke_without_command=True)
@click.option("--version", is_flag=True, help="Show version and exit")
@click.option(
  "--skip-pre-check",
  is_flag=True,
  default=False,
  help="Skip pre-check of required tools",
)
@click.pass_context
def cli(ctx: click.Context, version: bool, skip_pre_check: bool) -> None:
  if version:
    click.echo(f"PantoQA Bridge version: {get_pkg_version(PKG_NAME)}")
    ctx.exit(0)

  if not skip_pre_check:
    precheck_required_tools()

  if ctx.invoked_subcommand is None:
    ctx.invoke(serve)


@cli.command()
@click.option("--host", default=SERVER_HOST, show_default=True, help="Bind address")
@click.option("--port", default=SERVER_PORT, show_default=True, type=int, help="Port to listen on")
def serve(host: str, port: int) -> None:
  start_bridge_server(host, port)


@cli.command()
@click.option("--framework",
              type=click.Choice(["appium", "maestro"], case_sensitive=False),
              required=True,
              help="QA framework to use")
@click.argument("files", nargs=-1, required=True, type=click.Path(exists=True))
@click.option("--maestro-bin", help="Path to Maestro binary (for maestro framework)")
@click.option("--appium-url", help="Appium server URL (for appium framework)")
@click.option("--device", help="Device serial number to run tests on")
@make_sync
async def execute(
  framework: str,
  files: list[str],
  maestro_bin: str | None = None,
  appium_url: str | None = None,
  device: str | None = None,
) -> None:

  executable: QAExecutable | None = None
  if framework.lower() == "maestro":
    executable = MaestroExecutable(files=files, maestro_bin=maestro_bin, device_serial=device)
  elif framework.lower() == "appium":
    executable = AppiumExecutable(files=files, appium_url=appium_url, device_serial=device)
  else:
    raise click.ClickException(f"Unsupported framework: {framework}")

  await executable.execute()
  click.echo("Execution completed.")


if __name__ == "__main__":
  cli()
