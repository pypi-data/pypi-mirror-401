def validate_required_fields(data: dict, required: set, group_name: str = ""):
    for field in required:
        if not data.get(field):
            prefix = f"{group_name}." if group_name else ""
            raise ValueError(f"Missing required field '{prefix}{field}'")
