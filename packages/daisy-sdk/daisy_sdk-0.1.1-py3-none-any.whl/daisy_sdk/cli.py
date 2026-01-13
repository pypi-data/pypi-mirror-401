from __future__ import annotations

from pathlib import Path

import typer

from daisy_sdk.auth import get_valid_access_token
from daisy_sdk.image import fetch_and_run, find_existing_image, run_existing
from daisy_sdk.utils import DEFAULT_TOKEN_PATH, write_toml

app = typer.Typer(add_completion=False, invoke_without_command=True)


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """Daisy CLI entrypoint."""
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())


@app.command()
def run(
    update: bool = typer.Option(
        False,
        "--update",
        help="Fetch the latest image even if one already exists locally.",
    )
) -> None:
    """Fetch (if needed) and run the Daisy image."""
    if not update:
        print("Checking for existing Daisy image...")
        existing = find_existing_image()
        if existing:
            run_existing(existing)
            typer.echo(f"Started image: {existing}")
            return

    access_token = get_valid_access_token()
    image = fetch_and_run(access_token)
    typer.echo(f"Started image: {image}")


@app.command()
def setup() -> None:
    """Set up the Daisy config directory and config file. Start here for first-time users."""
    created_paths: list[Path] = []

    config_path = DEFAULT_TOKEN_PATH
    if not config_path.parent.exists():
        config_path.parent.mkdir(parents=True, exist_ok=True)
        created_paths.append(config_path.parent)

    if not config_path.exists():
        write_toml(config_path, {})
        created_paths.append(config_path)

    if created_paths:
        typer.echo("\nDaisy setup complete.\n")
        typer.echo(f"Config file: {config_path}")
        typer.echo(
            "\nNext steps:\n"
            "- Complete the Daisy signup flow to get the keys for config.toml.\n"
            "- If you are not enrolled in the beta, email support@daisyhq.com.\n"
        )
    else:
        typer.echo("Daisy setup already complete.")
