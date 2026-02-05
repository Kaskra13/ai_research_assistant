import PyPDF2
from smolagents import Tool


class PDFExtractorTool(Tool):
    name = "extract_pdf_text"
    description = """
    Extracts text content from a PDF file.
    Args:
        pdf_path (str): Path to the PDF file
    Returns:
        str: Extracted text from the PDF
    """
    inputs = {
        "pdf_path": {"type": "string", "description": "Path to PDF file"}
    }
    output_type = "string"

    def forward(self, pdf_path: str) -> str:
        try:
            with open(pdf_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            return text[:10000]
        except Exception as e:
            return f"Error extracting PDF: {str(e)}"

# Limit to 10 000 characters due to downstream constraints:
# - BART model has about 1024 token input limit
# - Groq API has 12K tokens/min limit (llama-3.3-70b-versatile)
# - Full papers (50-100K chars) would exceed both limits
# Extracting first 10K chars typically covers: abstract, intro, methodology