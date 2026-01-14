# /doc - Documentation Creation

Force documentation creation workflow for guides, tutorials, and API docs.

## Purpose

Bypass intelligent routing and go directly to `technical_writer` agent for creating comprehensive, well-structured documentation.

## Usage

```bash
/doc <what>                                 # Create documentation
/doc create API documentation               # API docs
/doc write user guide for authentication    # User guides
/doc create tutorial for beginners          # Tutorials
/doc document the caching system            # Technical docs
```

## When to Use

✅ **Use /doc when**:

- Creating user-facing documentation
- Writing API documentation
- Developing tutorials or guides
- Documenting architecture or design
- Creating README sections
- Need well-structured, comprehensive docs

❌ **Don't use /doc when**:

- Just want code with docstrings → Use `/code` (includes docstrings)
- Need to research before documenting → Use `/research` first
- Want to implement and document → Use `/feature` (includes docs)
- Just want code comments → Use `/code` or `/ai`

## How It Works

```
/doc <what>
  ↓
Force route to technical_writer (bypass orchestrator)
  ↓
technical_writer analyzes codebase (if documenting existing code)
  ↓
Creates structured documentation
  ↓
Returns: Markdown documentation with examples
```

## Examples

### Example 1: API Documentation

```bash
/doc create API documentation for auth module
```

Returns:

````markdown
# Authentication API

## Overview

[Description of auth system]

## Endpoints

### POST /api/login

[Detailed endpoint documentation]

## Examples

```python
# Login example
response = requests.post('/api/login', json={
    'username': 'user',
    'password': 'pass'
})
```

## Error Codes

[Error documentation]
````

### Example 2: User Guide

```bash
/doc write beginner guide for using TraceKit
```

Returns complete tutorial with:

- Installation steps
- Basic usage examples
- Common workflows
- Troubleshooting

### Example 3: Architecture Documentation

```bash
/doc document the orchestration system architecture
```

Returns:

- System overview
- Component diagrams (text-based)
- Workflow descriptions
- Integration points

## Output Format

Documentation follows these patterns:

### For API Docs:

```markdown
# API Name

## Overview

Brief description

## Installation

Setup instructions

## Usage

Basic examples

## API Reference

Detailed method/endpoint documentation

## Examples

Real-world usage examples

## Error Handling

Error codes and resolution
```

### For Tutorials:

```markdown
# Tutorial: <Topic>

## Prerequisites

What you need to know

## Step 1: <First Step>

Detailed instructions with code

## Step 2: <Next Step>

More instructions

## Troubleshooting

Common issues

## Next Steps

Where to go from here
```

### For Architecture Docs:

```markdown
# <System> Architecture

## Overview

High-level description

## Components

Detailed component breakdown

## Data Flow

How data moves through system

## Integration Points

External dependencies

## Configuration

How to configure
```

## After Using /doc

What you can do next:

1. **Review documentation** - Read and provide feedback
2. **Add to project** - Save to docs/ directory
3. **Commit** - `/git "add user guide"`
4. **Create more docs** - `/doc [another topic]`
5. **Generate code from docs** - `/code implement [from documentation]`

## Documentation Style

technical_writer follows:

- **Clear and concise** - No jargon unless necessary
- **Examples-heavy** - Show, don't just tell
- **Well-structured** - Hierarchical organization
- **Accessible** - Suitable for target audience
- **Actionable** - Readers can follow steps
- **Current** - Reflects actual codebase state

## Integration with Workflow

Typical flows:

**Research → Document**:

```
/research GraphQL best practices
  ↓
/doc create GraphQL implementation guide
```

**Implement → Document**:

```
/feature implement authentication system
  ↓
/doc create authentication user guide
```

**Document → Implement**:

```
/doc create API specification for users endpoint
  ↓
/feature implement users endpoint from spec
```

## Documentation Types Supported

| Type             | Description                   | Example                          |
| ---------------- | ----------------------------- | -------------------------------- |
| **API Docs**     | Endpoint/method documentation | `/doc API for auth module`       |
| **User Guides**  | How-to documentation          | `/doc user guide for deployment` |
| **Tutorials**    | Step-by-step learning         | `/doc tutorial for beginners`    |
| **Architecture** | System design docs            | `/doc architecture overview`     |
| **README**       | Project overviews             | `/doc update README`             |
| **Contributing** | Contributor guides            | `/doc contributing guidelines`   |

## Code Analysis

When documenting existing code, technical_writer:

1. Reads relevant source files
2. Analyzes structure and patterns
3. Extracts key information
4. Creates accurate documentation
5. Includes real code examples from codebase

## Comparison with Other Commands

| Command     | Output            | Includes Code | Researches Web | Agent                |
| ----------- | ----------------- | ------------- | -------------- | -------------------- |
| `/doc`      | Documentation     | ✅ Examples   | ❌ No          | technical_writer     |
| `/research` | Research summary  | ⚠️ Examples   | ✅ Yes         | knowledge_researcher |
| `/code`     | Code + docstrings | ✅ Code       | ❌ No          | code_assistant       |
| `/feature`  | Code + docs       | ✅ Code       | ❌ No          | Multiple             |

## Configuration

Documentation behavior in `.claude/config.yaml`:

```yaml
agents:
  technical_writer:
    style: conversational # or "formal", "technical"
    code_examples: true # Include code examples
    diagram_style: text # or "mermaid", "ascii"
    target_audience: intermediate # or "beginner", "advanced"
```

## Output Location

Documentation is typically saved to:

- `/docs/` - Main documentation
- `/docs/api/` - API documentation
- `/docs/guides/` - User guides
- `/docs/tutorials/` - Tutorials
- `README.md` - Project overview
- `CONTRIBUTING.md` - Contributor docs

## Workflow

```
/doc → technical_writer (direct, no routing)
     → Analyze request
     → Read codebase (if documenting code)
     → Structure documentation
     → Write with examples
     → Return markdown
```

## Aliases

The following aliases work identically:

- `/document` → `/doc`
- `/write-docs` → `/doc`
- `/docs` → `/doc`

## Best Practices

### Good Documentation Requests:

```bash
/doc create REST API documentation for all endpoints
/doc write installation guide for Windows users
/doc document the retry decorator functionality
/doc create architecture overview with data flow
```

### Vague Requests (still work, but provide details):

```bash
/doc write docs           # For what? Specify topic
/doc create guide         # What kind of guide?
/doc document code        # Which code/module?
```

## Agent

Routes to: **technical_writer** (always, no routing logic)

## Version

v1.0.0 (2026-01-09) - Initial creation as part of workflow command system
