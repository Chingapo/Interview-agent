import requests
from bs4 import BeautifulSoup

def scrape_job_description(url: str) -> dict:
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        
        text = soup.get_text(separator="\n", strip=True)

        jd_signals = [
    "responsibilities", "requirements", "qualifications",
    "experience", "skills", "role", "position", "apply",
    "salary", "benefits", "team", "looking for", "you will",
    "we are", "candidate", "job description"
]

        content_lower = text[:5000].lower()
        signal_hits = sum(1 for signal in jd_signals if signal in content_lower)
        is_thin = signal_hits < 3


        return {
            "success": True, 
            "content": text[:8000],
            "is_thin": is_thin
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
    

SCRAPER_TOOL = {
    "name": "scrape_job_description",
    "description": "Scrapes a job posting URL and returns the raw job description text. Use this first, before any other tool.",
    "input_schema": {
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "The full URL of the job posting to scrape"
            }
        },
        "required": ["url"]
    }
}