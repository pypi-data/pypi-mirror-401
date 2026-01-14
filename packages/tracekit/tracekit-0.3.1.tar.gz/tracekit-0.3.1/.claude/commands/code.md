# /code - Quick Ad-Hoc Code Writing

Force ad-hoc code writing workflow without specifications.

## Purpose

Bypass intelligent routing and go directly to `code_assistant` agent for fast, informal code writing without requiring TASK-XXX identifiers or requirements.yaml.

## Usage

```bash
/code <task>                    # Write code ad-hoc
/code write a function...       # Quick function
/code add error handling...     # Quick fix
/code create utility script...  # Quick script
```

## When to Use

✅ **Use /code when**:

- Writing quick utilities or helper functions
- Creating prototypes or proof-of-concepts
- Adding simple features or fixes
- Learning and experimentation
- You want fast results without formal validation

❌ **Don't use /code when**:

- Task is complex and needs requirements → Use `/ai` or `/feature`
- Task has TASK-XXX identifier → Use `/implement TASK-XXX`
- You need formal validation → Use `/feature` or spec workflow
- You just need documentation → Use `/doc`

## How It Works

```
/code <task>
  ↓
Force route to code_assistant (bypass orchestrator intelligence)
  ↓
code_assistant writes code quickly
  ↓
Returns: Code + usage example + brief explanation
```

No spec created, no formal validation, no task graph.

## Examples

### Example 1: Quick Function

```bash
/code write a function to calculate factorial
```

→ code_assistant creates function directly, no questions asked

### Example 2: Utility Script

```bash
/code create a script to backup logs
```

→ code_assistant writes script immediately

### Example 3: Bug Fix

```bash
/code fix the null pointer error in login function
```

→ code_assistant reads code and applies fix

## Comparison with Other Commands

| Command      | Speed          | Validation | Spec Required   | Use Case                    |
| ------------ | -------------- | ---------- | --------------- | --------------------------- |
| `/code`      | ⚡ Fast        | Basic      | ❌ No           | Quick utilities, prototypes |
| `/feature`   | ⏱️ Medium      | Formal     | Auto-generated  | Structured features         |
| `/implement` | ⏱️ Medium      | Formal     | ✅ Yes (manual) | Complex features with specs |
| `/ai`        | 🤖 Intelligent | Varies     | Auto-decided    | Let system choose           |

## After Using /code

What you can do next:

1. **Use the code** - It's ready to use immediately
2. **Test it** - `/ai write tests for this function`
3. **Review it** - `/review path/to/file.py`
4. **Commit it** - `/git "add utility function"`
5. **Formalize it** - If code grows complex, create spec with `/spec create`

## Warning

If you use `/code` for a complex task, the agent will warn you:

```
⚠️ This task seems complex. Consider using /feature or /ai instead for:
- Better validation
- Requirement tracking
- Structured implementation
Proceed anyway? [y/N]
```

## Aliases

The following aliases work identically:

- `/quick` → `/code`
- `/snippet` → `/code`
- `/write` → `/code`

## Agent

Routes to: **code_assistant** (always, no routing logic)

## Version

v1.0.0 (2026-01-09) - Initial creation as part of workflow system overhaul
