# expectfs

Declarative validation for things that are **not data models**.

`expectfs` lets you define clear, readable expectations about files, directories,
and system state — without schemas, test frameworks, or boilerplate.

This is for validating *the world*, not validating Python objects.

---

## Installation

```bash
pip install expectfs
```

---

## Quick Example

```python
from expect import expect, validate

expect.file("metrics.json") \
    .is_json() \
    .size_gt(100)

result = validate()

result.print()
```

If any expectation fails, a clear, actionable error message will be displayed after running validation.

---

## Why expect?

Most validation tools focus on:

* JSON schemas
* Data models
* API payloads
* Function inputs

But engineers constantly need to validate things like:

* “Does this file exist?”
* “Is this directory populated?”
* “Is this JSON valid?”
* “Did my pipeline actually produce output?”

`expect` exists for that gap.

---

## Key Features

* Declarative, chainable expectations
* Automatic dependency resolution (rules run in the correct order)
* Rule caching (each rule runs at most once)
* Clear failure messages

---

## How it Works (Conceptually)

```python
expect.file("output.json").is_json().size_gt(1024)
```

* `is_json` automatically ensures the file exists
* `size_gt` reuses prior results instead of re-running checks
* Dependencies are resolved recursively

Users don’t need to think about ordering.

---

## Supported Targets

Currently supported:

* Files
* Directories

Planned:

* Globs
* Environment variables
* Command outputs

---

## Status

This project is in **alpha**.

* APIs may evolve
* Backwards compatibility is not yet guaranteed
* Feedback and contributions are welcome

---

## License

MIT
