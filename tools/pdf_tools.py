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
