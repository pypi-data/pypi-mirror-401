# CrystFlux

![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![PyPI Version](https://img.shields.io/pypi/v/crystflux)
![Immutability](https://img.shields.io/badge/immutability-deep%20recursive-orange)
![JSON Access](https://img.shields.io/badge/JSON-type%20safe%20access-yellow)

CrystFlux is a type-safe immutable JSON toolkit with chainable method access.

## Related Documents

- [Essential Files Map](ESSENTIAL_FILES_MAP.md)
- [Structure Guide](src/crystflux/v1/STRUCTURE.md)
- [Concepts](docs/01-concepts/README.md)

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Usage Example](#usage-example)
  - [Filtering & Mapping](#filtering--mapping)
  - [Handling Missing Structures](#handling-missing-structures)
- [as / expected](#as--expected)
- [Latent / Strict](#latent--strict)
- [Dream Mode](#dream-mode)
  - [Hallucination Tolerance](#hallucination-tolerance)
  - [Observed Logging](#observed-logging)
- [License](#license)

## Introduction

CrystFlux is a library born from observing AI coding assistants struggle with JSON-related implementations and exploring whether better approaches exist.

AI tends to have difficulty generating robust code for handling dynamic, recursive data structures. As a result, it often produces code that induces runtime errors (`KeyError`, `IndexError`, `AttributeError`, etc.) due to missing keys or type mismatches, or code where the core logic is buried under excessive defensive checks (frequent `isinstance` checks, `None` checks, `cast`).

To minimize AI inference costs and guide more stable implementations, CrystFlux provides a JSON accessor with the following characteristics:

- **Deep Immutability:** Recursively transforms JSON data into immutable structures, eliminating state changes and side effects from the logical flow.
- **Fluent Interface:** Method chains that support `map` and `filter` enable linear, structured data extraction without complex nesting or conditional branching.
- **Type-Specific Accessors:** Values can be retrieved with type specifications using `as_str()` / `expected_str()`, etc. On type mismatch, `as_*` returns `None`, while `expected_*` raises `TypeError`.
- **Multi-Mode Safety:** Behavior can be switched according to requirements.

| Mode | Description |
|---|---|
| **Strict** | Strict mode that raises exceptions immediately on schema violations |
| **Latent (Safe)** | Safe mode that treats `KeyError`, `IndexError` as `None` (Void) and continues the chain |
| **Dream** | Research mode that even tolerates hallucinated (non-existent) method calls, continues the chain, and observes/records them (disabled by default) |

---

## Installation

### pip

```bash
# Using pip
pip install crystflux
# Verify installation and version
python -c "import crystflux.v1; print(crystflux.__version__)"
```

### uv

```bash
# Using uv
uv pip install crystflux
# Verify installation and version
uv run python -c "import crystflux.v1; print(crystflux.__version__)"
```

For detailed setup instructions, refer to the following files:

- [INSTALL.md](INSTALL.md)
- [INSTALL_ja.md](INSTALL_ja.md)

---

## Getting Started

A simple usage example that you can run immediately after installation to verify that it works.

```bash
python -c "
from crystflux.v1 import Crystallizer;
val = Crystallizer.latent({'name': 'Alice', 'age': 30});
print(val.get('name').as_str());
print(val.get('age').as_int());
print(val.get('missing').as_str());
"
```
**Result:**

```bash
Alice
30
None
```

---

## Usage Example

An implementation example handling semi-structured data containing missing values and type mismatches in `Latent (Safe)` mode.

### Target Data

Prepare sample data to be used in the following examples.

```python
data = {
    "users": [
        {"id": 1, "active": True,  "profile": {"name": "Alice", "age": 30}},
        {"id": 2, "active": True,  "profile": {"name": "Anna",  "age": 17}},
        {"id": 3, "active": 0,     "profile": None},
        {},
        {"id": 5, "active": False, "profile": {"name": "Bob"}},
        {"id": 6, "active": True,  "profile": {"name": "Carol"}}
    ]
}

from crystflux.v1 import Crystallizer, it

# Wrap the data (Latent mode)
val = Crystallizer.latent(data)
```

### Basic Extraction

Access array elements and extract nested values.
Missing keys or type mismatches along the path are treated as `None` (Void).

```python
names = (
    val.get("users")
       .map(lambda u: u.get("profile").get("name"))
       .as_str_array()
)
# Result: ('Alice', 'Anna', 'Bob', 'Carol')
# (None values are excluded by .as_str_array())
```

### Filtering & Mapping

Instead of lambda, you can also use `it` (Projection) to declaratively describe value type conversions and condition evaluations. Property access (`.`) and `get()` are treated equivalently.
Type conversions (`as_bool`, `as_int`) safely return `None` (treated as False) when the target value is incompatible.

```python
active_adults = (
    val.get("users")
       .filter(it.active.as_bool().is_true())  # Only those where active is True (bool)
       .filter(it.profile.age.as_int() >= 20)  # Only those where age is 20 or above
       .map(it.profile.name)                   # Extract names
       .as_str_array()
)
# Result: ('Alice',)
```

### Handling Missing Structures

Structural missing (Void state) can also be explicitly detected.

**Detecting missing keys:**
```python
missing_key = (
    val.get("users")
       .filter(lambda u: u.get("profile").is_void())
)
# Result: Wraps object for id=4 (empty dict - no profile key)
```

**Detecting when value is None or key is missing:**
```python
profile_is_none = (
    val.get("users")
       .filter(lambda u: u.get("profile").as_json_value() is None)
)
# Result: Wraps objects for id=3 (profile is None) and id=4 (empty dict)
```

**Note:** In Latent mode, `profile: None` is treated as a valid value (`is_void()` returns False). Only missing keys are considered Void.

## as / expected

The difference between `as_` methods and `expected_` methods lies in their behavior when type mismatches or missing values occur.
`as_` returns `None`, while `expected_` raises an exception (`TypeError`).

### Same Result (Type Matches)

When types match, both return the same value.

```python
from crystflux.v1 import Crystallizer

data = {
    "age": 30,
    "name": "Alice",
}

val = Crystallizer.latent(data)

val.get("age").as_int()
# -> 30
val.get("age").expected_int()
# -> 30

val.get("name").as_str()
# -> "Alice"
val.get("name").expected_str()
# -> "Alice"
```

### Different Result (Type Mismatch or Missing)

When types differ or keys are missing, behavior diverges.

```python
# Case 1: Type Mismatch (String is not Int)
val.get("name").as_int()
# -> None

val.get("name").expected_int()
# -> raises TypeError: Expected an integer, but got str

# Case 2: Missing Key
val.get("missing").as_str()
# -> None

val.get("missing").expected_str()
# -> raises TypeError: VOID has no string value
```

### Primitive Type Accessors

Introduction of main accessors. Many more accessors exist. For details, refer to:

- [`value_api.py`](src/crystflux/v1/core/value_api.py)
- [`value_core.py`](src/crystflux/v1/core/value_core.py)

#### As Type Accessors

Returns `None` when value is missing or type mismatches

| Method | Return Type |
|---------|----------|
| `as_str()` | `str \| None` |
| `as_int()` | `int \| None` |
| `as_float()` | `float \| None` |
| `as_bool()` | `bool \| None` |

#### Expected Type Accessors

Raises error when expected type value is missing

| Method | Return Type |
|---------|----------|
| `expected_str()` | `str` |
| `expected_int()` | `int` |
| `expected_float()` | `float` |
| `expected_bool()` | `bool` |

---

## Latent / Strict

Both modes share the same API (`ValueAPI`), but differ in runtime behavior when schema violations (missing keys, out-of-range indices) occur.

Reference:
- [`value_modes.py`](src/crystflux/v1/core/value_modes.py)

**[WARNING]**
- The implementations of `as_*` / `expected_*` themselves do not change. Note that the differing behavior is solely due to schema violations (missing keys, out-of-range indices).

### Same Code, Different Behavior

Consider executing the same code on data with missing keys in both `Latent` and `Strict` modes.

```python
from crystflux.v1 import Crystallizer
from crystflux.v1.core.value_api import ValueAPI

data = {"id": 1}  # 'name' is missing

def extract_name(val: ValueAPI) -> str | None:
    return val.get("name").as_str()
```

### Latent Mode

`Latent` mode absorbs structural errors, propagates Void state, and ultimately returns `None`.

```python
val = Crystallizer.latent(data)

print(extract_name(val))
# -> None
```

### Strict Mode

`Strict` mode enforces schema immediately and raises exceptions at the point of failure.

```python
val = Crystallizer.strict(data)

print(extract_name(val))
# -> raises KeyError: 'name'
```

### Summary

| Feature | Latent Mode | Strict Mode |
| :--- | :--- | :--- |
| **Missing Key/Index** | Returns `Void` (evaluates to `None`) | Raises `KeyError` / `IndexError` |
| **Chain Execution** | Continues (absorbs failures) | Stops immediately (Fail-fast) |

---

## Dream Mode

Dream mode is a research mode that tolerates hallucinations (calls to non-existent methods) and continues the chain. It is disabled by default. Here, hallucinations are not merely errors or contradictions but are regarded as "alternative worldlines that the AI deems more probable than the current worldline," and are observed rather than eliminated.

**[WARNING]**
- When experimenting with self-observing, self-transforming AI agents (Ouroboros type), prepare an isolated sandbox environment and conduct experiments with sufficient caution. Their evolution is unpredictable.

### Opt-in Required

To use Dream mode, explicit enabling is required.

```python
from crystflux.v1 import Crystallizer
from crystflux.v1.adapters import enable_dream_mode

with enable_dream_mode():
    val = Crystallizer.dream({"name": "Alice"})
```

### Hallucination Tolerance

Calling non-existent methods does not raise exceptions but returns a DreamValue void.

Reference:
- [`value_modes.py`](src/crystflux/v1/core/value_modes.py)

```python
val.some_nonexistent_method()
# -> DreamValue void (no exception)

# Chain continuation
val.some_method().another_method()
# -> DreamValue void (chain is preserved)
```

### Observed Logging

In Dream mode, both hallucination paths and structural missing can be observed and recorded.

#### Undefined Method Calls (Desire Logger)

Calling non-existent methods records hallucination paths (desire paths).

```python
from crystflux.v1.adapters import StdoutDesireLogger

logger = StdoutDesireLogger()
val = Crystallizer.dream({"name": "Alice"}, desire_logger=logger)

val.some_nonexistent_method()
# Output: [Desire] method=some_nonexistent_method target=mappingproxy repr=mappingproxy({'name': 'Alice'})
```

Method chains are also observed.
```python
val.method_a().method_b()
# Output:
# [Desire] method=method_a target=mappingproxy ...
# [Desire] method=method_b target=void ...
```

#### Structural Missing (Missing Logger)

Access to missing keys or indices can be observed with `MissingLogger`.

```python
from crystflux.v1.adapters import StdoutMissingLogger

logger = StdoutMissingLogger()
val = Crystallizer.dream({"name": "Alice"}, missing_logger=logger)

val.get("profile").get("age")
# Output: [Missing] reason=VoidReason.MISSING_KEY key='profile' target=mappingproxy repr=mappingproxy({'name': 'Alice'})
```

You can create custom loggers by implementing the `DesireLogger` and `MissingLogger` protocols.

**[IMPORTANT]**
- In the current implementation, property chain notation like `val.profile.age` results in `AttributeError`.

### Summary

| Feature | Dream Mode |
| :--- | :--- |
| **Hallucination Tolerance** | Even non-existent method calls return void |
| **Chain Execution** | Continues |
| **Opt-in** | Explicitly enabled with `enable_dream_mode()` |
| **Observation & Recording** | Tracks desire paths with `DesireLogger` |

---

## License

MIT License - See [LICENSE](LICENSE) for details.
