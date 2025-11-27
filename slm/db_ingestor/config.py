from yaml import safe_load
from os import listdir

with open("db_ingestor/config.yml") as yml:
    cfg = safe_load(yml)

cfg["documents"] = listdir(cfg["txt-docs-dir"])
assert cfg, "Missing config.yml"
