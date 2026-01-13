from expect.context import current_context
from expect.engine import run_validation
from expect.targets.dir import DirTarget
from expect.targets.file import FileTarget


class Expect:
    def file(self, path: str) -> FileTarget:
        return FileTarget(path, current_context())

    def dir(self, path: str) -> DirTarget:
        return DirTarget(path, current_context())


expect = Expect()


def validate():
    """
    Run validation on all registered expectations.
    """

    ctx = current_context()
    return run_validation(ctx)
