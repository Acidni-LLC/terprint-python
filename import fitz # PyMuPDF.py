import fitz # PyMuPDF
import requests


batch = "81283_0007516400"

url ="https://www.trulieve.com/content/dam/trulieve/en/lab-reports/"+batch+".pdf?download=true"  # Replace with the actual URL of the file
local_filename = batch+".pdf"  # Replace with your desired local filename

try:
    response = requests.get(url, stream=True)  # Use stream=True for large files
    response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

    with open(local_filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"File '{local_filename}' downloaded successfully.")

except requests.exceptions.RequestException as e:
    print(f"Error downloading file: {e}")


#https://www.trulieve.com/content/dam/trulieve/en/lab-reports/84573_0007311573.pdf?download=true
pdf_path = "C:\\JamiesonGill\\source\\repos\\Terprint\\test_output\\"+batch+".pdf"
pdf_path = local_filename
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
splittext  =splittext.split("Detailed Terpenes Analysis is on the following page", maxsplit=1)[0]
print(splittext)
#print(extracted_text)
splittext1 = extracted_text.split("This product is tested at this moisture level, not at dry weight.", maxsplit=1)[1]
splittext1 = splittext1.split("Terpenes Summary", maxsplit=1)[0]
print(splittext1)

with open(batch+".txt", "w", encoding='utf-8') as f:
    f.write(splittext + "\n----------------------" + splittext1)
