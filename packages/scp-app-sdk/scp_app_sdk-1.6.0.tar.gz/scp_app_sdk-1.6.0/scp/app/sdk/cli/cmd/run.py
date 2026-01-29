import asyncio
import click
import json
import os

from scp.app.sdk.cli.documentation import doc_run
from scp.app.sdk.cli.scp_config import SCPConfig
from scp.app.sdk.cli.server import scp_app_store_server
from scp.app.sdk.runner import run_install, run_uninstall, run_migrate, RunScriptException


def general_bootstrap(directory, user_id, iss, app_configuration, uninstall=False):
    # default app_config to avoid unpakcing issue
    app_config = None

    # IF no provided directory → default to ./ 
    if not directory:
        directory = os.getcwd()
    # If not provided as arg → prompt interactively
    if not user_id:
        user_id = click.prompt('👉 User ID', type=str)

    if not iss:
        iss = 'unknown' # avoid issue going to the exception if local usage

    if not app_configuration:
        app_configuration = click.prompt('👉 App configuration file path', type=click.Path(exists=True))

    # Load JSON from file if not valid path, trigger message if not uninstall
    try:
        with open(app_configuration, "r") as f:
            app_config = json.load(f)
    except Exception as e:
        raise click.ClickException(f"❌ Failed to load app configuration JSON: {e}")

    # Add SAM server from config
    config = SCPConfig()
    sam_server = config.get('sam_server')
    if not sam_server or sam_server == '' or not sam_server.startswith("http"):
        click.echo('⚠️ SAM server invalid or incorrect, starting configuration module.')
        config.prompt_for_config(prompt_scp=False)
        sam_server = config.get('sam_server')

    token = config.get('token')
    if not token:
        click.echo("⚠️ No token is configured.")
        config.prompt_and_set('token', 'token', is_url=False)
        token = config.get('token')
    while True:
        if scp_app_store_server(sam_server, token):
            break
        config.prompt_for_config(prompt_scp=False)
        sam_server = config.get('sam_server')
        token = config.get('token')

    env = {
        "USER_ID": user_id,
        "ISS": iss,
        "SAM_URL": sam_server,
    }

    return directory, app_config, env


def run_and_display(coro):
    try:
        out = asyncio.run(coro)
    except RunScriptException as e:
        raise click.ClickException(f"⚠️ {e}")

    click.echo("🗒️ Script output 🗒️")
    click.echo(out)


# click related
@click.group()
def run():
    """
    Execute and run apt script
    """
    pass


@run.command()
@click.argument("dir", required=False, type=click.Path())
@click.option("--user-id", type=str, help="User ID, also known as uepId")
@click.option("--iss", type=str, help="Iss")
@click.option("--app-configuration", type=click.Path(exists=True), help="Path to JSON app configuration file")
def install(dir, user_id, iss, app_configuration):
    """
    Run install script.

    \b
    Arguments:
      DIR   If no path is provided, the current directory is used.
    """
    directory, app_config, env = general_bootstrap(dir, user_id, iss, app_configuration, uninstall=False)
    run_and_display(run_install(directory=directory, input=app_config, env=env))


@run.command()
@click.argument("dir", required=False, type=click.Path())
@click.option("--user-id", type=str, help="User ID, also known as uepId")
@click.option("--iss", type=str, help="Iss")
@click.option("--app-configuration", type=click.Path(exists=True), help="Path to JSON app configuration file")
def migrate(dir, user_id, iss, app_configuration):
    """
    Run migrate script.

    \b
    Arguments:
      DIR   If no path is provided, the current directory is used.
    """
    directory, app_config, env = general_bootstrap(dir, user_id, iss, app_configuration, uninstall=False)
    run_and_display(run_migrate(directory=directory, input=app_config, env=env))


@run.command()
@click.argument("dir", required=False, type=click.Path())
@click.option("--iss", type=str, help="Iss")
@click.option("--user-id", type=str, help="User ID, also known as uepId")
@click.option("--app-configuration", type=click.Path(exists=True), help="Path to JSON app configuration file")
def uninstall(dir, user_id, iss, app_configuration):
    """
    Run uninstall script.

    \b
    Arguments:
      DIR   If no path is provided, the current directory is used.
    """
    directory, app_config, env = general_bootstrap(dir, user_id, iss, app_configuration, uninstall=True)
    run_and_display(run_uninstall(directory=directory, input=app_config, env=env))


@run.command()
def help():
    """Show detailed documentation"""
    doc_run()
