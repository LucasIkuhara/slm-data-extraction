from requests import get
from io import BytesIO, IOBase
from pathlib import Path
from docling.document_converter import DocumentConverter


def url_to_md(url: str, out_dir: str) -> BytesIO:
    """
    Downloads a file using a GET request, converts it to markdown and saves it to files.

    Parameters:
     - url: The base file url
     - out_dir: The output dir path.

    Raises:
     - In case the request fails.
    """

    print(f"Writing pages to {out_dir} from buffer...")
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    converter = DocumentConverter()
    result = converter.convert(url)

    page_tag = "<br>"
    raw_md = result.document.export_to_markdown(page_break_placeholder=page_tag)
    pages = raw_md.split(page_tag)

    for idx, page in enumerate(pages, 1):

        print(
            f"Writing page: {idx} ({100 * (idx + 1)/ len(pages):.2f}%)",
        )
        with open(f"{out_dir}/{idx}.txt", "w") as fd:
            fd.write(page)

    print(f"{out_dir}/ created successfully")
