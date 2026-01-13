class ValidationContext:
    def __init__(self):
        self._checks = []

    def register(self, target, rule):
        self._checks.append((target, rule))

    @property
    def checks(self):
        return list(self._checks)


_DEFAULT_CONTEXT = ValidationContext()


def current_context():
    return _DEFAULT_CONTEXT
