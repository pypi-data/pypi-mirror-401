from expect.targets.rules import file_exists, file_size_gt


def test_rule_runs_only_once(target_file):
    calls = {"count": 0}

    def spy_rule(target):
        calls["count"] += 1
        return True, None

    spy_rule.__name__ = "spy_rule"

    # Run twice
    target_file.run_rule(spy_rule)
    target_file.run_rule(spy_rule)

    assert calls["count"] == 1


def test_dependency_runs_only_once(target_file):
    calls = {"exists": 0}

    def counted_exists(target):
        calls["exists"] += 1
        return file_exists(target)

    counted_exists.__name__ = "file_exists"

    rule = file_size_gt(1)

    # Explicit + implicit
    target_file.run_rule(counted_exists)
    target_file.run_rule(rule)

    assert calls["exists"] == 1
