from smolagents import CodeAgent, LiteLLMModel
from tools.arxiv_tools import ArxivSearchTool, DownloadPaperTool
from tools.pdf_tools import PDFExtractorTool
from tools.summarization_tools import SummarizationTool
import config


class ResearchOrchestrator:
    
    def __init__(self):
        self.model = LiteLLMModel(
            model_id=config.AGENT_LLM,
            api_key=config.GROQ_API_KEY
        )
        
        self.tools = [
            ArxivSearchTool(),
            DownloadPaperTool(),
            PDFExtractorTool(),
            SummarizationTool()
        ]
        
        self.agent = CodeAgent(
            tools=self.tools,
            model=self.model,
            max_steps=config.MAX_AGENT_STEPS,
            additional_authorized_imports=["json", "ast"]
        )
    
    def research(self, query: str, num_papers: int = 3) -> dict:
        prompt = f"""
        Conduct a comprehensive research on the topic: "{query}"
        
        Workflow:
        1. Use arxiv_search to find the {num_papers} most relevant papers
        2. For each paper:
        - Extract key information from the abstract
        - Download the PDF using download_paper
        - Extract text using extract_pdf_text
        - Create a summary using summarize_text
        3. Prepare a final report containing:
        - Overview of found papers (include title as clickable link using URL, authors, and publication date for each paper)
        - Key findings from each paper
        - Common themes and trends
        
        Return the report as a FORMATTED MARKDOWN STRING, not a dictionary.
        Use headers (##), bullet points, and clear sections for readability.
        For the overview section, format each paper as:
        ### Paper N: [Title](URL)
        **Authors:** Author1, Author2, ...
        **Published:** YYYY-MM-DD
        """
        
        result = self.agent.run(prompt)
        return {
            "query": query,
            "result": result
        }

