from __future__ import annotations

import typer

from . import __version__
from .trash import trash_paths

app = typer.Typer(
    add_completion=False,
    subcommand_metavar="",
    rich_markup_mode="rich",
    help=(
        "Move files and folders to the macOS Trash instead of deleting them.\n\n"
        "Examples:\n"
        "  trash file.txt\n"
        "  trash -r folder/\n"
        "  trash -rf build/ dist/\n"
    ),
)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(__version__)
        raise typer.Exit(code=0)


@app.callback(invoke_without_command=True)
def trash_command(
    ctx: typer.Context,
    paths: list[str] = typer.Argument(None, help="Files and folders to move to Trash."),
    version: bool = typer.Option(
        False,
        "--version",
        callback=_version_callback,
        is_eager=True,
        help="Show the version and exit.",
    ),
    recursive: bool = typer.Option(
        False,
        "-r",
        "-R",
        "--recursive",
        help="Allow removing directories and their contents.",
    ),
    force: bool = typer.Option(
        False,
        "-f",
        "--force",
        help="Ignore nonexistent files and never prompt.",
    ),
    interactive: bool = typer.Option(
        False,
        "-i",
        "--interactive",
        help="Prompt before every removal.",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Show what would be moved, without changing anything.",
    ),
    verbose: bool = typer.Option(
        False,
        "-v",
        "--verbose",
        help="Print each moved path.",
    ),
) -> None:
    _ = version
    if not paths:
        typer.echo(ctx.get_help())
        raise typer.Exit(code=0)

    trash_paths(
        paths,
        recursive=recursive,
        force=force,
        interactive=interactive,
        dry_run=dry_run,
        verbose=verbose,
    )


def main() -> None:
    app()
