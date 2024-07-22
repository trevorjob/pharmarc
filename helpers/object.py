from flask import abort


def validate_object(obj, strin: list):
    for st in strin:
        if st not in obj:
            abort(400, description=f"Missing {st}")


def check_keys(obj: dict, allowed_keys: list[str]) -> dict:
    kes = [key for key in obj.keys() if key not in allowed_keys]

    for ob in kes:
        del obj[ob]

    return obj
