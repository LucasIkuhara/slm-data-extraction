# %%
from utils import url_to_buffer, pdf_buffer_to_txt_file

# Get file names and urls
with open("pdf_urls.txt", "r") as fd:
    file_urls = [x for x in fd.readlines() if len(x) > 0]
    names_and_urls = list(
        map(lambda x: (x.split("/")[-1][:-5], x.replace("\n", "")), file_urls)
    )

# %%
OUTPUT_DIR = "../plain-pages"

for name, url in names_and_urls:
    pdf_buffer = url_to_buffer(url)
    pdf_buffer_to_txt_file(pdf_buffer, f"{OUTPUT_DIR}/{name}")

# %%
