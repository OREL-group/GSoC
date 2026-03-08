# Contributing to LLAMOSC

Thank you for your interest in contributing. This document outlines the expected workflow and guidelines.

## How to contribute

1. **Do not push directly to the main (or default) branch.** All changes must go through pull requests.
2. **Open a pull request** against the repository’s default branch. If the project uses a `develop` branch, target that for feature work; otherwise target `main`.
3. **Ensure CI passes** before requesting review. The PR checks workflow runs syntax validation, import checks, linting, and tests. Your PR must pass these checks before it can be merged.
4. **Avoid changing core behavior without discussion.** Please do not modify agent logic, simulation behavior, or prompts in core research components without prior agreement with maintainers. For such changes, open an issue first to discuss the approach.

## Pull request process

- Use the pull request template when opening a PR. Fill in the summary, related issue(s), and the checkboxes for agent/prompt changes and tests.
- Address review feedback and keep the PR focused. Smaller, single-purpose PRs are easier to review.
- Maintainers may request changes; please update the PR accordingly.

## Code owners

Changes to the core LLAMOSC logic (under `Open Source Sustainibility using LLMs/`) require review from the designated code owners. This helps protect repository integrity and research components.

## Questions

If you have questions about contributing or the scope of an issue, please open a GitHub issue and tag the maintainers.
