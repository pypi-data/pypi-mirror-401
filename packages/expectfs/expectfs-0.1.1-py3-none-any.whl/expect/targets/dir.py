from pathlib import Path

from expect.targets.rules import dir_contains, dir_exists


class DirTarget:
    def __init__(self, path: str, context):
        self.path = Path(path)
        self._context = context
        self._cache = {}

    def run_rule(self, rule, *args, **kwargs):
        key = rule
        if key in self._cache:
            return self._cache[key]
        if callable(rule):
            result = rule(self, *args, **kwargs)
        else:
            raise TypeError("Rule must be callable")
        self._cache[key] = result
        return result

    def exists(self):
        self._context.register(self, dir_exists)
        return self

    def contains(self, pattern: str):
        self._context.register(self, dir_contains(pattern))
        return self

    def satisfies(self, rule):
        self._context.register(self, rule)
        return self

    def __str__(self):
        return str(self.path)
