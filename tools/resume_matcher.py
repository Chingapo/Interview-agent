import os
import re
from pypdf import PdfReader
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer, util

load_dotenv()

model = SentenceTransformer("all-MiniLM-L6-v2")

def load_resume(path: str) -> str:
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text+=page.extract_text()
    return text

def match_resume_to_job(job_description: str, resume_path: str = "resume.pdf") -> dict:
    try:
        resume_text = load_resume(resume_path)

        # Split the job description into sentences
        sentences = re.split(r'(?<=[.?!])\s+|\n+', job_description)
        requirements = [s.strip() for s in sentences if len(s.strip()) > 30]

        resume_chunks = [
            resume_text[i:i+500] 
            for i in range(0, len(resume_text), 500)
        ]
        resume_embeddings = model.encode(resume_chunks, convert_to_tensor=True)

        matches = []
        gaps = []

        for req in requirements[:20]:
            req_embedding = model.encode(req, convert_to_tensor=True)

            scores = util.cos_sim(resume_embeddings, req_embedding)
            score = scores.max().item() 

            if score >= 0.25:
                matches.append({"requirement": req, "score": round(score, 2)})
            else:
                gaps.append({"requirement": req, "score": round(score, 2)})
            
            overall_score = round(
                sum(m["score"] for m in matches)/max(len(requirements[:20]), 1), 2
            )

            return {
                "success": True,
                "overall_score": overall_score,
                "matches": matches[:10],
                "gaps": gaps[:10],
                "resume_snippet": resume_text[:500]
            }
    except Exception as e:
        return {"success": False, "error": str(e)}
    
RESUME_MATCHER_TOOL = {
    "name": "match_resume_to_job",
    "description": "Compares the job description requirements against the candidate's resume using semantic similarity. Returns matched strengths, gaps, and an overall fit score. Use this after scraping the job description.",
    "input_schema": {
        "type": "object",
        "properties": {
            "job_description": {
                "type": "string",
                "description": "The full job description text scraped from the posting"
            }
        },
        "required": ["job_description"]
    }
}