# 🛡️ py-guardrails

A lightweight, framework-agnostic Python utility library for **explicit validation and permission checks** in backend systems.

`py-guardrails` provides small, reusable helpers that act as **guardrails** around critical backend logic — helping developers fail fast, write clearer code, and avoid scattered authorization and validation logic.

---

## ✨ Why py-guardrails?

While building backend systems, it’s common to see:

* validation logic duplicated across services
* permission checks scattered and inconsistent
* silent failures that cause subtle bugs
* heavy framework dependencies for simple needs

Most existing solutions are either:

* tightly coupled to a specific framework, or
* overly complex for small to mid-sized systems.

**py-guardrails** fills the gap with a deliberately small, explicit utility layer that focuses on **intent**, not magic.

---

## 🎯 Design Goals

* **Explicit over implicit** — nothing happens automatically
* **Framework-agnostic** — works in APIs, CLIs, scripts, and background jobs
* **Small, focused abstractions** — easy to read, review, and test
* **Fail fast and clearly** — no silent failures
* **Open-source friendly** — predictable structure and behavior

This library prioritizes **clarity and correctness** over feature count.

---

## 📦 What This Library Provides

### ✅ Included

* Input validation helpers
* Permission enforcement helpers
* Clear, explicit custom exceptions

### ❌ Not Included (by design)

* Authentication
* Database access
* Framework integrations
* Decorators or magic hooks
* Policy engines or configuration DSLs

---

## 🧠 High-Level Architecture

```
guardrails/
├── validators.py   # Input validation helpers
├── permissions.py  # Permission enforcement utilities
├── exceptions.py   # Custom exception types
└── __init__.py     # Public API
```

Each module has a **single responsibility**, and all public behavior is exposed intentionally through the public API.

---

## 🚀 Installation

```bash
pip install py-guardrails
```

*(Publishing to PyPI can be added when needed — the project is packaging-ready.)*

---

## 🔧 Usage Examples

### Validation

```python
from guardrails import require_non_empty, require_positive

require_non_empty(username, "username")
require_positive(age, "age")
```

Raises `ValidationError` if validation fails.

---

### Permissions

```python
from guardrails import check_permission

rules = {
    "approve": {"admin", "manager"}
}

check_permission("admin", "approve", rules)
```

Raises `PermissionError` if the role is not allowed.

---

### Error Handling

```python
from guardrails import PermissionError

try:
    check_permission("user", "approve", rules)
except PermissionError as exc:
    handle_error(exc)
```

All failures are **explicit and intentional**.

---

## 🧪 Testing Philosophy

* Tests validate **behavior**, not implementation
* Both success and failure paths are tested
* No framework or mocking dependencies
* Uses `pytest` for clarity and simplicity

Run tests locally:

```bash
pip install -e .[dev]
pytest
```

---

## 🔍 How This Differs From Existing Tools

Unlike framework-bound validators or full RBAC engines:

* `py-guardrails` is **framework-agnostic by design**
* focuses on **intent-level checks**, not schemas or policies
* avoids complex configuration or hidden behavior
* is intentionally small and boring (by design)

It is meant to be **embedded**, not imposed.

---

## 🧩 When Should You Use This?

Use `py-guardrails` when:

* you want explicit validation and permission checks
* you are building backend services or internal tools
* you value readability and correctness
* you don’t want framework lock-in

Do **not** use it if you need:

* full authentication systems
* policy-based access control engines
* schema-heavy data validation

---

## 🛠️ Contributing

Contributions are welcome.

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Contribution Philosophy

* Small, focused changes
* Clear commit messages
* Explicit behavior
* Readability over cleverness

---

## 📜 License

MIT License © 2026 Tamal Majumdar

---

## 🧠 Final Note

`py-guardrails` is intentionally minimal.

Its value lies not in what it does, but in what it **prevents**:

* unclear intent
* scattered logic
* silent failures

If it makes your backend code easier to reason about, it’s doing its job.

---
