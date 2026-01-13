# daisy-sdk

CLI for authenticating with Daisy and running the Daisy image.

## Setup

```bash
mise install
uv sync --dev
```

If `uv` is not installed, you can install it with mise or pipx:

```bash
# with mise
mise use -g uv@0.2

# or with pipx
pipx install uv
```

## Usage

```bash
daisy run
```

Tokens must be stored in `~/.daisy/config.toml`:

```toml
access_token = "..."
refresh_token = "..."
```

On each run, the CLI validates the access token with Supabase; if it is invalid or expired, it refreshes and writes the new tokens back to the same file.
