# Getting Started with Claude Code - TraceKit

Welcome to the TraceKit Claude Code orchestration system! This guide explains the **intelligent three-path workflow system** that automatically routes your tasks to the right agent with the right approach.

**Version**: 3.0.0 (2026-01-09) - Complete system overhaul

## Table of Contents

1. [Quick Start](#quick-start)
2. [Understanding the Three Workflows](#understanding-the-three-workflows)
3. [Commands Overview](#commands-overview)
4. [Available Agents](#available-agents)
5. [Common Workflows](#common-workflows)
6. [Best Practices](#best-practices)
7. [Configuration](#configuration)
8. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Your First Command

**Not sure what to do? Just use `/ai`** - the system will figure out the rest:

```bash
# Write a simple function (system routes to ad-hoc workflow)
/ai write a function to calculate factorial

# Build a feature (system routes to auto-spec workflow)
/ai implement user authentication with JWT

# Research something (system routes to research agent)
/ai research Docker networking best practices 2026
```

### Check System Status

```bash
/status              # System health
/agents              # List available agents
/help                # Show all commands
```

---

## Understanding the Three Workflows

The system intelligently routes your tasks through **three different paths** based on complexity:

### Path 1: Ad-Hoc (No Requirements) 🏃 **FAST**

**For**: Quick utilities, simple functions, prototypes, bug fixes
**Command**: `/code <task>` or let `/ai` decide
**Agent**: code_assistant
**Creates**: Code only (no spec, no validation)
**Speed**: ⚡ Fastest (minutes)

**Example**:

```bash
/ai write a function to validate email addresses
# or explicitly:
/code write a function to validate email addresses
```

**Output**: Function with docstring, ready to use immediately.

---

### Path 2: Auto-Spec (System Generates) 🤖 **SMART**

**For**: Medium complexity features (not trivial, not massive)
**Command**: `/feature <task>` or let `/ai` decide
**Workflow**: Generate lightweight requirements → implement → validate
**Creates**: Requirements.yaml (auto-generated) + code + validation report
**Speed**: ⏱️ Medium (15-30 minutes)

**Example**:

```bash
/ai implement API endpoint for user registration
# or explicitly:
/feature implement API endpoint for user registration
```

**What Happens**:

1. System analyzes complexity (score: 55)
2. Generates AUTO-001 requirements with acceptance criteria
3. Asks: "Review requirements? [Y/n]"
4. Implements using spec_implementer
5. Validates using spec_validator
6. Returns: Code + tests + validation report

---

### Path 3: Manual Spec (User Writes) 📋 **FORMAL**

**For**: Complex features with detailed requirements
**Command**: `/spec extract` → `/implement TASK-XXX`
**Workflow**: User writes spec → extract tasks → implement → validate
**Creates**: Full requirements.yaml + task graph + code + validation
**Speed**: ⏱️ Thorough (hours)

**Example**:

```bash
# Step 1: Write requirements.md manually
vim requirements.md

# Step 2: Extract to formal spec
/spec extract requirements.md

# Step 3: Implement each task
/implement TASK-001

# Step 4: Validate
/validate TASK-001

# Step 5: Commit
/git "implement authentication system (TASK-001)"
```

---

## How the System Decides

The orchestrator calculates a **complexity score (0-100)** to choose the path:

| Score     | Path        | Example                              |
| --------- | ----------- | ------------------------------------ |
| **0-30**  | Ad-Hoc      | "write a function to reverse string" |
| **31-70** | Auto-Spec   | "implement JWT authentication"       |
| **71+**   | Manual Spec | "build complete OAuth system"        |

### Complexity Factors

**Increases Score (+)**:

- Security/auth keywords: +30
- Database/state: +20
- API integration: +15
- Multiple components: +15 each
- Validation needed: +10

**Decreases Score (-)**:

- "function", "helper", "utility": -30
- "quick", "simple", "small": -20
- "prototype", "example": -15

**You can override** with explicit commands: `/code`, `/feature`, `/implement`

---

## Commands Overview

### Tier 1: Universal Entry Point

| Command      | Purpose                | Intelligence          |
| ------------ | ---------------------- | --------------------- |
| `/ai <task>` | Universal task handler | ✅ Full routing logic |

Use `/ai` when unsure - the system will figure out the workflow.

---

### Tier 2: Workflow Commands (Explicit Control)

| Command             | Force Path | Use Case            | Example                           |
| ------------------- | ---------- | ------------------- | --------------------------------- |
| `/code <task>`      | Ad-Hoc     | Quick utilities     | `/code write helper function`     |
| `/feature <task>`   | Auto-Spec  | Structured features | `/feature implement caching`      |
| `/research <topic>` | N/A        | Web research        | `/research Docker best practices` |
| `/doc <what>`       | N/A        | Documentation       | `/doc create API guide`           |
| `/review [path]`    | N/A        | Code review         | `/review src/auth/`               |

---

### Tier 3: Spec Workflow (Manual)

| Command                | Purpose           | Example                         |
| ---------------------- | ----------------- | ------------------------------- |
| `/spec extract <file>` | Create task graph | `/spec extract requirements.md` |
| `/implement TASK-XXX`  | Implement task    | `/implement TASK-001`           |
| `/validate TASK-XXX`   | Run validation    | `/validate TASK-001`            |

---

### Tier 4: System Commands

| Command                 | Purpose       | Example                           |
| ----------------------- | ------------- | --------------------------------- |
| `/agents`               | List agents   | `/agents`                         |
| `/route <agent> <task>` | Force routing | `/route code_assistant "fix bug"` |
| `/help [cmd]`           | Documentation | `/help code`                      |
| `/status`               | System health | `/status`                         |
| `/context`              | Context usage | `/context`                        |
| `/cleanup`              | Maintenance   | `/cleanup`                        |
| `/git [msg]`            | Smart commits | `/git "add feature"`              |

---

## Available Agents

The system dynamically discovers agents from `.claude/agents/*.md`:

### Code Writing

- **code_assistant** (sonnet)
  - **Purpose**: Ad-hoc code without specifications
  - **Use**: Quick functions, utilities, prototypes, simple fixes
  - **Command**: `/code <task>`

- **spec_implementer** (sonnet)
  - **Purpose**: Formal implementation from requirements
  - **Use**: Complex features with TASK-XXX identifiers
  - **Command**: `/implement TASK-XXX`

### Validation

- **spec_validator** (sonnet)
  - **Purpose**: Validate against acceptance criteria
  - **Use**: After spec_implementer completes
  - **Command**: `/validate TASK-XXX`

### Research & Documentation

- **knowledge_researcher** (opus)
  - **Purpose**: Web research with citations
  - **Use**: Learning technologies, best practices, comparisons
  - **Command**: `/research <topic>`

- **technical_writer** (sonnet)
  - **Purpose**: Create documentation and tutorials
  - **Use**: API docs, user guides, architecture docs
  - **Command**: `/doc <what>`

### Quality & Operations

- **code_reviewer** (sonnet)
  - **Purpose**: Code quality audits and security reviews
  - **Use**: Pre-commit reviews, security audits
  - **Command**: `/review [path]`

- **git_commit_manager** (sonnet)
  - **Purpose**: Git operations with conventional commits
  - **Use**: Creating commits, managing version control
  - **Command**: `/git [msg]`

### Orchestration

- **orchestrator** (opus)
  - **Purpose**: Routes tasks and coordinates workflows
  - **Use**: Every `/ai` command (automatic)
  - **Command**: `/ai <task>`

**To see all agents**: `/agents` or `/agents --verbose`

---

## Common Workflows

### 1. Write Quick Code (Ad-Hoc)

```bash
# System decides (complexity: 25)
/ai write a function to parse CSV files

# Or force ad-hoc
/code write a function to parse CSV files
```

**Result**: Function created immediately, no spec, ready to use.

---

### 2. Build a Feature (Auto-Spec)

```bash
# System decides (complexity: 60)
/ai implement caching system with Redis

# Or force auto-spec
/feature implement caching system with Redis
```

**What Happens**:

1. "Task looks moderately complex. Generate requirements? [Y/n]"
2. Creates AUTO-001 with acceptance criteria
3. Implements with spec_implementer
4. Validates with spec_validator
5. Returns code + tests + validation report

---

### 3. Complex Feature (Manual Spec)

```bash
# Step 1: Write requirements
cat > requirements.md << 'EOF'
# User Authentication System

## Requirements
- User registration with email verification
- Login with JWT tokens
- Password reset workflow
- Role-based access control
EOF

# Step 2: Extract spec
/spec extract requirements.md

# Step 3: Implement tasks
/implement TASK-001  # Registration
/implement TASK-002  # Login
/implement TASK-003  # Password reset

# Step 4: Validate each
/validate TASK-001
/validate TASK-002
/validate TASK-003

# Step 5: Commit
/git "implement authentication system"
```

---

### 4. Research Before Coding

```bash
# Research best practices
/research JWT authentication best practices 2026

# Then implement based on research
/feature implement JWT authentication using best practices
```

---

### 5. Code → Review → Document → Commit

```bash
# Write code
/code implement rate limiting middleware

# Review quality
/review src/middleware/rate_limiter.py

# Fix issues from review
/code fix rate limiter issues from review

# Create documentation
/doc document rate limiting system

# Commit
/git "add rate limiting with documentation"
```

---

### 6. Bug Fix Workflow

```bash
# Quick fix
/code fix null pointer error in login handler

# Or with investigation
/ai investigate and fix the authentication timeout bug
```

---

## Best Practices

### 1. Let `/ai` Decide First

```bash
# ✅ Good: Let system choose workflow
/ai implement user authentication

# ⚠️ Also fine: Force specific workflow if you know
/code write a quick auth helper
/feature implement complete auth system
```

### 2. Use Appropriate Granularity

```bash
# ✅ Ad-hoc: Simple, self-contained
/code write a function to validate emails

# ✅ Auto-spec: Medium complexity
/feature add email validation to registration

# ✅ Manual spec: Complex, multi-component
/spec extract requirements.md  # For full auth system
```

### 3. Explicit Commands for Deterministic Routing

```bash
# In scripts or automation
/code generate migration script    # Always ad-hoc
/feature implement new endpoint    # Always auto-spec
/implement TASK-001                # Always formal
```

### 4. Use `/agents` to Understand Routing

```bash
# See all agents and their keywords
/agents --verbose

# Search for specific capability
/agents code
/agents research
```

### 5. Override Wrong Routing

```bash
# If orchestrator routes wrong
/ai write a quick helper
# → Routes to auto-spec (wrong!)

# Override with explicit command
/code write a quick helper
# → Routes to code_assistant (correct!)
```

---

## Configuration

All behavioral settings are in `.claude/config.yaml` (Single Source of Truth).

### Workflow Thresholds

```yaml
orchestration:
  workflow:
    ad_hoc_max: 30 # 0-30 = ad-hoc
    auto_spec_max: 70 # 31-70 = auto-spec
    manual_spec_min: 71 # 71+ = suggest manual

    auto_spec_enabled: true # Enable /feature
    auto_spec_prompt: true # Ask before generating
    auto_spec_auto_approve: false
```

### Agent Limits

```yaml
orchestration:
  agents:
    max_concurrent: 2 # Max agents running simultaneously
    max_batch_size: 2 # Max agents per batch
```

### Context Management

```yaml
orchestration:
  context:
    warning_threshold: 60 # Show warning at 60%
    checkpoint_threshold: 65 # Create checkpoint at 65%
    critical_threshold: 75 # Stop at 75%
```

**See full config**: `.claude/config.yaml`

---

## Troubleshooting

### System Routes to Wrong Agent

**Problem**: `/ai write a function` → routes to spec_implementer
**Solution**: Use explicit command: `/code write a function`

Or check routing with:

```bash
/agents --verbose  # See routing keywords
```

---

### Task Too Complex for Ad-Hoc

**Problem**: `/code implement complete API` → warns about complexity
**Solution**: Use appropriate workflow:

```bash
/feature implement complete API    # Auto-spec
# or
/spec extract requirements.md      # Manual spec
```

---

### Want to See Routing Decision

Enable in config:

```yaml
orchestration:
  workflow:
    show_routing_decisions: true
```

Now `/ai` will show:

```
Analyzing task... (complexity: 45)
→ Routing to: AUTO_SPEC
  Reason: Moderate complexity, multiple components
  Agent: orchestrator → spec_implementer → spec_validator
```

---

### Agent Not Found

**Problem**: `/route nonexistent_agent "task"`
**Solution**: List available agents: `/agents`

---

### Context Usage High

**Check**: `/context`
**Solution**: System auto-manages with checkpoints and summaries

---

## Advanced Features

### Force Specific Agent

```bash
# Bypass all routing logic
/route code_assistant "implement complex feature"

# See what orchestrator would do (dry run)
/ai --dry-run implement authentication
```

### Parallel Agent Coordination

```bash
# For comprehensive multi-perspective work
/swarm comprehensive analysis of microservices architecture
```

---

## Learning Path

1. **Day 1**: Use `/ai` for everything - learn what the system does
2. **Week 1**: Start using `/code` for quick tasks
3. **Month 1**: Use `/feature` for structured development
4. **Month 2**: Try manual `/spec` workflow for complex features
5. **Expert**: Use `/route` and understand full system

---

## Quick Reference

### Decision Tree

```
Need to code something?
├─ Simple/quick? → /code
├─ Medium complexity? → /feature (or /ai)
├─ Very complex? → /spec extract → /implement
├─ Research? → /research
├─ Documentation? → /doc
└─ Review? → /review
```

### When in Doubt

**Just use `/ai` and let the system decide!**

---

## Getting Help

```bash
/help                # All commands
/help code           # Specific command
/agents              # List agents
/status              # System health
```

**Documentation**:

- This file: `.claude/GETTING_STARTED.md`
- Config reference: `.claude/config.yaml`
- Command docs: `.claude/commands/*.md`
- Agent docs: `.claude/agents/*.md`

---

**Welcome to intelligent code development with Claude Code! 🚀**
