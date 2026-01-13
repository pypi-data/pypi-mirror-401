### Added
- `--dangerously-skip-permissions` flag for `weld plan` command
  - Allows Claude to explore codebase (read files, search patterns) during plan generation
  - Required when Claude needs file access to create comprehensive plans
  - Matches behavior of `weld implement` command
- `--no-review` flag for `weld implement` command
  - Skips post-step review prompt to avoid Claude CLI date serialization bugs
  - Workaround for "RangeError: Invalid time value" errors during review step
  - Useful when Claude CLI stats cache has issues
- Multiple transcript gist support in `weld commit` fallback mode
  - Now uploads separate gists for each session that contributed to staged files
  - Example: implement session + review session = 2 gists attached to commit
  - Each gist labeled with command type (implement, review, etc.)
  - Provides complete context for understanding changes
- Smart error recovery in `weld implement` command
  - When Claude crashes after making file changes, detects modifications and prompts user
  - Allows marking step as complete despite Claude error if work was actually done
  - Prevents losing progress when Claude has internal failures
  - Only prompts if file changes detected; genuine failures still return error

### Changed
- Enhanced `weld plan` prompt with 10 implementation plan rules
  - Monotonic phases, discrete steps, artifact-driven output
  - Explicit dependencies, vertical slices, invariants first
  - Test parallelism, rollback safety, bounded scope, execution ready
  - Rules condensed to minimize context usage while enforcing plan quality
- Optimized `weld implement` prompt to skip redundant test runs
  - When Claude identifies a step as already complete (but not marked), checks git status first
  - If worktree is clean: marks step complete without running tests
  - If worktree is dirty: reviews uncommitted changes and proceeds without re-running tests
  - Significant time savings when resuming after crashes or re-running completed steps

### Fixed
- **Critical**: Plan generation now strictly enforces required Phase → Step format
  - Added explicit format requirements to prompt to prevent conversational output
  - Added validation to reject plans that don't start with "## Phase" or lack steps
  - Fixed issue where Claude would output summaries/questions instead of structured plans
  - Plans now correctly follow docs/reference/plan-format.md specification
- **Critical**: `weld commit` now attaches transcripts from ALL relevant sessions
  - Fallback flow finds all sessions from registry that match staged files
  - Uploads one gist per matching session (e.g., implement + review)
  - Fixes issue where only one transcript was attached when multiple sessions contributed
  - Each transcript gets its own trailer line in commit message
