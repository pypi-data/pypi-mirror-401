# AGENTS.md

## Project: Skilz CLI - Universal AI Skills Package Manager

**Status:** Production Ready (v1.7+)

Skilz is the universal package manager for AI skills - think `npm install` but for AI agent skills and tools. It installs and manages skills across 14+ AI coding assistants including Claude Code, OpenCode, Gemini, Codex, and more.

### Quick Links
- 📖 [README.md](README.md) - Project overview
- 📚 [User Manual](docs/USER_MANUAL.md) - Complete usage guide
- 🎯 [Comprehensive Guide](docs/COMPREHENSIVE_USER_GUIDE.md) - All agent-specific instructions
- 🚀 [Gemini Migration](docs/GEMINI_MIGRATION.md) - Gemini CLI support
- 🌐 [Universal Agent Guide](docs/UNIVERSAL_AGENT_GUIDE.md) - Multi-agent setup

### Architecture Overview

**Technology Stack:**
- **Language:** Python 3.10+
- **Package Manager:** Poetry
- **Task Runner:** Task (Go-based)
- **Testing:** pytest (448+ tests, 85%+ coverage)
- **CLI Framework:** Click
- **Config Format:** YAML

**Key Components:**
1. **Registry** - Maps skill IDs to Git repositories and commits
2. **Installer** - Clones repos, checks out commits, copies skills
3. **Agents** - 14+ AI agent adapters (Claude, OpenCode, Gemini, etc.)
4. **Manifest** - Tracks installed skills with `.skilz-manifest.yaml`
5. **Config Sync** - Updates agent config files (AGENTS.md, GEMINI.md, etc.)

**Core Workflows:**
- Install: `registry.yaml` → clone repo → checkout SHA → copy to agent dir → write manifest
- Update: Compare installed SHA vs registry SHA → reinstall if different
- List: Read manifests → check for updates → display status table
- Search: GitHub API → filter repositories → display results

### Build and Development Commands

```bash
# Setup
task install              # Install in development mode
poetry install           # Alternative: direct poetry install

# Testing
task test                # Run all tests (verbose)
task test:fast           # Run tests (fast, no verbose)
task coverage            # Tests with coverage report
task coverage:html       # HTML coverage report

# Quality
task lint                # Ruff linter
task lint:fix            # Auto-fix linting issues
task format              # Format code with ruff
task typecheck           # mypy type checking
task check               # Run all quality checks (lint + type + test)

# Building
task build               # Build distribution packages
task clean               # Remove build artifacts
task ci                  # Full CI pipeline locally

# Shortcuts
task t                   # Alias for test
task c                   # Alias for coverage
task l                   # Alias for lint
task f                   # Alias for format
```

### Code Quality Standards

- **Tests:** 448+ tests, 85%+ coverage, ALL must pass
- **Type Safety:** 100% type hints, mypy strict mode
- **Linting:** Ruff, PEP 8 compliance
- **Documentation:** Docstrings for all public APIs

### Architectural Decisions

**Key Design Principles:**
1. **Registry-Based Resolution** - Skills resolved through YAML registry mapping IDs to Git sources
2. **Reproducible Installs** - Pinned Git SHAs ensure identical installs across environments
3. **Agent Agnostic** - Abstract agent interface supports 14+ different AI tools
4. **Manifest Tracking** - Every install writes `.skilz-manifest.yaml` for auditability
5. **Native vs Universal** - Respects native skill directories, falls back to universal mode

### Project Structure

```
src/skilz/
  ├── cli.py              # Main CLI entry point
  ├── commands/           # Command implementations (install, list, etc.)
  ├── agents.py           # Agent registry and adapters
  ├── installer.py        # Core installation logic
  ├── registry.py         # Registry resolution
  ├── git_ops.py          # Git operations
  ├── config_sync.py      # Config file synchronization
  └── manifest.py         # Manifest file management

tests/
  ├── test_*.py           # Unit tests for each module
  └── conftest.py         # Shared pytest fixtures
```

### Important Notes for Code Changes

1. **Agent Support** - When adding new agent support, update:
   - `src/skilz/agents.py` - Add agent adapter
   - `src/skilz/agent_registry.py` - Register agent
   - Tests for new agent
   - Documentation (README.md, COMPREHENSIVE_USER_GUIDE.md)

2. **Testing** - Always run full test suite before commits:
   ```bash
   task check  # Runs lint + typecheck + test
   ```

3. **Config Sync** - Changes to config sync affect multiple agents:
   - Claude Code: `.claude/skills/` (native, no config sync)
   - OpenCode: `.opencode/skill/` (native, no config sync)
   - Universal: `.skilz/skills/` + AGENTS.md/GEMINI.md (config sync)

4. **Git Operations** - Use `git_ops.py` utilities, never direct git commands

5. **Documentation** - Update docs when changing:
   - CLI commands → USER_MANUAL.md
   - Agent support → COMPREHENSIVE_USER_GUIDE.md
   - Workflows → README.md

---

<skills_system priority="1">

## Available Skills

<!-- SKILLS_TABLE_START -->
<usage>
When users ask you to perform tasks, check if any of the available skills
below can help complete the task more effectively.

How to use skills:
- Invoke: Bash("skilz read <skill-name>")
- The skill content will load with detailed instructions
- Base directory provided in output for resolving bundled resources

Usage notes:
- Only use skills listed in <available_skills> below
- Do not invoke a skill that is already loaded in your context
</usage>

<available_skills>

</available_skills>
<!-- SKILLS_TABLE_END -->

</skills_system>

---

## Quality Assurance Protocol

**IMPORTANT**: After ANY code changes, you MUST:

1. Use the `qa-enforcer` agent (if available) to enforce test coverage and quality standards
2. Run the full quality check pipeline:
   ```bash
   task check  # Runs lint + typecheck + test with coverage
   ```
3. Only consider the task complete after both steps pass successfully

This is a mandatory workflow that should be followed automatically without prompting.

---

## Development Workflow

1. **Make Changes** - Edit code following PEP 8 and type hints
2. **Run Tests** - `task test` or `task coverage`
3. **Check Quality** - `task check` (lint + typecheck + test)
4. **Build** - `task build` (creates wheel and sdist)
5. **Manual Test** - Install locally: `pip install -e .`

---

## Notes for AI Agents

- This is a Python CLI tool using Click framework
- Poetry manages dependencies (pyproject.toml)
- Task manages automation (Taskfile.yml)
- All commands use `skilz` prefix: `skilz install`, `skilz list`, etc.
- Registry format: `owner_repo/skill-name` → Git repo + SHA
- Supports both user-level (`~/.skilz/`) and project-level (`.skilz/`) installs
