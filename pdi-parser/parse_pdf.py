# %%
import PyPDF2

# %%
pdf_filename = "raw-pdis/pdi_santos.pdf"

# %%
with open("raw-pdis/pdi_santos.pdf", "rb") as pdf_file:
    pdf = PyPDF2.PdfReader(pdf_file)
    total_pages = len(pdf.pages)

    with open("text-output/out.txt", "w") as fd:
        for idx, page in enumerate(pdf.pages):
            print(
                f"Writing page: {page.indirect_ref.idnum} ({100 * (idx + 1)/ total_pages:.2f}%)",
            )
            fd.write(page.extract_text())

    # number_of_pages = read_pdf.getNumPages()
    # page = read_pdf.pages[0]
    # page_content = page.extractText()
# print(page_content)

# %%
