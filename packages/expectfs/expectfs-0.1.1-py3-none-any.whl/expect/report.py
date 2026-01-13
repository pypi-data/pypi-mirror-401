class ValidationError:
    def __init__(self, target, rule, message):
        self.target = target
        self.rule = rule
        self.message = message

    def __str__(self):
        return f"[{self.rule}] {self.target}: {self.message}"


class ValidationReport:
    def __init__(self):
        self.errors = []

    @property
    def ok(self):
        return len(self.errors) == 0

    def add_error(self, target, rule, message):
        self.errors.append(ValidationError(target, rule, message))

    def print(self):
        for err in self.errors:
            print(err)
