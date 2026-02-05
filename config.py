import os
from dotenv import load_dotenv


load_dotenv()


HF_TOKEN = os.getenv("HF_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


SUMMARIZATION_MODEL = "facebook/bart-large-cnn"
AGENT_LLM = "groq/llama-3.3-70b-versatile"


# Summarization limits (BART-large-CNN constraints)
MAX_SUMMARY_LENGTH = 250 # Max output length per chunk
MIN_SUMMARY_LENGTH = 50 # Min output length per chunk
CHUNK_SIZE = 1024 # Match BART's about 1024 token input limit
# API rate limit considerations (Groq: 12K TPM, 30 RPM)
MAX_AGENT_STEPS = 10 # Prevent excessive API calls in agent loop

