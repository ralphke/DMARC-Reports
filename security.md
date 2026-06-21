# Security Policy

This repository uses branch protection to ensure that changes cannot be merged into `main` without a pull request and review.

## Required workflow

- Do not push changes directly to `main`.
- Create a feature branch for any change.
- Open a pull request targeting `main`.
- Wait for review and approval before merging.

## Pull request requirements

The following protections should be enforced for the `main` branch:

- Require pull requests for all merges into `main`.
- Require at least one review from the repository owner or maintainer before merge.
- Require status checks to pass before merging (where applicable).
- Disable direct pushes to `main`.
- Require up-to-date branches before merging if possible.

## Review expectations

- Reviewers should verify that code changes are appropriate for DMARC report collection, parsing, and Power BI reporting.
- Reviewers should confirm that credential-handling files such as `.env` are not committed.
- Security-sensitive configuration and secrets should never be stored in the repository.

## How to configure branch protection

1. Go to the repository on GitHub.
2. Open **Settings** → **Branches**.
3. Add a branch protection rule for `main`.
4. Enable:
   - "Require pull request reviews before merging"
   - "Require review from Code Owners" (optional if code owners are configured)
   - "Require status checks to pass before merging"
   - "Include administrators" if administrators should also follow the rule
   - "Restrict who can push to matching branches" (optional)

## Notes

- If you use GitHub Actions or other CI, configure it to report status checks on PRs.
- Keep secrets out of the repository and use environment variables for runtime credentials.
