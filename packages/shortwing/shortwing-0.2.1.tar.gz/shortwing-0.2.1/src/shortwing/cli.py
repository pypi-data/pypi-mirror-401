"""Shortwing CLI - Click command definitions."""

import asyncio
import sys
from typing import Optional

import click

from shortwing import __version__
from shortwing.config import resolve_credentials
from shortwing.core import close_client, execute_query
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


def show_next_steps(exit_code: int, compact: bool) -> None:
    """
    Display contextual next steps to stderr after query execution.

    Only shows suggestions in interactive mode (not when piping output).

    Args:
        exit_code: The exit code (0=success, 1=query error, 2=config error)
        compact: Whether compact output mode was used
    """
    # Don't show suggestions if output is being piped
    if not sys.stdout.isatty():
        return

    suggestions = []

    if exit_code == EXIT_SUCCESS:
        suggestions.append("\nNext steps:")
        if not compact:
            suggestions.append("  • Try --compact for single-line JSON")
        suggestions.append("  • Pipe to jq: shortwing '...' | jq '.field'")
        suggestions.append("  • Save results: shortwing '...' > output.json")
        suggestions.append("  • Run shortwing --help for more options")

    elif exit_code == EXIT_QUERY_ERROR:
        suggestions.append("\nQuery failed. Try:")
        suggestions.append("  • Check DSL syntax at dimensions.ai/dsl")
        suggestions.append("  • Verify query structure")
        suggestions.append("  • Run shortwing --help for examples")

    elif exit_code == EXIT_CONFIG_ERROR:
        suggestions.append("\nConfiguration error. Try:")
        suggestions.append("  • Set API key: export DIMENSIONS_KEY=your-key")
        suggestions.append("  • Or use --key flag: shortwing --key KEY 'query'")
        suggestions.append("  • Check ~/.dimensions/dsl.ini configuration")

    if suggestions:
        click.echo("\n".join(suggestions), err=True)


async def run_query_async(
    query_arg: Optional[str],
    key: Optional[str],
    endpoint: Optional[str],
    instance: str,
    compact: bool,
    pretty: bool,
    ctx: Optional[click.Context] = None,
) -> None:
    """Async core query execution logic shared by commands."""
    try:
        # Resolve credentials
        api_key, api_endpoint = resolve_credentials(key, endpoint, instance)

        # Read query
        query = read_query(query_arg, ctx)
        if not query:
            # Show help instead of error
            if ctx:
                click.echo(ctx.get_help())
                ctx.exit(0)
            else:
                raise click.UsageError(
                    "No query provided. Pipe via stdin or pass as argument."
                )

        # Execute query (async HTTP call)
        result = await execute_query(query, api_key, api_endpoint)

        # Check for API error in response
        if "error" in result:
            # Output the error JSON and exit with code 1
            output = format_json(result, compact=compact)
            click.echo(output)
            show_next_steps(EXIT_QUERY_ERROR, compact)
            sys.exit(EXIT_QUERY_ERROR)

        # Format and output
        # --pretty is default, --compact overrides
        use_compact = compact and not pretty
        output = format_json(result, compact=use_compact)
        click.echo(output)
        show_next_steps(EXIT_SUCCESS, use_compact)
        sys.exit(EXIT_SUCCESS)

    except ConfigurationError as e:
        click.echo(str(e), err=True)
        show_next_steps(EXIT_CONFIG_ERROR, False)
        sys.exit(EXIT_CONFIG_ERROR)
    except ShortwingError as e:
        click.echo(str(e), err=True)
        show_next_steps(EXIT_QUERY_ERROR, False)
        sys.exit(e.exit_code)
    except click.UsageError:
        raise  # Let click handle usage errors
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        show_next_steps(EXIT_QUERY_ERROR, False)
        sys.exit(EXIT_QUERY_ERROR)
    finally:
        # Clean up HTTP client
        await close_client()


def run_query(*args, **kwargs):
    """Sync wrapper for run_query_async."""
    asyncio.run(run_query_async(*args, **kwargs))


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
        # Check if a query will be available
        has_query_from_args = ctx.obj.get("query_from_args")

        # If no query from args, show help instead of error
        if not has_query_from_args and sys.stdin.isatty():
            click.echo(ctx.get_help())
            ctx.exit(0)

        # Run query - it will handle errors appropriately
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
    # If no query arg and no stdin, show help
    if not query and sys.stdin.isatty():
        ctx = click.get_current_context()
        click.echo(ctx.get_help())
        ctx.exit(0)

    # Run query - it will handle errors appropriately
    run_query(query, key, endpoint, instance, compact, pretty)


if __name__ == "__main__":
    main()
