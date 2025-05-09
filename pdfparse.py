import fitz
# from PIL import Image
# import pytesseract
# import io


def parse_pdf(file_bytes):
    '''Parse a PDF file and return the text as a string'''
    pdf = fitz.open(stream=file_bytes, filetype="pdf")

    text = ""

    for page in pdf:
        text += page.get_text()

    pdf.close()

    return text


# def parse_pdf(file_bytes):
#     '''Parse a PDF file and return the text as a string'''
#     pdf = fitz.open(stream=file_bytes, filetype="pdf")

#     text = ""

#     for page in pdf:
#         pix = page.get_pixmap(dpi=300)
#         img = Image.open(io.BytesIO(pix.tobytes("png")))
#         text += pytesseract.image_to_string(img)

#     pdf.close()

#     return text


def test(file_bytes):
    pdf = fitz.open(stream=file_bytes, filetype="pdf")
    for page_index, page in enumerate(pdf):
        blocks = page.get_text("dict")["blocks"]
        # for b in blocks:
        #     if "image" in b:
        #         # No standard alt text stored here — check annotations as fallback
        #         print(
        #             f"Image found on page {page_index + 1}, but alt text is not directly accessible.")

        # Check for annotations (where alt text may be stored in tagged PDFs)
        print(page.annots())
        for annot in page.annots() or []:
            print(annot)
            # if annot.type[0] == 8:  # "Stamp" or custom annotation
            #     print(
            #         f"Annotation on page {page_index + 1}: {annot.info.get('title', '')}")
            #     print(f"Alt text: {annot.info.get('content', '')}")


if __name__ == "__main__":
    with open("example.pdf", "rb") as f:
        file_bytes = f.read()
    # test(file_bytes)
    print(parse_pdf(file_bytes))
