# DDD FastAPI Starter

A Python 3.12+ feature-first modular monolith with explicit dependency injection and no required external services.

## Quick start: Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
uvicorn ddd_fastapi.main:create_app --factory --reload
```

## Quick start: Linux/macOS

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev]'
cp .env.example .env
uvicorn ddd_fastapi.main:create_app --factory --reload
```

Open http://127.0.0.1:8000/docs in development. Create an item with `POST /api/v1/items` and JSON `{"name":"Example","description":"Optional"}`. List with GET on the same path; GET, PUT (full replacement), and DELETE use `/api/v1/items/{uuid}`. Creation returns 201 and Location; deletion returns 204. Lists use offset and limit (maximum 100), ordered by insertion.

## Architecture and a new bounded context

`src/ddd_fastapi/modules/items` is the working example:

- `domain`: frozen entities, value objects, invariants, exceptions, repository Protocol. Only the Python standard library belongs here.
- `application`: use cases depending on domain contracts.
- `infrastructure`: concrete adapters implementing those contracts.
- `presentation`: Pydantic schemas, FastAPI routing, dependency providers.

Copy this structure into a new business module. Start with business invariants and a narrow repository Protocol, implement use cases, add an adapter, then register its router in `create_app`. Modules should communicate through explicit application contracts rather than importing another module's infrastructure. Avoid generic base repositories and shared business models.

## Dependency injection and lifecycle

`create_app` is the composition root. Lifespan creates one repository per running app and releases it on shutdown. Request providers construct inexpensive services using that repository; no process-global business state or cached settings are used. Always enter `TestClient` as a context manager to run lifespan. Override presentation providers with `app.dependency_overrides` for alternative adapters. Immutable items and a lock protect in-memory operations across worker threads.

The example repository is volatile and process-local: restarts erase data, and multiple workers/replicas have separate stores. Run one worker for this demo. Add durable storage before using it for real data.

## Configuration and operations

Copy `.env.example`; environment variables override `.env`. `APP_ENVIRONMENT` accepts development, test, production. OpenAPI and docs are enabled only in development. `APP_LOG_LEVEL` validates supported levels. `APP_CORS_ORIGINS` is a JSON array of explicit origins, empty by default; wildcard origins are rejected. CORS does not provide authentication.

`GET /health/live` reports process liveness. `/health/ready` checks only the async callables supplied as `readiness_checks` to the factory; with no dependencies it is ready. Adapters should provide bounded timeout probes, open/close their clients in lifespan, and avoid exposing dependency details.

Application logs are JSON with UTC timestamps and request IDs. Supply a UUID in `X-Request-ID` to correlate requests, or the server generates one. All API errors have `code`, `message`, and `request_id`; validation responses omit input values and internal errors omit exception details. Uvicorn access logs are disabled in the container to avoid logging query strings. Configure platform log retention and redact sensitive adapter logs.

## Verification

```sh
ruff check .
ruff format --check .
pyright
pytest
python scripts/smoke.py
uvicorn ddd_fastapi.main:create_app --factory --host 127.0.0.1 --port 8000
```

CI checks Python 3.12, 3.13, and 3.14 and builds the container on 3.12. Starlette requires a patched 1.x release; development installs HTTPX2 for its test client. HTTPX remains available for application clients and the smoke test. Dependency ranges are intentional for a reusable template; generate and maintain a reviewed lockfile for a deployed application.

## Docker and Coolify

```sh
docker build -t ddd-fastapi .
docker run --rm -p 8000:8000 ddd-fastapi
# Or:
docker compose up --build -d
```

The multi-stage image installs wheels and runs as UID 10001. Its healthcheck uses `/health/live`. `compose.yaml` supplies a read-only filesystem, dropped capabilities, and a temporary filesystem.

In Coolify, create an application from your own Git repository using the Dockerfile build pack (or import `compose.yaml`). Set internal port 8000, configure the domain/TLS, set `APP_ENVIRONMENT=production`, and configure explicit frontend CORS origins if needed. Set the platform health path to `/health/ready`. For Compose, adjust published ports to your platform routing convention. No credentials are required. Review proxy trust, request limits, authentication/authorization, and durable adapters for your deployment before exposing business data publicly.

## GitHub Template usage

The owner must enable **Template repository** in GitHub repository settings after completing the release checklist. Choose **Use this template -> Create a new repository**, select your own account and repository name, then create and clone it. This creates an independent repository with its own history, issues, security settings, and releases. Configure its visibility and private vulnerability reporting yourself; see [SECURITY.md](SECURITY.md).

To adapt your repository:

1. Update `[project].name`, description, and version in `pyproject.toml`, and the FastAPI title in `src/ddd_fastapi/main.py`.
2. If renaming the Python package, rename `src/ddd_fastapi`, update the Hatch wheel package path in `pyproject.toml`, and update imports and Uvicorn factory paths in Dockerfile, scripts, tests, and documentation. Search with `rg 'ddd-fastapi|ddd_fastapi|DDD FastAPI Starter'`. Reinstall with `python -m pip install -e ".[dev]"` and run the checks.
3. Keep or replace the Items example. To remove it, remove its router import/registration and repository import/lifespan wiring from `main.py`, then remove the Items-specific imports/handlers in `core/errors.py` and `modules/items`. Replace the corresponding domain, service, API tests and Items assertions in `scripts/smoke.py`; retain health, configuration, and generic error tests. Add your own bounded context using the structure above.
4. Retain upstream copyright and third-party notices; add notices for your own contributions where appropriate.

## Working with Codex

Open this repository in OpenAI Codex and give it a scoped task with acceptance criteria. The root [AGENTS.md](AGENTS.md) supplies architecture, security, implementation, and verification rules. Ask Codex to inspect the affected module, follow those rules, and report actual checks. Compatible assistants should read the same file. Review diffs before committing; deployment and publication require explicit approval. See the [official AGENTS.md guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

## Private enterprise adapters

Keep private integrations in your own private repository or separately installed package. Implement the module's domain Protocol there and inject it through the composition root/provider. Supply credentials through the deployment secret manager; add adapter configuration validation and readiness probes. Do not copy private code, endpoints, or credentials into this public template.

See [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), and [PUBLIC_RELEASE_CHECKLIST.md](PUBLIC_RELEASE_CHECKLIST.md). Released under the [MIT License](LICENSE), copyright (c) 2026 DK. Dependency licenses and notices remain applicable, including MPL-2.0 source availability for redistributed certifi.
