import fitz # PyMuPDF

pdf_path = "C:\\Users\\JamiesonGill\\Downloads\\64811_0007392408.pdf"
def extract_text_from_pdf(pdf_path):
    """Extracts all text from a PDF file."""
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        print(f"Error extracting text: {e}")
    return text

# Example usage
# pdf_file = "sample.pdf"
extracted_text = extract_text_from_pdf(pdf_path)
splittext = extracted_text.split("Terpenes Summary", maxsplit=1)[1]
print(splittext.split("Detailed Terpenes Analysis is on the following page", maxsplit=1)[0])
#print(extracted_text)
splittext1 = extracted_text.split("This product is tested at this moisture level, not at dry weight.", maxsplit=1)[1]
splittext1 = splittext1.split("Terpenes Summary", maxsplit=1)[0]
print(splittext1)
