# %%
from io import IOBase
from utils import url_to_buffer

# Get file names and urls
with open("pdf_urls.txt", "r") as fd:
    file_urls = [x for x in fd.readlines() if len(x) > 0]
    names_and_urls = list(map(lambda x: (x.split("/")[-1][:-4], x), file_urls))

# %%
for name, url in names_and_urls:
    pdf_buffer = url_to_buffer(url)

# %%
# Get PDFs from url as Buffer

# %%
import PyPDF2


# with open("raw-pdis/pdi_santos.pdf", "rb") as pdf_file:
def pdf_buffer_to_txt_file(buffer: IOBase, file_name: str):
    print(f"Writing to {file_name} from buffer...")
    pdf = PyPDF2.PdfReader(buffer)
    total_pages = len(pdf.pages)
    with open(file_name, "w") as fd:
        for idx, page in enumerate(pdf.pages):
            print(
                f"Writing page: {page.indirect_ref.idnum} ({100 * (idx + 1)/ total_pages:.2f}%)",
            )
            fd.write(page.extract_text())
    print(f"{file_name} created successfully")


# %%
