from expect.targets.rules import dir_contains, dir_exists


def test_dir_exists_passes(target_dir):
    ok, msg = target_dir.run_rule(dir_exists)
    assert ok


def test_dir_contains_passes(tmp_dir):
    f = tmp_dir / "model.pt"
    f.write_text("x")

    from tests.conftest import FakeTarget

    t = FakeTarget(tmp_dir)

    rule = dir_contains("*.pt")
    ok, msg = t.run_rule(rule)
    assert ok


def test_dir_contains_fails(target_dir):
    rule = dir_contains("*.pt")
    ok, msg = target_dir.run_rule(rule)
    assert not ok
