import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def research_company(company_name: str, role_title: str) -> dict:
    try:
        query = f"{company_name} company culture engineering team {role_title} 2024 2025"

        response = client.search(
            query=query,
            search_depth="basic",
            max_results=5,
            include_answer=True
        )

        results = []

        for r in response.get("results", []):
            results.append({
                "title": r.get("Title"),
                "url": r.get("url"),
                "content": r.get("content", "")[:1000]
            })

        return {
            "success": True,
            "summary": response.get("answer", ""),
            "sources": results
        }
    
    except Exception as e:
        return {"success": False, "error": str(e)}
    
RESEARCHER_TOOL = {
    "name": "research_company",
    "description": "Searches for recent information about a company — culture, tech stack, news, engineering team. Use this after scraping the job description to enrich context before generating the report.",
    "input_schema": {
        "type": "object",
        "properties": {
            "company_name": {
                "type": "string",
                "description": "The name of the company to research."
            },
            "role_title": {
                "type": "string",
                "description": "The job title being applied for, to focus the search"
            }
        },
        "required": ["company_name", "role_title"]
    }

}
