import pdfplumber

# Open the PDF file
with pdfplumber.open(r"C:\Users\JamiesonGill\Downloads\64811_0007392408.pdf") as pdf:
    # Go through each page
    for page in pdf.pages:
        # Get tables from the current page
        tables = page.extract_table()

        # Print the table data
        print(tables)