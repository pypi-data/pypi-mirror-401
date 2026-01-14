---
name: context
description: Display context usage and optimization recommendations
arguments: []
---

# Context Command

Analyze current context usage and provide actionable optimization recommendations.

## Usage

```bash
/context           # Show context analysis and recommendations
```

## Examples

```bash
/context           # Display current context status with optimization advice
```

## Information Displayed

### Current Usage

- Total tokens used and available
- Usage percentage
- Current threshold level (healthy/warning/critical)
- Historical usage trend (if available)

### Context Breakdown

- Conversation messages
- File contents read
- Tool outputs
- Agent completion reports
- Coordination state files

### Optimization Recommendations

Based on current usage, provides specific recommendations:

#### At 40-60% (Healthy)

- Continue normal operation
- No optimization needed
- Consider checkpointing for long-running tasks

#### At 60-65% (Warning)

- Archive old completion reports
- Summarize long conversation threads
- Move analysis files to `.coordination/`
- Consider creating checkpoint before next major task

#### At 65-75% (Urgent)

- **Immediate**: Create checkpoint now
- Archive all completed agent outputs
- Summarize conversation history
- Defer non-critical file reads
- Complete current task before starting new work

#### At 75%+ (Critical)

- **Stop**: Complete current task immediately
- **Required**: Create checkpoint
- **Required**: Trigger context compaction
- Restore from checkpoint after compaction
- Do not start new multi-agent workflows

## Sample Output

```
Context Usage Analysis
======================

Current Usage:
  Tokens:         90,000 / 200,000 (45%)
  Status:         🟢 Healthy
  Trend:          ↑ Increasing (15k in last 10 messages)

Context Breakdown:
  Conversation:   25,000 tokens (28%)
  File Contents:  35,000 tokens (39%)
  Tool Outputs:   20,000 tokens (22%)
  Agent Reports:  10,000 tokens (11%)

Optimization Recommendations:
  ✓ Operating normally - no action required
  • Consider checkpoint if planning large multi-agent workflow
  • Next warning threshold at 120,000 tokens (60%)

Context Efficiency:
  Signal-to-Noise: High
  Large Files Read: 2 files >5000 tokens
  Suggestions:
    - Consider using offset/limit when reading large files
    - Archive old agent outputs (5 reports >7 days old)
```

## Context Management Thresholds

From `.claude/orchestration-config.yaml`:

- **<60%**: Healthy - Normal operation
- **60%**: Warning - Start optimizing
- **65%**: Checkpoint - Create checkpoint now
- **75%**: Critical - Complete task, then compact
- **85%**: Emergency - Automatic compaction triggered

## Optimization Strategies

### Immediate Actions (any threshold)

```bash
# Archive old completion reports
.claude/hooks/cleanup_stale_files.py

# Clean coordination files
.claude/hooks/session_cleanup.sh

# Create checkpoint
.claude/hooks/checkpoint_state.sh create task-name "Description"
```

### File Reading Optimization

```python
# Instead of reading entire large file
Read(file_path="/large/file.py")

# Use offset/limit for large files
Read(file_path="/large/file.py", offset=100, limit=50)
```

### Agent Coordination

- Limit to 2 concurrent agents (enforced by `enforce_agent_limit.py`)
- Use batching for multi-agent workflows
- Create checkpoints between batches
- Archive completion reports after synthesis

## See Also

- `/status` - System health and agent status
- `/cleanup` - Run maintenance tasks
- `.claude/hooks/check_context_usage.sh` - Context monitoring
- `.claude/orchestration-config.yaml` - Threshold configuration
- `.claude/hooks/checkpoint_state.sh` - Checkpoint management
