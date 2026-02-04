import arxiv
from smolagents import Tool
from typing import List, Dict


class ArxivSearchTool(Tool):
    name = "arxiv_search"
    description = """
    Searches for scientific papers in the arXiv database.
    Args:
        query (str): Search query (e.g., 'machine learning transformers')
        max_results (int): Maximum number of results (default 5)
    Returns:
        List[Dict]: List of papers with title, authors, abstract, URL, and ID
    """
    inputs = {
        "query": {"type": "string", "description": "Search query"},
        "max_results": {"type": "integer", "description": "Number of results", "default": 5, "nullable": True}
    }
    output_type = "any"

    def forward(self, query: str, max_results: int = 5) -> list:
        try:
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )

            results = []
            for paper in search.results():
                results.append({
                    "title": paper.title,
                    "authors": [author.name for author in paper.authors],
                    "abstract": paper.summary,
                    "url": paper.entry_id,
                    "arxiv_id": paper.entry_id.split('/')[-1],
                    "published": str(paper.published.date())
                })
            
            return results
        except Exception as e:
            return [{"error": f"Error during arXiv search: {str(e)}"}]


class DownloadPaperTool(Tool):
    name = "download_paper"
    description = """
    Downloads the full text PDF of a paper from arXiv by ID.
    Args:
        arxiv_id (str): arXiv paper ID (e.g., '2103.14030')
    Returns:
        str: Path to the downloaded PDF file
    """
    inputs = {
        "arxiv_id": {"type": "string", "description": "ArXiv paper ID"}
    }
    output_type = "string"

    def forward(self, arxiv_id: str) -> str:
        try:
            paper = next(arxiv.Search(id_list=[arxiv_id]).results())
            filename = f"{arxiv_id.replace('/', '_')}.pdf"
            paper.download_pdf(filename=filename)
            return filename
        except Exception as e:
            return f"Error downloading paper: {str(e)}"
