# What is this file even doing?
# When apps were first created, we were in a conundrum about where the
# core source code of the apps should live when we would expose functionality through both the metaflow
# and outerbounds packages. Because of this, we made the trade-off to let the apps live in the
# extensions and we would expose them through the outerbounds package.
# Once we decided on this, we had another issue. If we try to import anything from
# metaflow, we will end up running `init_config` (from ob-metaflow-extensions) which will try to resolve the configuration
# remotely. This essentially breaks the CLI (since metaflow will crash at the time of import).
#
# To circumvent this issue, we had previously tried to catch the exception raised by `init_config` and
# added a placeholder CLI (dummy-cli so users would come ask us, lol).
#
# Now we instead implement the whole CLI within `outerbounds.apps.cli` (moved from `mf_extensions.outerbounds.plugins.apps.core.app_cli`).
# The way we implement the CLI is by lazy loading the commands when required. This helps in 3 ways:
#   1. Doesn't break the whole CLI if apps cannot be loaded.
#   2. The Apps CLI will fail early if the wrong parameters are set. It will fail with better error messaging (bubbling errors from module imports).
#   3. Helps decouple the code and have fewer tricky code paths.

from typing import Tuple, Union
from outerbounds._vendor import click
from ..utils import metaflowconfig
import os
import uuid
import importlib

# We need this environment variable to ensure that we use the correctly vendor'd click.
# The app_core contains a configuration module that helps centralize the configuration
# parsing and validation of apps in one place (CLI/Config File/Programmatic API). This
# configuration framework needs the correct selection of click (from either outerbounds/metaflow)
# so that the CLI has the correct configurations set in it.
os.environ["APPS_CLI_LOADING_IN_OUTERBOUNDS"] = "true"
OUTERBOUNDS_APP_CLI_AVAILABLE = True


class AppException(Exception):
    """Exception raised when app configuration is invalid."""

    pass


class TempEnvVarReplace:
    """
    Context manager to temporarily replace specified environment variables.
    Accepts a variable number of names (str), storing their original values and restoring them on exit.
    """

    def __init__(self, **vars_to_replace: str):
        self._vars = vars_to_replace
        self._originals = {}  # type: ignore[var-annotated]

    def __enter__(self):
        for key, value in self._vars.items():
            self._originals[key] = os.environ.get(key)
            if value is not None:
                os.environ[key] = str(value)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for key, value in self._originals.items():
            if value is None:
                if key in os.environ:
                    del os.environ[key]
            else:
                os.environ[key] = value
        return False


class AppLazyGroup(click.Group):
    lazy_commands = {}  # type: ignore[var-annotated]  # name -> "module:attr"

    def list_commands(self, ctx):
        return sorted(set(super().list_commands(ctx)) | set(self.lazy_commands))

    def get_command(self, ctx, name):
        # ctx : https://click.palletsprojects.com/en/stable/api/#click.Context
        cmd = super().get_command(ctx, name)
        if cmd is not None:
            return cmd

        target = self.lazy_commands.get(name)
        if not target:
            return None

        mod_name, attr = target.split(":")
        try:
            # We need to set the right values at module import so that
            # any sub-command to apps can work when basic parameters
            # like `--profile` are passed to `outerbounds app`
            with TempEnvVarReplace(
                METAFLOW_HOME=ctx.params.get("config_dir"),
                METAFLOW_PROFILE=ctx.params.get("profile"),
            ):
                mod = importlib.import_module(mod_name)
        except Exception as e:
            if e.__class__.__name__ == "OuterboundsConfigException":
                error_and_exit(e.message)
            raise e

        obj = getattr(mod, attr)

        # If it's already a Click command, return it directly
        if isinstance(obj, click.core.Command):
            return obj

        # If it's a callable factory, call it to produce the command
        if callable(obj):
            cmd = obj()
            if not isinstance(cmd, click.core.Command):
                raise click.ClickException(
                    f"{target} did not return a click.Command (got {type(cmd)!r})"
                )
            return cmd

        raise click.ClickException(
            f"{target} must be a click.Command or a callable returning one (got {type(obj)!r})"
        )


def error_and_exit(msg):
    click.secho(msg, fg="red", bold=True, err=True)
    raise SystemExit(1)


def resolve_perimeter_and_api_server(config_dir: str, profile: str, perimeter=None):
    metaflow_config = metaflowconfig.init_config(config_dir, profile)
    api_server = metaflowconfig.get_sanitized_url_from_config(
        config_dir, profile, "OBP_API_SERVER"
    )
    if perimeter is None:
        perimeter = metaflow_config.get("OBP_PERIMETER")

    return perimeter, api_server  # type: ignore


@click.group()
def cli():
    pass


class CliState(object):
    pass


@cli.group(
    help="Commands related to Deploying/Running/Managing Apps on Outerbounds Platform.",
    cls=AppLazyGroup,
)
@click.option(
    "--perimeter",
    default=None,
    help="Perimeter ID. Defaults to the currently active perimeter.",
)
@click.option(
    "-d",
    "--config-dir",
    default=os.path.expanduser(os.environ.get("METAFLOW_HOME", "~/.metaflowconfig")),
    help="Path to Metaflow configuration directory",
    show_default=True,
)
@click.option(
    "-p",
    "--profile",
    default=os.environ.get("METAFLOW_PROFILE", None),
    help="The named metaflow profile",
)
@click.pass_context
def app(
    ctx,
    perimeter=None,
    config_dir=None,
    profile=None,
):
    """App-related commands."""
    metaflow_set_context = getattr(ctx, "obj", None)
    ctx.obj = CliState()
    ctx.obj.trace_id = str(uuid.uuid4())
    ctx.obj.app_state_dir = os.path.join(os.curdir, ".ob_apps")

    # resolve the perimeter and the API URL
    perimeter, api_server = resolve_perimeter_and_api_server(
        config_dir, profile, perimeter
    )
    if perimeter is None or api_server is None:
        raise AppException(
            "Exception resolving perimeter / outerbounds token. "
            "Please fetch a new configuration string from the outerbounds UI and "
            "re-run the `outerbounds configure` command. "
        )
    ctx.obj.perimeter = perimeter
    ctx.obj.api_url = api_server
    os.makedirs(ctx.obj.app_state_dir, exist_ok=True)


app.lazy_commands = {  # type: ignore[attr-defined]
    "deploy": "outerbounds.apps.cli:deploy",
    "list": "outerbounds.apps.cli:list",
    "delete": "outerbounds.apps.cli:delete",
    "info": "outerbounds.apps.cli:info",
    "logs": "outerbounds.apps.cli:logs",
}
