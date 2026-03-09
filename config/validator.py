def validate_config_structure(cfg: dict):
    if not isinstance(cfg, dict):
        raise ValueError("config must be a dict")
    if "distribution" not in cfg:
        raise ValueError("missing distribution section")
    if "objective" not in cfg:
        raise ValueError("missing objective section")
