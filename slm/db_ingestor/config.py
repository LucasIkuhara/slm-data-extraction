from yaml import safe_load


with open("db_ingestor/config.yml") as yml:
    cfg = safe_load(yml)
assert cfg, "Missing config.yml"
