import os
from typing import Tuple


BASE_PATH = os.environ.get("BASE_PATH")
if BASE_PATH is None:
    raise Exception(
        "Missing BASE_PATH. Please set this environment variable before trying again."
    )


def get_files() -> Tuple[str, int, str]:
    """
    Get all available raw text files.

    Returns:
        A tuple containing file_name, page number and raw text.
    """
    dirs = os.listdir(BASE_PATH)

    for txt_dir in dirs:
        files = os.listdir(f"{BASE_PATH}/{txt_dir}")
        read = []
        for txt_file in files:
            page = int(txt_file.split(".")[0])

            with open(f"{BASE_PATH}/{txt_dir}/{txt_file}", "r") as f:
                txt = f.read()
                read.append((txt_file, page, txt))
        return read
