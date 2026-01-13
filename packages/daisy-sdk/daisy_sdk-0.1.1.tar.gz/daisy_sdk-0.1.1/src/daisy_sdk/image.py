from __future__ import annotations

import shlex
import subprocess
import tempfile
import tomllib
import time
from pathlib import Path
from typing import Any

import requests

from daisy_sdk.utils import DEFAULT_PROJECT_CONFIG_PATH, run_command


def _get_presigned_url(access_token: str) -> str:
    get_download_url = "https://daisydatahq--daisy-cloud-get-image-link.modal.run"
    url = f"{get_download_url}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers, timeout=30)
    if not response.ok:
        raise RuntimeError(
            f"Image link request failed: {response.status_code} {response.text.strip()}"
        )
    payload: dict[str, Any] = response.json()
    presigned = payload.get("url") or payload.get("presigned_url")
    if not presigned:
        raise RuntimeError("Image link response missing url")
    return presigned


def _download_image(presigned_url: str, dest: Path) -> None:
    with requests.get(presigned_url, stream=True, timeout=60) as response:
        response.raise_for_status()
        total = response.headers.get("Content-Length")
        total_bytes = int(total) if total and total.isdigit() else 0
        downloaded = 0
        last_report = time.monotonic()
        with dest.open("wb") as handle:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    handle.write(chunk)
                    if total_bytes:
                        downloaded += len(chunk)
                        now = time.monotonic()
                        if now - last_report >= 0.5:
                            percent = int(downloaded / total_bytes * 100)
                            bar_len = 30
                            filled = int(bar_len * percent / 100)
                            bar = "#" * filled + "-" * (bar_len - filled)
                            print(f"Download progress: [{bar}] {percent}%", end="\r", flush=True)
                            last_report = now
                    else:
                        downloaded += len(chunk)
                        now = time.monotonic()
                        if now - last_report >= 1.0:
                            mb = downloaded / (1024 * 1024)
                            print(f"Downloaded {mb:.1f} MB", end="\r", flush=True)
                            last_report = now
        if total_bytes:
            print(" " * 60, end="\r", flush=True)
            print(f"Downloading [{'#' * 30}] 100%")
        else:
            print()


def _docker_load(tar_path: Path) -> str:
    result = run_command(["docker", "load", "-i", str(tar_path)], capture_output=True)
    output = (result.stdout or "") + (result.stderr or "")
    for line in output.splitlines():
        if "Loaded image:" in line:
            return line.split("Loaded image:", 1)[1].strip()
    raise RuntimeError("Failed to parse docker load output for image name")


def collect_project_config_paths(cfg: dict[str, Any]) -> list[str]:
    paths: list[str] = []
    project_config_paths = cfg.get("project_config_paths")
    if isinstance(project_config_paths, list):
        for path in project_config_paths:
            if isinstance(path, str):
                paths.append(path)

    projects = cfg.get("projects")
    if isinstance(projects, list):
        for entry in projects:
            if isinstance(entry, str):
                paths.append(entry)
            elif isinstance(entry, dict):
                path = entry.get("path")
                if isinstance(path, str):
                    paths.append(path)

    for _, section in cfg.items():
        if isinstance(section, dict):
            path = section.get("project_path")
            if isinstance(path, str):
                paths.append(path)

    seen: set[str] = set()
    unique_paths: list[str] = []
    for path in paths:
        if path not in seen:
            unique_paths.append(path)
            seen.add(path)
    return unique_paths


def build_command(
    tag: str,
    port: str,
    project_config_path: Path,
    run: bool,
    platform: str | None,
) -> list[str]:
    home = Path.home()
    daisy_dir = home / ".daisy"
    volumes = [
        ("-v", f"{daisy_dir}:/root/.daisy"),
    ]

    with project_config_path.open("rb") as handle:
        cfg = tomllib.load(handle)

    for path in collect_project_config_paths(cfg):
        volumes.append(("-v", f"{path}:{path}"))

    flat_vols = [arg for pair in volumes for arg in pair]
    platform_args: list[str] = []
    if platform:
        platform_args = ["--platform", platform]
    cmd = ["docker", "run", "--rm", *platform_args, "-p", f"{port}:80", *flat_vols, tag]

    print("Docker run command:")
    print(" ".join(shlex.quote(part) for part in cmd))

    if run:
        subprocess.run(cmd, check=True)

    return cmd


def _docker_run(
    image: str,
    *,
    port: str = "8080",
    project_config_path: Path = DEFAULT_PROJECT_CONFIG_PATH,
    run: bool = True,
    platform: str | None = "linux/amd64",
) -> list[str]:
    return build_command(image, port, project_config_path, run, platform)


def find_existing_image() -> str | None:
    result = run_command(
        ["docker", "images", "--format", "{{.Repository}}:{{.Tag}}"],
        capture_output=True,
    )
    lines = [line.strip() for line in (result.stdout or "").splitlines()]
    candidates = [
        line for line in lines if line and not line.startswith("<none>") and "daisy" in line
    ]
    if "daisy:latest" in candidates:
        return "daisy:latest"
    return candidates[0] if candidates else None


def run_existing(image: str) -> None:
    print(f"Using existing image: {image}")
    print("Starting container at http://localhost:8080 ...")
    _docker_run(image)


def fetch_and_run(access_token: str) -> str:
    print("Fetching image link...")
    presigned_url = _get_presigned_url(access_token)
    print("Image link received.")
    with tempfile.NamedTemporaryFile(suffix=".tar", delete=True) as handle:
        tar_path = Path(handle.name)
        print("Downloading image...")
        _download_image(presigned_url, tar_path)
        print("Image download complete.")
        print("Loading image into Docker...")
        image = _docker_load(tar_path)
        print(f"Image loaded: {image}")

    print("Starting container at http://localhost:8080 ...")
    _docker_run(image)
    return image
