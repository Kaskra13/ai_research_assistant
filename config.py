import os
from dotenv import load_dotenv


load_dotenv()


HF_TOKEN = os.getenv("HF_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


SUMMARIZATION_MODEL = "facebook/bart-large-cnn"
QA_MODEL = "deepset/roberta-base-squad2"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
AGENT_LLM = "groq/llama-3.3-70b-versatile"


MAX_PAPERS = 5
MAX_SUMMARY_LENGTH = 250
MIN_SUMMARY_LENGTH = 50
CHUNK_SIZE = 1024
MAX_AGENT_STEPS = 10
