# AI development guidelines

Applies throughout this repository to OpenAI Codex and compatible coding assistants. Build a reusable FastAPI starter using pragmatic DDD, Clean Architecture, and a modular monolith. Read README.md and the affected code before editing.

## Architecture

- Preserve bounded-context and modular monolith boundaries. Implement new business capabilities inside `src/ddd_fastapi/modules/<context>`.
- Keep domain entities, value objects, invariants, exceptions, and repository contracts independent of FastAPI, Pydantic, persistence frameworks, and infrastructure.
- Application services coordinate use cases and depend on domain contracts.
- Infrastructure implements persistence and external adapters. Presentation handles HTTP contracts, schemas, routers, and request dependency providers.
- Wire concrete adapters in the existing `create_app` composition root and lifespan. Preserve Presentation -> Application -> Domain dependencies; inject infrastructure through contracts.
- Avoid unnecessary abstractions, generic base classes/repositories, mediator frameworks, and event buses.

## Implementation

- Reuse existing configuration, JSON logging, exception handling, and dependency injection conventions.
- Do not scaffold a second FastAPI application or introduce another framework for an existing capability.
- Keep new dependencies optional unless essential; explain essential additions and review their licenses and security implications.
- Maintain async correctness: do not block the event loop with synchronous I/O; match providers and adapters to their actual I/O model.
- Make resource lifecycles explicit. Open and close clients in lifespan, keep state scoped to the app instance, and preserve isolation across test apps.
- Do not silently change in-memory storage into mandatory external infrastructure.

## Testing and verification

- Add focused unit tests for new domain logic, application service tests for changed use cases, and API integration tests for changed HTTP behavior.
- Use lifespan-aware TestClient contexts and isolated application instances.
- Activate the project virtual environment, then run:

```sh
ruff check .
ruff format --check .
pyright
pytest
```

- Run `python scripts/smoke.py` when startup, wiring, or HTTP behavior changes; verify Docker when deployment configuration changes.
- Report actual commands and results, including failures and checks not run. Preserve the existing verification baseline.

## Security

- Never commit secrets, hardcode credentials, or include private endpoints or proprietary source code.
- Do not expose internal exception details or sensitive inputs in API error responses.
- Preserve secure defaults, restrictive CORS, and production documentation settings.
- Do not weaken authentication or authorization in derived projects. The example starter itself has no authentication.
- Keep private adapters in private packages/repositories and inject them through domain contracts. Follow SECURITY.md for vulnerability reports.
- Preserve upstream copyright and third-party license notices.

## Assistant behavior

- Inspect existing code before changes. Make small, reviewable changes; do not modify unrelated modules.
- Prefer established conventions. Do not redesign the architecture without explicit approval.
- Do not deploy or publish without explicit approval. Do not commit, push, tag, create releases, change visibility, or modify Git remotes unless explicitly requested.
- Summarize changed files, verification results, and remaining risks or blockers. Never claim external settings are enabled without verification.
