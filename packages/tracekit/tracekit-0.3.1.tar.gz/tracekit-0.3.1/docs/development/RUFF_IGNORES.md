# Ruff Linting Rule Ignores - Rationale Documentation

This document provides detailed rationale for all Ruff linting rules that are ignored in the TraceKit codebase.

**Last Updated:** 2026-01-11
**Review Schedule:** Quarterly

## Table of Contents

- [Global Ignores](#global-ignores)
- [Per-File Ignores](#per-file-ignores)
- [Review Process](#review-process)

---

## Global Ignores

These rules are ignored project-wide. Each ignore is documented with rationale and examples.

### Style & Formatting

#### `E501` - Line too long

**Reason:** Handled by the Ruff formatter automatically. Manual enforcement is redundant.
**Status:** ✅ Appropriate

#### `RUF005` - collection-literal-concatenation

**Example:** `[1, 2] + [3, 4]` vs `[1, 2, 3, 4]`
**Reason:** Concatenation is sometimes clearer when combining dynamic lists.
**Status:** ✅ Appropriate for scientific code

---

### Intentional Code Patterns

#### `PLC0415` - import-outside-top-level

**Reason:** Used for lazy imports of optional dependencies (matplotlib, pandas, pptx).
Prevents ImportError for users who don't have all optional packages installed.
**Example:** `src/tracekit/visualization/waveforms.py` imports matplotlib only when plotting.
**Status:** ✅ Required for optional dependencies

#### `SIM102` - collapsible-if

**Example:** Prefers `if a and b:` over `if a: if b:`
**Reason:** Explicit nesting improves readability in complex validation logic.
**Status:** ⚠️ Review - May be overly permissive. Consider enabling with selective ignores.

#### `SIM105` - suppressible-exception

**Example:** Prefers `contextlib.suppress(ValueError)` over `try/except`
**Reason:** Try/except is more familiar and debuggable in complex error handling.
**Status:** ✅ Appropriate

#### `SIM108` - if-else-block-instead-of-if-exp

**Example:** Prefers `x = a if cond else b` over `if cond: x = a else: x = b`
**Reason:** Multi-line if/else blocks are clearer for complex assignments.
**Status:** ✅ Appropriate

#### `SIM116` - if-else-block-instead-of-dict-lookup

**Example:** Prefers `LOOKUP[key]` over `if key == 'a': ... elif key == 'b': ...`
**Reason:** Dict lookup not always clearer for dispatch logic with side effects.
**Status:** ✅ Appropriate

#### `SIM117` - multiple-with-statements

**Example:** Prefers `with a, b:` over `with a: with b:`
**Reason:** Separate statements can be clearer when context managers have different scopes.
**Status:** ✅ Appropriate

---

### Performance Rules

#### `PERF401` - manual-list-comprehension

**Reason:** Conditional appends in loops are often clearer than filtered comprehensions.
**Status:** ⚠️ Review - List comprehensions are generally more efficient. Consider case-by-case review.

#### `PERF402` - manual-list-copy

**Reason:** Explicit `list()` call for copying is clear and intentional.
**Status:** ✅ Appropriate

#### `PERF403` - manual-dict-comprehension

**Reason:** Explicit dict building can be clearer for complex transformations.
**Status:** ✅ Appropriate

---

### API Compatibility

#### `ARG001` - unused-function-argument

**Reason:** API compatibility requires maintaining function signatures even if not all args are used.
**Example:** Callback functions, abstract methods, future compatibility.
**Status:** ⚠️ Review - Each instance should be documented with `# noqa: ARG001 - reason`

#### `ARG002` - unused-method-argument

**Reason:** Same as ARG001, but for methods.
**Status:** ⚠️ Review - Same concern as ARG001

---

### Type Checking

#### `TC002` - typing-only-third-party-import

**Reason:** Low priority refactoring for TYPE_CHECKING blocks.
**Status:** ⚠️ Review - Consider enabling to improve import organization

#### `TC003` - typing-only-standard-library-import

**Reason:** Low priority refactoring for TYPE_CHECKING blocks.
**Status:** ⚠️ Review - Consider enabling to improve import organization

#### `TC004` - runtime-import-in-type-checking-block

**Reason:** Can be tricky to refactor without breaking runtime behavior.
**Status:** ⚠️ Review - Address when refactoring modules

#### `TC010` - runtime-string-union

**Reason:** Low priority typing improvement for string unions.
**Status:** ✅ Appropriate for now

#### `UP007` - non-pep604-annotation-union

**Example:** Prefers `int | str` over `Union[int, str]`
**Reason:** May need Union for compatibility with older type checkers.
**Status:** ⚠️ Review - PEP 604 syntax is supported in Python 3.10+, TraceKit requires 3.12+

---

### Pathlib vs os.path

#### `PTH110` - os-path-exists

**Reason:** `os.path.exists()` is acceptable and familiar.
**Status:** ⚠️ Review - Consider migrating to `Path.exists()` for consistency

#### `PTH123` - builtin-open

**Reason:** Standard `open()` is fine for simple file operations.
**Status:** ✅ Appropriate (Path.open() adds no value for simple operations)

---

### Pylint Rules

#### `PLW0603` - global-statement

**Reason:** Sometimes necessary for module-level state (caches, singletons).
**Status:** ⚠️ Review - Each use should be justified

#### `PLW2901` - redefined-loop-name

**Reason:** Often intentional in nested loops or sequential transformations.
**Status:** ✅ Appropriate

#### `PLW3301` - nested-min-max

**Example:** `max(a, max(b, c))` vs `max(a, b, c)`
**Reason:** Readability preference for grouped comparisons.
**Status:** ⚠️ Review - Flattened form is generally clearer

---

### Ruff-Specific Rules

#### `RUF043` - implicit-optional

**Reason:** Regex patterns with metacharacters trigger false positives.
**Status:** ✅ Appropriate

#### `RUF046` - unnecessary-cast-to-int

**Reason:** Explicit casts often needed for mypy type narrowing.
**Status:** ✅ Appropriate

#### `RUF059` - unpacked-variable-never-used

**Reason:** Common in tests where not all return values are needed.
**Status:** ✅ Appropriate (covered by test-specific ignores)

---

## Per-File Ignores

### `**/__init__.py`

#### `E402` - Module level import not at top

**Reason:** Organized imports in `__init__.py` may reorder for logical grouping.
**Status:** ✅ Appropriate

---

### `tests/**/*.py`

Test files have relaxed rules for pragmatic reasons:

- **`ARG001-005`**: Test fixtures and mock methods may not use all parameters
- **`B007`**: Test loops may iterate without using values
- **`B017`**: Generic exceptions acceptable in test error handling
- **`E402`**: `matplotlib.use()` must be set before imports
- **`E721`**: Direct type comparison acceptable in exception testing
- **`E741`**: Short variable names like `l` acceptable in test scope
- **`F841`**: Subprocess results may be intentionally unused
- **`PLR2004`**: Magic values in test assertions are clear in context
- **`RUF001/003`**: Unicode symbols acceptable in test data
- **`RUF012`**: Test mocks don't need ClassVar annotations

**Status:** ✅ Appropriate - Tests prioritize clarity over strict linting

---

### Special Module Ignores

#### `src/tracekit/exploratory/*.py` - `RUF002`

**Reason:** Mathematical symbols (∑, ∫, etc.) in docstrings are intentional.
**Status:** ✅ Appropriate

#### `src/tracekit/integrations/llm.py` - `PLC0415`, `F401`

**Reason:** Dynamic imports for optional LLM dependencies.
**Status:** ✅ Appropriate

#### `src/tracekit/exporters/*.py` - `F401`

**Reason:** Imports used in generated code/templates.
**Status:** ✅ Appropriate

---

## Review Process

### Quarterly Review Checklist

1. **Review ⚠️ items** - Reassess if each ignore is still necessary
2. **Check for alternatives** - Can ignored patterns be refactored?
3. **Document new ignores** - Add rationale for any new ignores
4. **Update this document** - Keep rationale current

### Adding New Ignores

When adding a new ignore:

1. Document the reason in `pyproject.toml` with an inline comment
2. Add detailed rationale to this document
3. Mark as ⚠️ for review if uncertain
4. Consider if a `# noqa` comment on specific lines is better than a global ignore

### Metrics

- **Total global ignores:** 26
- **Ignores marked for review (⚠️):** 9
- **Appropriate ignores (✅):** 17
- **Target:** Review flagged items quarterly; aim to reduce total ignores over time

---

## Recommendations

### High Priority

1. **Enable `UP007`** - Migrate to PEP 604 union syntax (`int | str`)
2. **Review `ARG001/002`** - Document or refactor unused arguments
3. **Enable `TC002/003`** - Improve type checking import organization

### Medium Priority

1. **Review `SIM102`** - Consider enabling with selective per-line ignores
2. **Review `PERF401`** - Benchmark and consider list comprehensions
3. **Enable `PLW3301`** - Flatten nested min/max calls

### Low Priority

1. **Consider `PTH110`** - Migrate to `Path.exists()` for consistency
2. **Review `PLW0603`** - Document each use of global statement

---

## Security Note

This document was created as part of the P1 security improvements (2026-01-11).
Reviewing linting ignores is part of maintaining code quality and security posture.
