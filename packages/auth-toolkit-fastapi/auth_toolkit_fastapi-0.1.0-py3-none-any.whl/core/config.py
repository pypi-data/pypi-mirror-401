from .defaults import AuthDefaults

def merge_defaults(defaults: AuthDefaults, overrides: dict) -> AuthDefaults:
    data = defaults.__dict__.copy()

    for key, value in overrides.items():
        if value is not None:
            data[key] = value

    return AuthDefaults(**data)
