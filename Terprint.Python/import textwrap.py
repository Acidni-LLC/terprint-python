import textwrap
import langextract as lx
import fitz # PyMuPDF

# 1. Define a concise prompt
prompt = textwrap.dedent("""\
Extract table data from potency and terpene summary.""")

# 2. Provide a high-quality example to guide the model
examples = [
    lx.data.ExampleData(
        text=(
        "Analyte Result (mg/g) (%)"
 "trans-Caryophyllene 11.693 1.169%"
 "(R)-(+)-Limonene 6.674 0.667%"
 "Linalool 5.149 0.515%"
 "beta-Myrcene 3.983 0.398%"
 "alpha-Humulene 3.116 0.312%"
 "trans-Nerolidol 1.524 0.152%"
 "alpha-Bisabolol 0.957 0.096%"
 "Fenchyl Alcohol 0.803 0.08%"
 "beta-Pinene 0.656 0.066%"
 "alpha-Pinene 0.475 0.048%"
        ),
        extractions=[
            lx.data.Extraction(
                extraction_class="trans-Caryophyllene",
                extraction_text="trans-Caryophyllene 11.693 1.169%" 
            ),
            lx.data.Extraction(
                extraction_class="(R)-(+)-Limonene",
                extraction_text="(R)-(+)-Limonene 6.674 0.667%"
            ),
            lx.data.Extraction(
                extraction_class="Linalool",
                extraction_text="Linalool 5.149 0.515%"
            ),
        ],
    )
]

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
print(extracted_text)
# 3. Run the extraction on your input text
input_text =extracted_text
input_document = (
    r"C:\Users\JamiesonGill\Downloads\64811_0007392408.pdf"
)
result = lx.extract(
    text_or_documents=input_text,
    prompt_description=prompt,
    examples=examples,
    model_id="gemini-2.5-pro",
    api_key="AIzaSyBbjvJnLLSanl5WpXWAXy0VqXe6ES4n74I" 
)

# Save the results to a JSONL file
lx.io.save_annotated_documents([result], output_name="extraction_results.jsonl")

# Generate the interactive visualization from the file
html_content = lx.visualize("extraction_results.jsonl")
with open("visualization.html", "w", encoding='utf-8') as f:
    f.write(html_content)
    