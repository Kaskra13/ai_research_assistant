from transformers import pipeline
from smolagents import Tool
import config


class SummarizationTool(Tool):
    name = "summarize_text"
    description = """
    Creates a summary of long text using BART model.
    Args:
        text (str): Text to summarize
        max_length (int): Maximum length of summary
    Returns:
        str: Generated summary
    """
    inputs = {
        "text": {"type": "string", "description": "Text to summarize"},
        "max_length": {"type": "integer", "description": "Max length", "default": 250, "nullable": True}
    }
    output_type = "string"

    def __init__(self):
        super().__init__()
        self.summarizer = pipeline(
            "summarization",
            model=config.SUMMARIZATION_MODEL,
            device=-1
        )
    
    def forward(self, text: str, max_length: int = 250) -> str:
        try:
            chunks = [text[i:i+config.CHUNK_SIZE] 
                     for i in range(0, len(text), config.CHUNK_SIZE)]
            
            summaries = []
            for chunk in chunks[:5]:
            # Process max 5 chunks to stay within API rate limits:
            # - BART input: about 1024 tokens per chunk
            # - 5 chunks = about 5K tokens total input
            # - Groq TPM limit: 12K tokens/min
            # This ensures we don't hit rate limits when processing multiple papers
                if len(chunk.strip()) < 50:
                    continue
                summary = self.summarizer(
                    chunk,
                    max_length=max_length,
                    min_length=config.MIN_SUMMARY_LENGTH,
                    do_sample=False
                )[0]['summary_text']
                summaries.append(summary)
            
            return " ".join(summaries)
        except Exception as e:
            return f"Error summarizing: {str(e)}"
