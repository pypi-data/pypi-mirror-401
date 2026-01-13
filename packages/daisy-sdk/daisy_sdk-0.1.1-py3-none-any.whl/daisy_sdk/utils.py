from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

import tomli_w

DEFAULT_TOKEN_PATH = Path.home() / ".daisy" / "config.toml"
DEFAULT_PROJECT_CONFIG_PATH = Path.home() / ".daisy" / "projects.toml"


def ensure_parent_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def read_toml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("rb") as handle:
        import tomllib

        return tomllib.load(handle)


def write_toml(path: Path, data: dict[str, Any]) -> None:
    ensure_parent_dir(path)
    with path.open("wb") as handle:
        tomli_w.dump(data, handle)


def run_command(args: list[str], *, capture_output: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        check=True,
        text=True,
        capture_output=capture_output,
    )
