from requests import get
from io import BytesIO


def url_to_buffer(url: str) -> BytesIO:
    """
    Downloads a file using a GET request and saves it to a buffer, akin to a locally
    loaded file.

    Parameters:
     - url: The base file url

    Returns:
     A BytesIO buffer created from the response.
    """

    try:
        response = get(url)
    except Exception as e:
        print(f"Failed to download file from {url}: ", e)

    buffer = BytesIO(response._content)
    buffer.seek(0)
    return buffer
