# Contributing

Use Python 3.12+ and a virtual environment, then install with `python -m pip install -e ".[dev]"`. Before proposing changes run `ruff check .`, `ruff format --check .`, `pyright`, and `pytest`. Run `python scripts/smoke.py` when startup or HTTP wiring changes. Report actual results and explain behavior changes in pull requests.

Read [AGENTS.md](AGENTS.md) before using Codex or another coding assistant. Give it a bounded task and acceptance criteria, ask it to inspect existing code, and review its diff and verification results. Architecture changes and deployment/publication require explicit approval.

Keep business invariants in framework-free domain code and use narrow Protocol contracts for adapters. New capabilities belong in bounded contexts; add focused domain, application, and API tests. Use application factories and lifespan contexts to avoid test state leakage. Reuse the existing configuration, errors, logging, and providers.

For your own application, use GitHub **Use this template -> Create a new repository** to create an independent repository, then follow the [README template steps](README.md#github-template-usage) for metadata/package renaming, replacing the Items example, and adding a bounded context. Keep private adapters in a separate private package/repository implementing domain contracts; inject them in your composition root instead of adding proprietary code to the public starter.

Never add secrets, private endpoints, or proprietary code. Preserve upstream and third-party license notices. Contributions are provided under the project's [MIT License](LICENSE), copyright (c) 2026 DK. Report vulnerabilities using [SECURITY.md](SECURITY.md). Do not publish or release without explicit owner approval.
