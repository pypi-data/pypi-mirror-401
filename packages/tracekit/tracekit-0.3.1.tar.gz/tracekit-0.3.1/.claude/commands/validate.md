---
name: validate
description: Run validation against acceptance criteria and requirements
arguments: <task-id|phase|all>
---

# Validate Command

Execute validation tests against specifications, acceptance criteria, and requirements.

## Usage

```bash
/validate <task-id>    # Validate specific task
/validate <phase>      # Validate entire phase
/validate all          # Validate all completed tasks
```

## Examples

```bash
/validate TASK-001     # Validate single task
/validate phase-auth   # Validate authentication phase
/validate all          # Full validation suite
```

## What Gets Validated

### Task Implementation

- Code matches specification requirements
- All acceptance criteria passing
- Tests cover specified behavior
- Edge cases handled correctly
- Error handling implemented

### Code Quality

- Follows coding standards (`.claude/coding-standards.yaml`)
- Type hints present and correct
- Documentation complete
- No linting errors
- Security best practices followed

### Test Coverage

- Unit tests for all functions
- Integration tests for workflows
- Edge case coverage
- Error condition testing
- Test assertions meaningful

### Specification Compliance

- All requirements from `spec/requirements.yaml` met
- Task graph dependencies satisfied
- Acceptance criteria all passing
- No incomplete FUTURE markers in scope

## Validation Process

1. **Load Specification**: Read from `.coordination/spec/`
2. **Discover Tests**: Find tests for target task/phase
3. **Run Test Suite**: Execute pytest with coverage
4. **Check Standards**: Validate against coding standards
5. **Verify Acceptance**: Check all criteria passing
6. **Generate Report**: Write validation manifest

## Sample Output

```
Validation Report: TASK-001
===========================

Specification:
  Task ID:       TASK-001
  Title:         Implement user authentication
  Requirements:  8 specified
  Acceptance:    5 criteria

Test Results:
  Tests Run:     23
  Passed:        23
  Failed:        0
  Skipped:       0
  Coverage:      94%

Acceptance Criteria:
  ✓ Users can register with email/password
  ✓ Passwords hashed with bcrypt
  ✓ JWT tokens issued on login
  ✓ Protected routes require valid token
  ✓ Invalid credentials return 401

Code Quality:
  ✓ Follows coding standards
  ✓ Type hints complete
  ✓ Documentation present
  ✓ No linting errors
  ✓ Security review passed

Requirements Coverage:
  ✓ REQ-001: User registration
  ✓ REQ-002: Password hashing
  ✓ REQ-003: JWT authentication
  ✓ REQ-004: Route protection
  ✓ REQ-005: Error handling
  ✓ REQ-006: Password validation
  ✓ REQ-007: Token refresh
  ✓ REQ-008: Logout functionality

Status: ✅ PASS

All requirements met, all tests passing, validation successful.
```

## Validation Manifest

Results written to `.coordination/spec/{project}/validation-manifest.yaml`:

```yaml
task_id: TASK-001
validation_date: 2025-01-09T13:00:00Z
status: pass
tests:
  total: 23
  passed: 23
  failed: 0
  coverage: 94
acceptance_criteria:
  - id: AC-001
    description: Users can register with email/password
    status: pass
  - id: AC-002
    description: Passwords hashed with bcrypt
    status: pass
requirements_coverage:
  - req_id: REQ-001
    status: satisfied
    evidence: tests/test_registration.py::test_user_registration
code_quality:
  coding_standards: pass
  type_hints: pass
  documentation: pass
  linting: pass
  security: pass
issues: []
```

## Validation Agents

This command routes to `spec_validator` agent:

- **Agent**: spec_validator
- **Model**: sonnet
- **Tools**: Read, Write, Edit, Bash, Grep, Glob
- **Output**: `.claude/agent-outputs/[task-id]-validation-complete.json`

## Validation Levels

### Quick Validation (default)

```bash
/validate TASK-001
```

- Runs tests for specific task
- Checks acceptance criteria
- Basic quality checks
- Fast feedback (~1-2 minutes)

### Comprehensive Validation

```bash
/validate TASK-001 --comprehensive
```

- Full test suite with coverage
- Security scanning
- Performance testing
- Documentation review
- Thorough quality audit (~5-10 minutes)

### Phase Validation

```bash
/validate phase-auth
```

- Validates all tasks in phase
- Integration tests across tasks
- Phase-level acceptance criteria
- Dependency verification

## Integration with Spec Workflow

Validation fits into spec workflow:

```bash
/spec extract requirements.md      # Create specification
/implement TASK-001                # Implement task
/validate TASK-001                 # Validate implementation
/spec decompose                    # Continue to next task
```

## Continuous Validation

### Pre-commit Validation

Automatic validation runs on commit:

- `.claude/hooks/auto_validate.py` (PostToolUse)
- Validates changed files
- Blocks commit if validation fails

### CI/CD Integration

```yaml
# .github/workflows/validate.yml
- name: Run validation
  run: |
    uv run pytest --cov
    # Validation checks run automatically
```

## Failure Handling

### When Validation Fails

1. **Review Report**: Check validation manifest for failures
2. **Fix Issues**: Address failing tests/criteria
3. **Re-validate**: Run validation again
4. **Iterate**: Repeat until passing

### Common Failure Reasons

- Missing test coverage for edge cases
- Acceptance criteria not fully implemented
- Type hints incomplete
- Linting errors
- Security vulnerabilities
- Documentation gaps

## See Also

- `/implement` - Task implementation from spec
- `/spec validate` - Validate specification structure
- `.claude/agents/spec_validator.md` - Validator agent documentation
- `.claude/PYTEST_GUIDE.md` - Testing guide
