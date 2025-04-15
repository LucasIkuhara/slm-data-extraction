from requests import get
from io import BytesIO, IOBase
from pathlib import Path
import PyPDF2


def url_to_buffer(url: str) -> BytesIO:
    """
    Downloads a file using a GET request and saves it to a buffer, akin to a locally
    loaded file.

    Parameters:
     - url: The base file url

    Raises:
     - In case the request fails.

    Returns:
     A BytesIO buffer created from the response.
    """

    response = get(url)
    if response.status_code != 200:
        raise Exception(f"Request returned an error status code {response.status_code}")

    buffer = BytesIO(response._content)
    buffer.seek(0)
    return buffer


def pdf_buffer_to_txt_file(buffer: IOBase, out_dir: str):
    """
    Reads PDF buffer and extracts its text. The result is saved to a file.

    Parameters:
     - buffer: A binary buffer containing a PDF file.
     - out_dir: The output dir path.
    """
    print(f"Writing pages to {out_dir} from buffer...")
    pdf = PyPDF2.PdfReader(buffer)
    total_pages = len(pdf.pages)
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    for idx, page in enumerate(pdf.pages, 1):
        try:
            txt = page.extract_text()
            print(
                f"Writing page: {idx} ({100 * (idx + 1)/ total_pages:.2f}%)",
            )
            with open(f"{out_dir}/{idx}.txt", "w") as fd:
                fd.write(txt)
        except Exception:
            print(f"Failed to extract page {idx + 1}. Skipping page.")
    print(f"{out_dir}/ created successfully")
