from expect.targets.rules import file_exists, file_size_gt


def test_file_exists_passes(target_file):
    ok, msg = target_file.run_rule(file_exists)
    assert ok
    assert msg is None


def test_file_exists_fails(tmp_path):
    from tests.conftest import FakeTarget

    t = FakeTarget(tmp_path / "missing.txt")

    ok, msg = t.run_rule(file_exists)
    assert not ok
    assert msg is not None


def test_file_size_gt_passes(target_file):
    rule = file_size_gt(5)
    ok, msg = target_file.run_rule(rule)
    assert ok


def test_file_size_gt_fails(target_file):
    rule = file_size_gt(1000)
    ok, msg = target_file.run_rule(rule)
    assert not ok
