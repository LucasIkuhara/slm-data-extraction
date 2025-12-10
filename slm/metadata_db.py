from os import environ
from sqlalchemy import create_engine, text


meta_db = create_engine(
    environ["META_DB_CONN_STRING"],
)


def query_metadata(*args, **kwargs):
    with meta_db.connect() as meta:
        return meta.execute(text(args[0]), *args[1:], **kwargs)


if __name__ == "__main__":
    with meta_db.connect() as meta:
        print(meta.execute(text("SELECT * FROM DESCOM.METADATA LIMIT 5")))
