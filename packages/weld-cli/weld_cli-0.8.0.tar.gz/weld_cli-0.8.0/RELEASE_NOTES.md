### Added
- `--autopilot` flag for `weld implement` command
  - Executes all plan steps automatically without user intervention
  - After each step: runs code review with auto-fix, then commits
  - Stops on first Claude failure
  - Designed for CI/automation and unattended execution

### Changed
- `--dangerously-skip-permissions` now defaults to `True` for `weld plan` command
  - Plans are generated without permission prompts by default
  - Use `--no-dangerously-skip-permissions` to restore previous behavior
- All Claude CLI invocations now use `skip_permissions=True` for smoother automated workflows

### Fixed
- Plan prompt template restructured with explicit WRONG/CORRECT format examples
  - Shows concrete anti-pattern to avoid (bullet-point summaries)
  - Provides complete correct example with all required sections
  - Adds output format checklist as final reminder before generation
  - Explicitly forbids questions, follow-up options, and conversational closing
  - Clarifies CLI context: output goes directly to file, not interactive chat
