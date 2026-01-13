from expect.targets.rule_helpers import (
    ensure_dir,
    ensure_exists,
    ensure_file,
    ensure_json,
)


def chainable(*prereqs):
    """
    Apply prerequisite rules to a rule function.

    Each prereq must be a callable(target) -> (ok, msg).
    The wrapped rule will:
      - run prereqs first (via target.run_rule)
      - short-circuit on failure
      - rely on per-target caching to avoid re-execution
    """

    def wrap(rule):
        def wrapped(target):
            for prereq in prereqs:
                ok, msg = target.run_rule(prereq)
                if not ok:
                    return False, msg
            return target.run_rule(rule)

        wrapped.__name__ = rule.__name__
        return wrapped

    return wrap


def file_exists(target):
    ok, msg = ensure_exists(target)
    if not ok:
        return False, msg
    return ensure_file(target)


file_exists.__name__ = "file_exists"


def file_size_gt(min_bytes: int):
    def rule(target):
        size = target.path.stat().st_size
        if size <= min_bytes:
            return False, f"File size {size} <= {min_bytes}"
        return True, None

    rule.__name__ = f"file_size_gt({min_bytes})"
    return chainable(file_exists)(rule)


def is_json(target):
    return ensure_json(target)


is_json = chainable(file_exists)(is_json)
is_json.__name__ = "is_json"


def dir_exists(target):
    ok, msg = ensure_exists(target)
    if not ok:
        return False, msg
    return ensure_dir(target)


dir_exists.__name__ = "dir_exists"


def dir_contains(pattern: str):
    def rule(target):
        matches = list(target.path.glob(pattern))
        if not matches:
            return False, f"No files matching '{pattern}'"
        return True, None

    rule.__name__ = f"dir_contains({pattern})"
    return chainable(dir_exists)(rule)
