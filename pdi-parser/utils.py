from requests import get
from io import BytesIO, IOBase
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


def pdf_buffer_to_txt_file(buffer: IOBase, file_path: str):
    """
    Reads PDF buffer and extracts its text. The result is saved to a file.

    Parameters:
     - buffer: A binary buffer containing a PDF file.
     - file_name: The output file path.
    """
    print(f"Writing to {file_path} from buffer...")
    pdf = PyPDF2.PdfReader(buffer)
    total_pages = len(pdf.pages)
    with open(file_path, "w") as fd:
        for idx, page in enumerate(pdf.pages):
            print(
                f"Writing page: {page.indirect_ref.idnum} ({100 * (idx + 1)/ total_pages:.2f}%)",
            )
            fd.write(page.extract_text())
    print(f"{file_path} created successfully")
