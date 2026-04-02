# Security Incident Response - Legacy Backend Workflow Leak

## Incident

- File removed: `musepicker_back/.github/workflows/github_actions_security.yml`
- Behavior: workflow attempted to POST GitHub secrets to an external domain.

## Required Actions (Manual, Immediate)

1. Rotate all potentially exposed credentials:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `DB_HOST`
   - `DB_USERNAME`
   - `DB_PASSWORD`
   - `GOOGLE_API_KEY`
2. Invalidate and recreate any cloud IAM credentials that may have been exposed.
3. Audit GitHub Actions run history for this workflow and identify execution timestamps and actors.
4. Review GitHub repository secrets and environment secrets for least privilege.
5. Enable branch protection + required reviews on workflow file changes.
6. Restrict GitHub Actions permissions:
   - Set default workflow permissions to `read` unless write is required.
   - Use OIDC short-lived credentials instead of long-lived static cloud secrets.
7. Review Git commit history for secret exposure and perform remediation if required.

## Local Code Changes Applied

- Deleted exfiltration workflow file.
- Removed hardcoded DB and API secrets from legacy `application.properties`.
- Replaced with environment-variable based configuration.
- Updated legacy backend deploy workflow to OIDC role assumption (no static AWS access keys).
