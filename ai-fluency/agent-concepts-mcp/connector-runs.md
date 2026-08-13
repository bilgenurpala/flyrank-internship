# GitHub Connector Evidence

## Connection

- Client: Codex
- Connector: GitHub plugin
- Repository: `bilgenurpala/flyrank-internship`
- Access demonstrated: read-only repository file, issue search, and commit search
- Cost observed: no per-call charge was shown during these runs

## Run 01 — Repository File Read

Task: Fetch the live `devlog.md` file from the repository's `main` branch.

Tool result: The connector returned the repository version of the file, including the 2026-08-13 entry about the five-run automation workflow and its citation-export limitation.

Evidence: [run-01-github-file-read.png](screenshots/run-01-github-file-read.png)

## Run 02 — Live Issue Search

Task: Search the repository's current open issues.

Tool result: The connector returned the live issue set, including issue #19 for Three Roads and issue #20 for Empty but Live. It also confirmed that no issue titled Agent Concepts and MCP Basics exists in the repository.

Evidence: [run-02-github-issue-search.png](screenshots/run-02-github-issue-search.png)

## Run 03 — Commit Search

Task: Query the repository's most recent commits.

Tool result: The connector returned commit `2e379b755832b3e554aebd2224825893dffe940d`, titled `docs: ship no-code automation workflow v2`, as the most recent commit at the time of the run.

Evidence: [run-03-github-commit-search.png](screenshots/run-03-github-commit-search.png)

## What These Runs Establish

The three runs demonstrate model-selected tool calls against live external repository state that was not supplied in the chat context. They do not demonstrate the full MCP surface: no resource or prompt primitive was exercised.

Resource selection can vary by host and UI implementation. The explainer uses the general application-controlled distinction, but these runs do not test a resource workflow or establish one universal resource-selection interface.

The connector expanded access, not reasoning quality. Authentication, repository permissions, approval controls, and human verification remain separate concerns.
