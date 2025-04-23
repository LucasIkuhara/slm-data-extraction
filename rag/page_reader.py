import os
from typing import List, Optional, Tuple
from functools import cache


class PageReader:
    def __init__(self, base_path: str):
        self.base_path = base_path

    @cache
    def get_files(self, dir_filter: Optional[List[str]] = None) -> Tuple[str, int, str]:
        """
        Get all available raw text files.

        Returns:
            A tuple containing file name, page number and raw text.
        """
        dirs = os.listdir(self.base_path)
        if dir_filter:
            dirs = [x for x in dirs if x in dir_filter]

        for txt_dir in dirs:
            files = os.listdir(f"{self.base_path}/{txt_dir}")
            read = []
            for txt_file in files:
                page = int(txt_file.split(".")[0])

                with open(f"{self.base_path}/{txt_dir}/{txt_file}", "r") as f:
                    txt = f.read()
                    read.append((txt_dir, page, txt))
            return read

    def get_file(self, dir_name: str, page: int) -> str:
        all_pages = self.get_files(dir_name)
        for a, curr_page, text in all_pages:
            if page == curr_page:
                print(a, curr_page, text)
                return
