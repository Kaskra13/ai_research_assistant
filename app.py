import gradio as gr
from agents.orchestrator import ResearchOrchestrator
import config
import json


orchestrator = ResearchOrchestrator()


def format_research_report(result_dict):
    if isinstance(result_dict, str):
        return result_dict
    
    if isinstance(result_dict, dict):
        report = "# Research report\n\n"
        
        if 'Overview' in result_dict:
            report += f"## Overview\n{result_dict['Overview']}\n\n"
        
        if 'Key findings' in result_dict:
            report += "## Key findings\n\n"
            for paper, finding in result_dict['Key findings'].items():
                report += f"### {paper}\n{finding}\n\n"
        
        if 'Common themes and trends' in result_dict:
            report += f"## Common themes and trends\n{result_dict['Common themes and trends']}\n\n"
        
        if 'Most important citations' in result_dict:
            report += "## Most important citations\n\n"
            for paper, citations in result_dict['Most important citations'].items():
                report += f"### {paper}\n"
                if isinstance(citations, dict):
                    if citations.get('arxiv_refs'):
                        report += f"- **arXiv references:** {', '.join(citations['arxiv_refs'])}\n"
                    if citations.get('doi_refs'):
                        report += f"- **DOI references:** {', '.join(citations['doi_refs'])}\n"
                    report += f"- **Total citations:** {citations.get('total_count', 0)}\n"
                    report += f"- **Numbered references:** {citations.get('numbered_refs', 0)}\n"
                report += "\n"
        
        return report
    
    return json.dumps(result_dict, indent=2, ensure_ascii=False)


def conduct_research(query: str, num_papers: int) -> tuple:
    try:
        result = orchestrator.research(query, num_papers)
        
        formatted_report = format_research_report(result["result"])
        
        return (
            formatted_report,
            "Research completed successfully"
        )
    except Exception as e:
        return (f"Error: {str(e)}", "Research failed")


with gr.Blocks(title="Multi-Agent Research Assistant") as demo:
    gr.Markdown("""
    # Multi-Agent Research Assistant
    ### Powered by Hugging Face & smolagents
    
    This agent automatically:
    - Searches for scientific papers in arXiv
    - Downloads and analyzes full texts
    - Generates summaries of key information
    - Synthesizes results into a single report
    """)
    
    with gr.Row():
        with gr.Column():
            query_input = gr.Textbox(
                label="Research query",
                placeholder="e.g., 'transformer models for time series forecasting'",
                lines=2
            )
            num_papers_slider = gr.Slider(
                minimum=1,
                maximum=3,
                value=2,
                step=1,
                label="Number of papers to analyze"
            )
            submit_btn = gr.Button("Start research", variant="primary")
        
        with gr.Column():
            output_report = gr.Markdown(
                label="Research report"
            )
            status_output = gr.Textbox(label="Status", lines=1)
    
    submit_btn.click(
        fn=conduct_research,
        inputs=[query_input, num_papers_slider],
        outputs=[output_report, status_output]
    )
    
    gr.Examples(
        examples=[
            ["Large language models for code generation", 2],
            ["Anomaly detection in time series data", 2],
            ["Multimodal learning with transformers", 2],
        ],
        inputs=[query_input, num_papers_slider]
    )


if __name__ == "__main__":
    demo.launch(
        share=False,
        server_name="127.0.0.1",
        server_port=7860,
        theme=gr.themes.Soft()
    )
