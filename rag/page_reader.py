from dataclasses import dataclass
import os
from typing import List, Optional, Tuple
from functools import cache


@dataclass
class DocumentPage:
    source_document: str
    page: int
    raw_text: str


class PageReader:
    def __init__(self, base_path: str):
        self.base_path = base_path

    @cache
    def get_files(self, doc_filter: Optional[List[str]] = None) -> List[DocumentPage]:
        """
        Get all available raw text files. Optionally can be filtered by documents.

        Args:
            doc_filter: A list of document names to use as base.

        Returns:
            A list of objects containing file name, page number and raw text.
        """

        # Get documents list
        dirs = os.listdir(self.base_path)
        if doc_filter:
            dirs = [x for x in dirs if x in doc_filter]

        for txt_dir in dirs:
            files = os.listdir(f"{self.base_path}/{txt_dir}")
            read = []
            for txt_file in files:
                page = int(txt_file.split(".")[0])

                with open(f"{self.base_path}/{txt_dir}/{txt_file}", "r") as f:
                    txt = f.read()
                    res = DocumentPage(txt_dir, page, txt)
                    read.append(res)
            return read

    def get_file(self, doc_name: str, page: int) -> DocumentPage:
        """
        Get a single page from a document.

        Args:
            doc_name: The base document.
            page: The page number.

        Returns:
            An object with the text content and metadata.
        """
        all_pages = self.get_files([doc_name])

        for a, curr_page, text in all_pages:
            if page == curr_page:
                print(a, curr_page, text)
                return
