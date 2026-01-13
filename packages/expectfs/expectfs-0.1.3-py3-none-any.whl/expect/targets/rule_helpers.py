import json


def ensure_exists(target):
    if not target.path.exists():
        return False, "Path does not exist"
    return True, None


def ensure_file(target):
    if not target.path.is_file():
        return False, "Path exists but is not a file"
    return True, None


def ensure_dir(target):
    if not target.path.is_dir():
        return False, "Path exists but is not a directory"
    return True, None


def ensure_json(target):
    try:
        with open(target.path, "r") as f:
            json.load(f)
        return True, None
    except Exception as e:
        return False, f"Invalid JSON: {e}"
