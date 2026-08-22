# Docker

Container definitions live in the [`docker/`](../../docker) directory.

## Images

- [`Dockerfile`](../../docker/Dockerfile) — production image. Multi-stage build
  using the official `uv` base image, installs into a virtualenv, runs as a
  non-root user, includes a `HEALTHCHECK`, and ships only runtime dependencies.
- [`Dockerfile.dev`](../../docker/Dockerfile.dev) — development image with the
  full dev toolchain and hot reload.

### Multi-architecture builds

The production image builds for `linux/amd64` and `linux/arm64` (including Apple
Silicon) via Buildx in the [Docker workflow](../../.github/workflows/docker.yml).
For projects needing prebuilt wheels across many Python versions, the
[Multi-Py](https://github.com/multi-py) images are a drop-in base.

## Development environment

```bash
make docker-up     # web + worker + beat + postgres + redis, with hot reload
make docker-down
```

The dev override [`docker-compose.dev.yml`](../../docker/docker-compose.dev.yml)
mounts `src/` as a volume so edits reload instantly, enables debug settings, and
uses `Dockerfile.dev`. The base
[`docker-compose.yml`](../../docker/docker-compose.yml) defines the services and
healthchecked `db`/`redis` dependencies.

## Registry publishing

On pushes to `main` and version tags, the Docker workflow builds and pushes
multi-arch images to:

- **GitHub Container Registry** (`ghcr.io/<owner>/<repo>`) — always
- **Docker Hub** — when the `DOCKERHUB_USERNAME` variable and `DOCKERHUB_TOKEN`
  secret are configured

Tags are derived automatically from branch names, semantic version tags
(`{{version}}`, `{{major}}.{{minor}}`) and commit SHAs via
`docker/metadata-action`.
