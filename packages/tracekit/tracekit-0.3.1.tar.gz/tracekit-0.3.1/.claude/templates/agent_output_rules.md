# Agent Output Rules

## Purpose

Standardizes how agents produce output to prevent context explosion during orchestration.
This template defines the file-based output pattern that all agents MUST follow.

## Core Principle

**File-based output, not in-context output.**

Agents write detailed results to files and return only brief summaries. This prevents
individual agents from generating excessive tokens that accumulate in the orchestrator's
context.

## Output Size Limits

| Output Type      | Max Tokens | Action if Exceeded       |
| ---------------- | ---------- | ------------------------ |
| Return summary   | 2,000      | Truncate, reference file |
| In-context data  | 5,000      | Force file-based output  |
| Per-agent budget | 50,000     | Summarize immediately    |

## Required Output Pattern

### Step 1: Write Detailed Output to File

```python
# Agent writes full output to designated location
output_path = ".claude/agent-outputs/{agent_id}-output.json"

output_data = {
    "agent_id": agent_id,
    "task": task_description,
    "status": "complete",
    "detailed_results": full_results,  # All verbose data here
    "artifacts": list_of_created_files,
    "timestamp": iso_timestamp
}

# Write to file FIRST
write_to_file(output_path, output_data)
```

### Step 2: Return Brief Summary Only

```python
# Agent returns ONLY summary to orchestrator
return {
    "status": "complete",
    "summary": "Brief 1-2 sentence description of what was done",
    "key_findings": ["Finding 1", "Finding 2"],  # Max 5 items
    "output_file": output_path,  # Reference to detailed output
    "artifacts": ["list", "of", "files"],  # Created files only
    "next_steps": "Recommendation for orchestrator"  # Optional
}
```

## Summary Structure

### Mandatory Fields

- `status`: complete | blocked | needs-review
- `summary`: 1-2 sentences max
- `output_file`: Path to detailed output

### Optional Fields

- `key_findings`: Array of max 5 bullet points
- `artifacts`: Array of created file paths
- `next_steps`: Single recommendation
- `metrics`: Object with key numbers only

## Anti-Patterns (DO NOT DO)

1. **Returning full file contents**

   ```python
   # BAD - Returns entire file content
   return {"result": read_entire_file(path)}
   ```

2. **Embedding verbose output in summary**

   ```python
   # BAD - Verbose output in return
   return {"details": "..." * 10000}
   ```

3. **Returning lists of all items found**

   ```python
   # BAD - Returns all 500 items
   return {"files": all_500_files}

   # GOOD - Returns count and reference
   return {"file_count": 500, "list_file": ".claude/outputs/file_list.txt"}
   ```

4. **Including stack traces in return**

   ```python
   # BAD - Full traceback
   return {"error": full_traceback}

   # GOOD - Brief error with reference
   return {"error": "ImportError in module X", "details_file": "error_log.txt"}
   ```

## Enforcement

This pattern is enforced by:

1. **PreToolUse hook (enforce_agent_limit.py)**: Blocks new agents if limit reached
2. **SubagentStop hook (check_subagent_stop.py)**: Validates completion reports exist
3. **Orchestrator review**: Orchestrator checks output_file exists

## Examples

### Good Agent Output

```json
{
  "status": "complete",
  "summary": "Fixed 5 type errors in loader module",
  "key_findings": [
    "Missing Optional wrapper on 3 parameters",
    "Incorrect return type annotation on parse_header",
    "Unused import causing type conflict"
  ],
  "output_file": ".claude/agent-outputs/a1b2c3d4-output.json",
  "artifacts": [
    "src/tracekit/loaders/binary.py",
    "src/tracekit/loaders/validation.py"
  ]
}
```

### Bad Agent Output (Will Cause Context Issues)

```json
{
  "status": "complete",
  "summary": "Here are all the changes I made...",
  "changes": [
    {
      "file": "...",
      "before": "... 500 lines ...",
      "after": "... 500 lines ..."
    },
    {
      "file": "...",
      "before": "... 500 lines ...",
      "after": "... 500 lines ..."
    }
  ],
  "full_test_output": "... 5000 lines of pytest output ..."
}
```

## Integration with Orchestrator

The orchestrator:

1. **Launches agent** with task description
2. **Retrieves output** via TaskOutput
3. **Validates** output follows this pattern
4. **Reads detailed results** from output_file if needed
5. **Summarizes** for next agent handoff

## Version

- Version: 1.0.1
- Created: 2025-12-30
- Updated: 2026-01-06
- Enforcement: Via hooks in .claude/hooks/
