# %%
from utils import url_to_md
from os import listdir


# Get file names and urls
with open("pdf_urls.txt", "r") as fd:
    file_urls = [x for x in fd.readlines() if len(x) > 0]
    file_urls = [x for x in file_urls if "#" not in x]

names_and_urls = []
for url in file_urls:
    name = url.split("/")[-1][:-5]
    clean_url = url.replace("\n", "")
    names_and_urls.append((name, clean_url))

# %%
OUTPUT_DIR = "../plain-pages"
previously_extracted = listdir(OUTPUT_DIR)

for name, url in names_and_urls:
    if name in previously_extracted:
        print(f"Skipping {name}, already extracted previously.")
        continue
    url_to_md(url, f"{OUTPUT_DIR}/{name}")

# %%
