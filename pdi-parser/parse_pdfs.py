# %%
from utils import url_to_md

# Get file names and urls
with open("pdf_urls.txt", "r") as fd:
    file_urls = [x for x in fd.readlines() if len(x) > 0]
    file_urls = [x for x in file_urls if "#" not in x]
    names_and_urls = list(
        map(lambda x: (x.split("/")[-1][:-5], x.replace("\n", "")), file_urls)
    )

# %%
OUTPUT_DIR = "../plain-pages"

for name, url in names_and_urls:
    pdf_buffer = url_to_md(url, f"{OUTPUT_DIR}/{name}")

# %%
