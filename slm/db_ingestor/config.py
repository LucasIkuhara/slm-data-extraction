from yaml import safe_load
from os import listdir

with open("db_ingestor/config.yml") as yml:
    cfg: dict = safe_load(yml)
assert cfg, "Missing config.yml"

if not cfg.get("documents"):
    cfg["documents"] = listdir(cfg["txt-docs-dir"])
