from expect.targets.rules import is_json


def test_is_json_passes(target_json):
    ok, msg = target_json.run_rule(is_json)
    assert ok


def test_is_json_fails(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text("{ not valid json ")

    from tests.conftest import FakeTarget

    t = FakeTarget(p)

    ok, msg = t.run_rule(is_json)
    assert not ok
