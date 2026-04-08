# 🎯 Interview Prep Agent

I built this because I was tired of generic interview prep advice.
I wanted something brutally honest — tailored to my resume and real job descriptions.

So I built an agent that does exactly that with a follow-up chat interface for deeper exploration.

It forces the question:
“given THIS resume and THIS job, what actually matters?”

Built using raw Anthropic tool use, Python, and Streamlit.

---

## What It Does

Paste a job URL (or the JD text directly) and upload your resume. The agent autonomously:

1. **Scrapes the job posting** — fetches and parses the job description from the URL
2. **Researches the company** — searches for recent news, culture signals, and tech stack via Tavily
3. **Matches your resume** — semantically compares your resume against job requirements using sentence-transformers
4. **Generates a tailored report** including:
   - Role snapshot
   - Match score with honest gap analysis
   - 6 interview questions (3 role-generic + 3 tailored to your specific resume)
   - Red flags about the role or company
   - Positioning angle — how to frame yourself for this specific role
   - Resume feedback: grammar issues, weak phrasing, and rewrite suggestions using JD vocabulary
5. **Follow-up chat** — ask anything about the role, your answers, or your resume after the report generates

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | Anthropic API (`claude-sonnet-4-6`) |
| Orchestration | Raw Anthropic tool use (no LangChain) |
| Search | Tavily API |
| Scraping | `requests` + `BeautifulSoup` |
| Resume parsing | `pypdf` |
| Semantic matching | `sentence-transformers` (`all-MiniLM-L6-v2`) |
| UI | Streamlit |
| Deployment | Streamlit Community Cloud |

---

## Architecture

This project uses **raw Anthropic tool use** — no orchestration framework. The agent loop in `agent.py` is a `while True` that:

1. Calls the Claude API with tool schemas and conversation history
2. Checks `stop_reason` — if `tool_use`, executes the requested tool and feeds the result back
3. If `end_turn`, extracts the final report and breaks

Claude decides which tools to call and in what order. The code executes them and manages the message history. That's the entire pattern.

```
You → Claude (job URL + resume + tool schemas)
Claude → agent (call scrape_job_description)
agent → Claude (scraped JD content)
Claude → agent (call research_company)
agent → Claude (Tavily search results)
Claude → agent (call match_resume_to_job)
agent → Claude (match scores and gaps)
Claude → You (final interview prep report)
```

---

## Project Structure

```
interview-agent/
├── tools/
│   ├── __init__.py
│   ├── scraper.py          # Job posting scraper
│   ├── researcher.py       # Tavily company research
│   └── resume_matcher.py   # Semantic resume matching
├── agent.py                # Orchestration loop + system prompt
├── app.py                  # Streamlit UI
├── main.py                 # CLI entry point
├── requirements.txt
└── .env                    # API keys (not committed)
```

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/Chingapo/Interview-agent.git
cd Interview-agent
```

**2. Create and activate a virtual environment**
```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# Mac/Linux
python -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables**

Create a `.env` file in the project root:
```
ANTHROPIC_API_KEY=your_anthropic_key_here
TAVILY_API_KEY=your_tavily_key_here
```

Get your keys from:
- Anthropic: [console.anthropic.com](https://console.anthropic.com)
- Tavily: [tavily.com](https://tavily.com)

**5. Add your resume**

Place your resume as `resume.pdf` in the project root.

---

## Running

**Streamlit UI (recommended)**
```bash
streamlit run app.py
```
Opens at `http://localhost:8501`

**CLI**
```bash
python main.py "https://www.linkedin.com/jobs/view/..."
```

---

## Deployment

Deployed on Streamlit Community Cloud. To deploy your own instance:

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo, set main file to `app.py`
4. Add secrets in Advanced Settings:
```toml
ANTHROPIC_API_KEY = "your_key"
TAVILY_API_KEY = "your_key"
```

---

## Known Limitations

- **LinkedIn** — partially works depending on whether the posting is publicly accessible. If scraping fails, use the manual JD paste option.
- **Wellfound** — blocks scrapers. Use manual paste.
- **Naukri** — returns thin content on some listings. Use manual paste.
- **Resume match score** — uses semantic similarity via `all-MiniLM-L6-v2`. If your resume doesn't use JD-adjacent vocabulary, scores will be low even when you're a genuine fit. The qualitative analysis Claude generates is more reliable than the raw score.
- **Rate limiting** — 3 runs per hour per browser session. Clear cookies to reset (sufficient for personal use).

---

## Why Raw Anthropic Tool Use

Most agent tutorials reach for LangChain immediately. I used the raw Anthropic API to understand what orchestration frameworks are actually doing under the hood — managing the messages list, handling `stop_reason`, routing tool calls, feeding results back.

Understanding the pattern at this level, LangChain and LangGraph make complete sense.

---