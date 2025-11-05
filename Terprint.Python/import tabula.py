import tabula

# Extract tables from the PDF
tables = tabula.read_pdf(r"C:\Users\JamiesonGill\Downloads\64811_0007392408.pdf", pages='all')

# Print the number of tables extracted
print(f"Number of tables extracted: {len(tables)}")

# Print the first table
print(tables[0])
print(tables[1])