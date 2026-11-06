# Public release checklist

- [x] Owner approves MIT terms and the 2026 copyright year for individual ownership.
- [x] Owner confirms copyright (c) 2026 DK; validate standard MIT LICENSE and remove LICENSE.draft.
- [x] Review tracked and untracked release files and history for secrets, private endpoints, and proprietary code.
- [x] Confirm ddd-fastapi v0.1.0, public GitHub Template distribution, and GitHub Private Vulnerability Reporting policy.
- [ ] Owner enables and verifies GitHub Private Vulnerability Reporting using SECURITY.md.
- [x] Run installation, Ruff lint/format, Pyright, Pytest, startup/API smoke checks, and Docker build.
- [ ] Confirm GitHub Actions passes on supported Python versions.
- [x] Review dependency versions and choose a lockfile policy for deployments.
- [x] Review README deployment limits and adapter/authentication requirements.
- [ ] Enable GitHub Template setting when ready; publish only with owner approval.

## Verification recorded on 2026-11-06

- Ruff lint and format checks passed; strict Pyright passed.
- All 28 tests passed on Python 3.12.16, 3.13.18, and 3.14.7. Python 3.12/3.13 were verified in ephemeral Linux containers; 3.14 was verified on Windows.
- Real HTTP Uvicorn health and Items CRUD smoke checks passed on Python 3.12/3.13. The final Docker image built and passed its healthcheck and CRUD checks as UID 10001 with a read-only filesystem and dropped capabilities.
- Public-file scan and manual review found no credentials, private endpoints, or company-specific content. At Task 002 verification there were no commits or tracked files; all 40 release files were untracked. Generated environments/caches are excluded from the release scan.
- Fixed vulnerable Starlette constraints and bundled container pip. Installed development dependencies and the final image's exact Python package inventory passed pip-audit with no known vulnerabilities. This does not constitute an operating-system package vulnerability audit.
- Reviewed third-party license metadata and bundled license files: MIT, BSD, Apache-2.0, PSF-2.0, and MPL-2.0; no apparent incompatibility with the proposed MIT license. Preserve dependency notices and MPL source availability when redistributing dependencies. The template keeps dependency ranges; deployed applications should maintain a reviewed lockfile.
- CI configuration was validated locally; a hosted GitHub Actions run remains pending. Pyright's downloaded Node runtime needed libatomic1 in the slim verification containers; that package was installed only in those temporary test environments.
- At Task 002 completion, release remained blocked on license/copyright and maintainer/security decisions and completion of the hosted CI gate. Nothing was committed, pushed, tagged, or published.

## Task 003 release preparation

MIT terms, personal ownership, copyright year 2026, and private reporting through GitHub are owner-confirmed. The owner explicitly supplied `Copyright (c) 2026 DK` (Dodo Kresno). LICENSE contains standard MIT text with that exact notice. LICENSE.draft was removed only after validating the completed LICENSE. Package metadata declares MIT and includes LICENSE; the Docker builder copies it for wheel packaging.

AGENTS.md establishes reusable Codex conventions. README.md and CONTRIBUTING.md explain independent template repositories, metadata/package renaming, removing/replacing Items, new bounded contexts, and private adapters. Backend code and dependency constraints are unchanged from Task 002. The Docker build copies LICENSE so wheel metadata preserves the project license.

No unresolved local copyright blocker remains. External release gates: owner enables and verifies private vulnerability reporting and the Template repository setting, then confirms hosted CI passes. No GitHub settings have been changed or verified by this preparation.

### Task 003 verification results

- PASS: Ruff lint, Ruff format check, strict Pyright, and all 28 Pytest tests on Python 3.14.7.
- PASS: reviewed all 41 tracked/untracked public-file candidates; no secrets, private endpoints, or proprietary code found. Environment/cache artifacts remain ignored; .env.example is intentionally included.
- PASS: standard MIT terms, exact owner-approved `Copyright (c) 2026 DK`, no license placeholders, and removal of LICENSE.draft after validation. Editable installation and Docker wheel packaging include MIT metadata and LICENSE; third-party notices remain present.
- PASS: rebuilt Docker image, non-root read-only runtime, healthcheck, and real HTTP health/Items CRUD. Task 002 Python 3.12/3.13 tests and dependency audit remain the prior baseline; dependencies and backend code did not change in Task 003.
- No unresolved local release blockers. GitHub Private Vulnerability Reporting and Template repository settings are documented but unverified; hosted CI remains an external release gate.
- Git status: 41 untracked files, no staged files or commits. No commits, pushes, tags, releases, visibility changes, or remote changes were performed.

### Exact initial commit files

This list excludes ignored files and the removed license draft. Review it again before staging if the working tree changes.

```text
.dockerignore
.env.example
.github/workflows/ci.yml
.gitignore
AGENTS.md
CONTRIBUTING.md
Dockerfile
LICENSE
PUBLIC_RELEASE_CHECKLIST.md
README.md
SECURITY.md
compose.yaml
pyproject.toml
scripts/smoke.py
src/ddd_fastapi/__init__.py
src/ddd_fastapi/core/__init__.py
src/ddd_fastapi/core/config.py
src/ddd_fastapi/core/errors.py
src/ddd_fastapi/core/logging.py
src/ddd_fastapi/core/middleware.py
src/ddd_fastapi/main.py
src/ddd_fastapi/modules/__init__.py
src/ddd_fastapi/modules/health/__init__.py
src/ddd_fastapi/modules/health/checks.py
src/ddd_fastapi/modules/health/presentation/__init__.py
src/ddd_fastapi/modules/health/presentation/router.py
src/ddd_fastapi/modules/items/__init__.py
src/ddd_fastapi/modules/items/application/__init__.py
src/ddd_fastapi/modules/items/application/service.py
src/ddd_fastapi/modules/items/domain/__init__.py
src/ddd_fastapi/modules/items/domain/models.py
src/ddd_fastapi/modules/items/domain/repository.py
src/ddd_fastapi/modules/items/infrastructure/__init__.py
src/ddd_fastapi/modules/items/infrastructure/repository.py
src/ddd_fastapi/modules/items/presentation/__init__.py
src/ddd_fastapi/modules/items/presentation/router.py
tests/conftest.py
tests/test_api.py
tests/test_config_health.py
tests/test_domain.py
tests/test_service.py
```

### Recommended next commands (owner-run)

From the repository root in PowerShell, review and stage only the listed public files:

```powershell
git status --short
git ls-files --others --exclude-standard
git add -- .dockerignore .env.example .github/workflows/ci.yml .gitignore AGENTS.md CONTRIBUTING.md Dockerfile LICENSE PUBLIC_RELEASE_CHECKLIST.md README.md SECURITY.md compose.yaml pyproject.toml scripts/smoke.py src/ddd_fastapi tests
git diff --cached --check
git diff --cached --stat
git diff --cached
git commit -m "feat: release DDD FastAPI starter v0.1.0"
```

The commit command is a recommendation, not an action taken by the assistant. Separately, the owner must enable and verify GitHub Private Vulnerability Reporting using SECURITY.md, enable **Template repository** in repository settings, and confirm hosted CI before approving public release. No push, tag, or publication is included in these commands.
