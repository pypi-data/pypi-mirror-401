# /agents - List Available Agents

Show all available agents with their capabilities, keywords, and use cases.

## Usage

```bash
/agents               # List all agents
/agents code          # Search agents by keyword
/agents --verbose     # Show routing keywords
```

## Purpose

Help users understand:

- What agents are available
- When to use each agent
- What keywords trigger which agent
- How routing works

## Output Format

### Default View

```
Available Agents (7):

1. orchestrator (opus)
   → Routes tasks to specialists and coordinates multi-agent workflows
   Use: Complex multi-step tasks, workflow coordination

2. code_assistant (sonnet)
   → Writes ad-hoc code without specifications
   Use: Quick functions, utilities, prototypes, simple fixes

3. spec_implementer (sonnet)
   → Implements from specifications with TASK-XXX identifiers
   Use: Formal feature development with requirements

4. spec_validator (sonnet)
   → Validates implementations against acceptance criteria
   Use: After spec_implementer, to verify requirements met

5. knowledge_researcher (opus)
   → Web research with citations and comprehensive analysis
   Use: Learning new technologies, best practices, comparisons

6. technical_writer (sonnet)
   → Creates documentation, tutorials, and guides
   Use: API docs, user guides, architecture documentation

7. code_reviewer (sonnet)
   → Code quality audits, security reviews, best practices
   Use: Pre-commit reviews, security audits, quality checks

8. git_commit_manager (sonnet)
   → Git operations with conventional commit format
   Use: Creating commits, managing version control
```

### Verbose View (`--verbose`)

```
Available Agents (7):

1. orchestrator (opus) - .claude/agents/orchestrator.md
   → Routes tasks to specialists and coordinates multi-agent workflows
   Keywords: route, coordinate, delegate, workflow, multi-step
   Use: Complex multi-step tasks, workflow coordination

2. code_assistant (sonnet) - .claude/agents/code_assistant.md
   → Writes ad-hoc code without specifications
   Keywords: write, create, add, function, script, utility, helper, quick, simple
   Use: Quick functions, utilities, prototypes, simple fixes
   Anti-keywords: TASK-, implement (formal), requirements

3. spec_implementer (sonnet) - .claude/agents/spec_implementer.md
   → Implements from specifications with TASK-XXX identifiers
   Keywords: implement, TASK-, module, formal, requirements
   Use: Formal feature development with requirements
   Requires: TASK-XXX identifier or auto-generated requirements.yaml

[... etc for all agents]
```

### Search View (`/agents code`)

```
Agents matching "code" (3):

1. code_assistant (sonnet)
   → Writes ad-hoc code without specifications
   Match: Keywords include "code" context words

2. spec_implementer (sonnet)
   → Implements from specifications
   Match: Keywords include "code, build, develop"

3. code_reviewer (sonnet)
   → Code quality audits and reviews
   Match: Keywords include "code review, quality"
```

## When to Use /agents

✅ **Use /agents when**:

- Learning the system for the first time
- Unsure which agent handles a task
- Want to understand routing keywords
- Debugging routing issues (wrong agent selected)
- Discovering available capabilities

## Examples

### Example 1: List All

```bash
/agents
```

Shows complete list with descriptions.

### Example 2: Search

```bash
/agents document
```

Returns: technical_writer agent details.

### Example 3: Verbose

```bash
/agents --verbose
```

Shows all agents with full keyword lists and file paths.

## Understanding Agent Roles

### Code Writing

- **code_assistant**: Ad-hoc code (no spec)
- **spec_implementer**: Formal code (with spec)

### Quality & Review

- **spec_validator**: Validates against requirements
- **code_reviewer**: Reviews for quality/security

### Knowledge & Documentation

- **knowledge_researcher**: Web research
- **technical_writer**: Create docs

### Operations

- **git_commit_manager**: Git operations
- **orchestrator**: Coordinates all agents

## Routing Priority

The orchestrator uses this priority to select agents:

1. **Explicit Commands** (HIGHEST)
   - `/code` → code_assistant
   - `/feature` → auto-spec workflow
   - `/research` → knowledge_researcher
   - `/doc` → technical_writer
   - `/review` → code_reviewer

2. **TASK-XXX Identifiers** (HIGH)
   - Any TASK-XXX → spec_implementer

3. **Complexity Scoring** (MEDIUM)
   - Score 0-30 → code_assistant
   - Score 31-70 → auto-spec workflow
   - Score 71+ → suggest manual spec

4. **Keyword Matching** (FALLBACK)
   - Match user request against agent keywords
   - Select highest-scoring agent

## How to Force Specific Agent

If orchestrator routes to wrong agent:

1. **Use explicit command**:

   ```bash
   /code <task>       # Force code_assistant
   /feature <task>    # Force auto-spec
   /research <topic>  # Force knowledge_researcher
   ```

2. **Use /route command**:

   ```bash
   /route code_assistant "write a function"
   ```

3. **Improve request phrasing**:
   ```bash
   # Instead of: "make auth"
   # Use: "write a quick auth function" → code_assistant
   # Or: "implement TASK-001 authentication" → spec_implementer
   ```

## Agent Discovery

Agents are **dynamically discovered** from `.claude/agents/*.md`:

1. System scans directory for `*.md` files
2. Parses YAML frontmatter for metadata
3. Extracts `routing_keywords` list
4. Builds routing table at runtime

This means:

- ✅ Adding new agents is automatic
- ✅ No hardcoded routing tables
- ✅ System is extensible
- ✅ Custom agents work immediately

## Configuration

Agent behavior controlled in `.claude/config.yaml`:

```yaml
orchestration:
  agents:
    max_concurrent: 2 # Max simultaneous agents
    max_batch_size: 2 # Max per batch

  workflow:
    show_routing_decisions: true # Show why agent was selected
    allow_command_overrides: true # Allow /code, /feature, etc
```

## Related Commands

| Command                 | Purpose                       |
| ----------------------- | ----------------------------- |
| `/agents`               | List available agents         |
| `/route <agent> <task>` | Force route to specific agent |
| `/help`                 | Show all commands             |
| `/status`               | System health                 |

## Version

v1.0.0 (2026-01-09) - Initial creation as part of utility command system
