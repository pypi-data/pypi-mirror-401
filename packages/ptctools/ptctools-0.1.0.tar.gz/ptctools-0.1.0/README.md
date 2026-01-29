# ptctools - Portainer Client Tools

CLI for managing Portainer stacks, volume backups, and database operations.

> **Note:** Only tested on Portainer 2.33.6

## Installation

```bash
# From Git repository
uv tool install git+https://github.com/tamntlib/ptctools.git
# or
uv tool install ptctools --from git+https://github.com/tamntlib/ptctools.git

# From local path
uv tool install . --no-cache --reinstall
```

## Usage

```bash
export PORTAINER_URL=https://portainer.example.com
export PORTAINER_ACCESS_TOKEN=your-api-key
export S3_ACCESS_KEY=your-s3-key
export S3_SECRET_KEY=your-s3-secret
export S3_ENDPOINT=https://s3.<region>.amazonaws.com

# Stack deployment
ptctools stack deploy -u $PORTAINER_URL -n mystack -f compose.yaml

# Volume backup/restore (uses Duplicati)
ptctools volume backup -u $PORTAINER_URL -v vol1,vol2 -o s3://mybucket
ptctools volume restore -u $PORTAINER_URL -i s3://mybucket/vol1  # volume name derived from URI path
ptctools volume restore -u $PORTAINER_URL -v vol1 -i s3://mybucket/vol1  # explicit volume name

# Database backup/restore (uses minio/mc for S3)
ptctools db backup -u $PORTAINER_URL -c container_id -v db_data \
  --db-user postgres --db-name mydb -o backup.sql.gz
ptctools db backup -u $PORTAINER_URL -c container_id -v db_data \
  --db-user postgres --db-name mydb -o s3://mybucket/backups/db.sql.gz

ptctools db restore -u $PORTAINER_URL -c container_id -v db_data \
  --db-user postgres --db-name mydb -i backup.sql.gz
ptctools db restore -u $PORTAINER_URL -c container_id -v db_data \
  --db-user postgres --db-name mydb -i s3://mybucket/backups/db.sql.gz

# Config management
# Create config from inline data
ptctools config set -u $PORTAINER_URL -n my-config -d "config content"
ptctools config set -u $PORTAINER_URL -n nginx.conf -f ./nginx.conf
ptctools config set -u $PORTAINER_URL -n my-config -d "new content" --force
ptctools config list -u $PORTAINER_URL
ptctools config get -u $PORTAINER_URL -n my-config
ptctools config delete -u $PORTAINER_URL -n my-config

# Utils - local Duplicati operations
ptctools utils backup --input ./data --output s3://backups/mydata
ptctools utils restore --input s3://backups/mydata --output ./restored

```

## Environment Variables

- `PORTAINER_ACCESS_TOKEN` - Portainer API key (required)
- `S3_ACCESS_KEY` / `S3_SECRET_KEY` - S3 credentials (for backup commands)
- `S3_ENDPOINT` - S3/MinIO endpoint URL
- `DUPLICATI_PASSPHRASE` - Backup encryption passphrase (optional, for volume backups)

## Commands

### `ptctools stack deploy`
Deploy or update a Docker stack in Portainer.

### `ptctools volume backup/restore`

- **backup**: Backup multiple Docker volumes (comma-separated) to S3 using Duplicati container.
- **restore**: Restore a single Docker volume from S3. Volume name can be specified via `--volume` or derived from the input URI path.

### `ptctools db backup/restore`
Backup/restore PostgreSQL database. Supports both local files and S3 URIs.
- Uses `pg_dump`/`psql` for database operations
- Uses `minio/mc` container for S3 transfers

### `ptctools utils backup/restore`
Local backup/restore operations using Duplicati CLI (docker or local).

### `ptctools config set/get/list/delete`
Manage Docker Swarm configs via Portainer API.
