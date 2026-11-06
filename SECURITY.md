# Security

## Supported versions

The release target is v0.1.0. Once released, security fixes target the latest patch of the latest released minor series (initially 0.1.x). Earlier minor series and unreleased development snapshots have no guaranteed security backports. Upgrade to the latest supported patch before reporting an issue. Derived applications maintain their own support policies.

## Report a vulnerability privately

Use GitHub Private Vulnerability Reporting: open this repository's **Security -> Advisories -> Report a vulnerability** form. Include affected versions, reproduction steps, impact, and a minimal example with secrets removed. Do not disclose vulnerabilities, exploit details, or credentials in public issues or pull requests.

If the private reporting button is unavailable, ask the owner to enable it; a public request must contain no vulnerability details. No response-time SLA is promised.

## Owner configuration required

Enable private reporting in GitHub:

**Repository -> Settings -> Security -> Code security -> Private vulnerability reporting -> Enable**

GitHub may instead label this area **Settings -> Security and quality -> Advanced Security**. See [GitHub's configuration guide](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository).

The repository owner must configure this setting and verify that **Report a vulnerability** is available under **Security -> Advisories**. This file documents the policy; it does not enable the setting. Enablement has not been verified during local release preparation. Owners of repositories created from this template must configure their own reporting settings.

## Deployment scope

This starter has no authentication or authorization. Add these controls before exposing protected resources. In-memory data is demonstration-only. Use HTTPS, restrict network access, set explicit CORS origins, and store deployment secrets outside source control. Keep dependencies updated and review advisories in your consuming project.
