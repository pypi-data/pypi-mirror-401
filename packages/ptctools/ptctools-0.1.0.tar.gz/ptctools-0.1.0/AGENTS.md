# AGENTS.md - ptctools

## Overview

Portainer Client Tools CLI package for managing Portainer stacks, volumes, and databases from the command line.

## Project Structure

```text
src/ptctools/
├── pyproject.toml          # Package config, entry point: ptctools.cli:main
├── README.md               # User documentation
└── src/ptctools/
    ├── __init__.py         # Version: 0.1.0
    ├── cli.py              # Main click CLI, registers subcommand groups
    ├── _portainer.py       # Shared Portainer API utilities (internal)
    ├── _s3.py              # Shared S3/URI parsing utilities (internal)
    ├── stack.py            # stack deploy command
    ├── volume.py           # volume backup/restore commands
    ├── db.py               # db backup/restore commands
    └── utils.py            # utils backup/restore commands (local Duplicati)
```

## CLI Architecture

Uses [click](https://click.palletsprojects.com/) with nested command groups:

```
ptctools
├── stack deploy      # Deploy/update Portainer stack
├── volume backup     # Backup volumes to S3 via Duplicati (--volumes: comma-separated)
├── volume restore    # Restore single volume from S3 (--volume or from URI path)
├── db backup         # Backup PostgreSQL via container exec
├── db restore        # Restore PostgreSQL from backup
├── utils backup      # Local backup to S3 or directory using Duplicati
└── utils restore     # Local restore from S3 or directory using Duplicati
```

## Environment Variables

All commands require `PORTAINER_ACCESS_TOKEN`. Backup commands also use:
- `S3_ACCESS_KEY`, `S3_SECRET_KEY` - S3 credentials
- `DUPLICATI_PASSPHRASE` - Optional encryption

## Development

```bash
# Install in development mode
uv tool install . --force

# Test CLI
ptctools --help
```

## Adding New Commands

1. Create module in `src/ptctools/` with a `cli` click group
2. Register in `cli.py` via `main.add_command(module.cli, name="name")`
3. Use `_portainer.py` for Portainer API calls
