import camelot

# Extract tables from the PDF
tables = camelot.read_pdf(r"C:\Users\JamiesonGill\Downloads\64811_0007392408.pdf")

# Print the number of tables extracted
print(f"Number of tables extracted: {len(tables)}")

# Print the first table2
print(tables[0].df)