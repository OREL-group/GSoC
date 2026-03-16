# Contributing to LLAMOSC

Thank you for your interest in contributing. This document outlines the expected workflow and guidelines.

## How to contribute

1. **Do not push directly to the `main` branch.** All changes must go through pull requests.

2. **Open pull requests against the `develop` branch.**  
   The `develop` branch is used for active development and review. Approved changes may later be merged into `main` by the maintainers.

3. **Ensure CI passes before requesting review.**  
   The PR checks workflow runs syntax validation, import checks, linting, and tests. Your PR must pass these checks before it can be merged.

4. **Avoid changing core behavior without discussion.**  
   Please do not modify agent logic, simulation behavior, or prompts in core research components without prior agreement with maintainers. For such changes, open an issue first to discuss the approach.

## Pull request process

- Use the pull request template when opening a PR.
- Fill in the summary, related issue(s), and the checkboxes for agent/prompt changes and tests.
- Keep pull requests focused and limited to a single purpose when possible.
- Address review feedback and update the PR as requested by maintainers.

## Code owners

Changes to the core LLAMOSC logic (under `Open Source Sustainibility using LLMs/`) require review from the designated code owners. This helps protect repository integrity and research components.

## Questions

If you have questions about contributing or the scope of an issue, please open a GitHub issue and tag the maintainers.