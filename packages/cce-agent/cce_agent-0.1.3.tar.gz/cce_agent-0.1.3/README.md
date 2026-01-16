# CCE Agent (CLI)

Context-aware Code Evolution (CCE) Agent is a CLI for running structured code analysis and change workflows
locally or in remote environments (e.g., GitHub Codespaces).

This README is CLI-focused so the PyPI page shows how to install and use the tool.
For architecture and internals, see the docs in this repo.

## Requirements

- Python 3.11+
- Git
- API keys (at least one): `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`

## Install

```bash
pip install cce-agent
# or (isolated)
pipx install cce-agent
```

## Quick start (local)

```bash
# Run CCE locally in the current repo
cce run --issue-url https://github.com/owner/repo/issues/123
```

## Configuration

The CLI reads configuration from (highest priority first):

1) CLI flags
2) Environment variables
3) `cce_config.yaml`
4) Built-in defaults

Common environment variables:

```bash
export OPENAI_API_KEY=...
export ANTHROPIC_API_KEY=...
export LANGSMITH_API_KEY=...   # optional
```

## Command reference

Use `--help` for authoritative defaults and descriptions:

```bash
cce --help
cce run --help
cce run-deep-agents --help
cce launch codespace --help
cce report cycles --help
```

### `cce run` (local)

```bash
cce run --issue-url https://github.com/owner/repo/issues/123 [OPTIONS]
```

Options:

- `--issue-url` (required): GitHub issue URL to process
- `--target-repo`: Target repository slug (owner/repo) for worktree ops when issue is in another repo
- `--target-repo-url`: Target repository URL for worktree ops when issue is in another repo
- `--base-branch`: Base branch for git ops (default: auto)
- `--run-mode`: `demo|guided|expert` (default: guided)
- `--execution-mode`: `native|aider|hybrid` (default: native)
- `--artifact-path`: Directory for JSON/MD summary artifacts
- `--workspace-root`: Workspace root (default: current directory)
- `--no-worktree`: Run in workspace without creating a worktree
- `--enable-git-workflow`: Enable branch/commit integration
- `--auto-pr` / `--no-auto-pr`: Enable/disable automatic PR creation
- `--use-aider` / `--no-aider`: Enable/disable Aider integration
- `--prompt-cache` / `--no-prompt-cache`: Enable/disable prompt caching
- `--recursion-limit`: ReAct (tool loop) recursion limit per execution cycle

### `cce run-deep-agents` (local)

```bash
cce run-deep-agents --issue-url https://github.com/owner/repo/issues/123 [OPTIONS]
```

Options:

- `--issue-url` (required)
- `--target-repo`
- `--target-repo-url`
- `--base-branch`
- `--run-mode`: `demo|guided|expert`
- `--execution-mode`: `native|aider|hybrid`
- `--artifact-path`
- `--workspace-root`
- `--no-worktree`
- `--auto-pr` / `--no-auto-pr`
- `--read-only` / `--edit`
- `--timeout-seconds`: Deep agents timeout (default: 2400 or env override)
- `--max-cycles`: Max deep agents cycles
- `--remaining-steps`: Deep agents remaining_steps budget

### `cce launch codespace` (remote)

```bash
cce launch codespace --codespace <NAME> --issue-url https://github.com/owner/repo/issues/123 [OPTIONS]
```

Options:

- `--codespace` (required): Codespace name from `gh codespace list`
- `--cli-root`: Path to CLI repo in Codespace (dev-only; default: use installed package)
- `--auto-install-cli`: Install cce-agent in the Codespace if missing
- `--cli-version`: Optional cce-agent version to install when auto-installing
- `--workspace-root`: Workspace root (default: `/workspaces/<repo>`)
- `--stream` / `--no-stream`: Enable/disable live output
- `--download-artifacts`: Download artifacts after completion
- `--remote-artifact-path`: Remote artifact path (default: `/tmp/cce-artifacts`)
- `--timeout`: Remote execution timeout (seconds)
- `--use-deep-agents`: Run deep agents workflow in Codespace
- `--deep-agents-read-only`: Deep agents read-only mode
- `--deep-agents-timeout`: Deep agents timeout override (seconds)
- `--deep-agents-max-cycles`: Deep agents max cycles override
- `--deep-agents-remaining-steps`: Deep agents remaining_steps override
- `--issue-url` (required)
- `--target-repo`
- `--target-repo-url`
- `--base-branch`
- `--run-mode`: `demo|guided|expert`
- `--execution-mode`: `native|aider|hybrid`
- `--artifact-path`
- `--no-worktree`
- `--enable-git-workflow`
- `--auto-pr` / `--no-auto-pr`
- `--use-aider` / `--no-aider`
- `--prompt-cache` / `--no-prompt-cache`
- `--recursion-limit`

### `cce report cycles`

```bash
cce report cycles [--output-path /path/to/report.md]
```

Options:

- `--output-path`: Optional output path for the cycle analysis report

## Examples

```bash
# Run locally with worktree + auto PR
cce run --issue-url https://github.com/owner/repo/issues/123 --enable-git-workflow --auto-pr

# Run deep agents locally
cce run-deep-agents --issue-url https://github.com/owner/repo/issues/123 --max-cycles 6

# Launch in Codespace with package-first auto-install
cce launch codespace --codespace my-cs --issue-url https://github.com/owner/repo/issues/123 --auto-install-cli
```

## Development

```bash
pip install -e .
pip install -e ".[dev]"
```

## License

MIT
