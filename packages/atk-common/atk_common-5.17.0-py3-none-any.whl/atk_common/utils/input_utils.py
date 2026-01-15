def require_field(obj: dict, key: str):
    if key not in obj or obj[key] is None:
        raise ValueError(f"Missing required field: {key}")
    return obj[key]