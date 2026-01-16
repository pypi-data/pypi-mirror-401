"""Shortwing CLI - Click command definitions."""

import sys
from typing import Optional

import click

from shortwing import __version__
from shortwing.config import initialize_client, resolve_credentials
from shortwing.core import execute_query
from shortwing.exceptions import (
    EXIT_CONFIG_ERROR,
    EXIT_QUERY_ERROR,
    EXIT_SUCCESS,
    ConfigurationError,
    ShortwingError,
)
from shortwing.output import format_json


class ShortwingGroup(click.Group):
    """
    Custom group that handles both:
    - shortwing "query string" (no subcommand)
    - shortwing query "query string" (with subcommand)
    """

    def invoke(self, ctx):
        """Invoke the group, handling query args that look like commands."""
        # Get the args that would be treated as command/subcommand args
        # Use 'args' which is the future-proof attribute
        remaining_args = getattr(ctx, "args", []) or getattr(
            ctx, "protected_args", []
        )

        if remaining_args:
            first_arg = remaining_args[0]
            # Only treat as query if:
            # 1. It's not a known command AND
            # 2. It doesn't start with '-' (which would be an option for a subcommand)
            if first_arg not in self.commands and not first_arg.startswith("-"):
                # Not a command and not an option, treat all remaining args as query
                ctx.ensure_object(dict)
                ctx.obj["query_from_args"] = " ".join(remaining_args)
                # Set invoked_subcommand to None to invoke the group itself
                ctx.invoked_subcommand = None
                # Call the group callback directly
                return ctx.invoke(self.callback, **ctx.params)

        return super().invoke(ctx)


def read_query(
    query_arg: Optional[str], ctx: Optional[click.Context] = None
) -> Optional[str]:
    """
    Read query from stdin (if piped), context, or from argument.

    Stdin takes precedence over argument.
    """
    # Check if stdin has data (is piped)
    if not sys.stdin.isatty():
        stdin_data = sys.stdin.read().strip()
        if stdin_data:
            return stdin_data

    # Check for query from context (set by ShortwingGroup.invoke)
    if ctx and ctx.obj and ctx.obj.get("query_from_args"):
        return ctx.obj["query_from_args"].strip()

    # Fall back to positional argument
    if query_arg:
        return query_arg.strip()

    return None


def run_query(
    query_arg: Optional[str],
    key: Optional[str],
    endpoint: Optional[str],
    instance: str,
    compact: bool,
    pretty: bool,
    ctx: Optional[click.Context] = None,
) -> None:
    """Core query execution logic shared by commands."""
    try:
        # Resolve credentials
        api_key, api_endpoint = resolve_credentials(key, endpoint, instance)

        # Read query
        query = read_query(query_arg, ctx)
        if not query:
            raise click.UsageError(
                "No query provided. Pipe via stdin or pass as argument."
            )

        # Initialize dimcli
        initialize_client(api_key, api_endpoint)

        # Execute query
        result = execute_query(query)

        # Check for API error in response
        if "error" in result:
            # Output the error JSON and exit with code 1
            output = format_json(result, compact=compact)
            click.echo(output)
            sys.exit(EXIT_QUERY_ERROR)

        # Format and output
        # --pretty is default, --compact overrides
        use_compact = compact and not pretty
        output = format_json(result, compact=use_compact)
        click.echo(output)
        sys.exit(EXIT_SUCCESS)

    except ConfigurationError as e:
        click.echo(str(e), err=True)
        sys.exit(EXIT_CONFIG_ERROR)
    except ShortwingError as e:
        click.echo(str(e), err=True)
        sys.exit(e.exit_code)
    except click.UsageError:
        raise  # Let click handle usage errors
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        sys.exit(EXIT_QUERY_ERROR)


# Shared options decorator
def common_options(func):
    """Decorator to add common options to commands."""
    func = click.option(
        "--key",
        help="API key (overrides DIMENSIONS_KEY env var and dsl.ini)",
    )(func)
    func = click.option(
        "--endpoint",
        help="API endpoint (overrides DIMENSIONS_ENDPOINT env var and dsl.ini)",
    )(func)
    func = click.option(
        "--instance",
        default="live",
        help="Instance name from dsl.ini (default: live)",
    )(func)
    func = click.option(
        "--compact",
        is_flag=True,
        default=False,
        help="Output compact JSON (no indentation)",
    )(func)
    func = click.option(
        "--pretty",
        is_flag=True,
        default=False,
        help="Force pretty-printed JSON (default)",
    )(func)
    return func


@click.group(cls=ShortwingGroup, invoke_without_command=True)
@click.version_option(version=__version__, prog_name="shortwing")
@common_options
@click.pass_context
def main(ctx, key, endpoint, instance, compact, pretty):
    """
    Shortwing - Lightweight CLI for Dimensions DSL queries.

    Execute DSL queries via stdin or as an argument:

    \b
    shortwing "search grants for \\"malaria\\" return researchers"
    echo 'search grants for "malaria"' | shortwing
    shortwing query "search grants"

    \b
    Credentials are loaded from (in order of priority):
    1. CLI flags (--key, --endpoint)
    2. Environment variables (DIMENSIONS_KEY, DIMENSIONS_ENDPOINT)
    3. ~/.dimensions/dsl.ini file
    """
    ctx.ensure_object(dict)
    if ctx.invoked_subcommand is None:
        run_query(None, key, endpoint, instance, compact, pretty, ctx)


@main.command("query")
@click.argument("query", required=False)
@common_options
def query_cmd(query, key, endpoint, instance, compact, pretty):
    """
    Execute a DSL query.

    Query can be provided as argument or piped via stdin.
    Stdin takes precedence if both are provided.
    """
    run_query(query, key, endpoint, instance, compact, pretty)


if __name__ == "__main__":
    main()
