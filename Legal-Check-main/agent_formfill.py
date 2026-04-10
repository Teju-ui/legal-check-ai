"""
agent_formfill.py — Form Filler Agent
Responsible for: Analysing uploaded forms and generating a precise
"How to Fill This Form" guide. Only reports fields with direct evidence.
Called by the orchestrator in agent.py. Never import app.py.
"""
import os
from groq import Groq
from dotenv import load_dotenv
from prompts import get_system_prompt, formfill_prompt

load_dotenv()
_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
_MODEL = "llama-3.1-8b-instant"


def _call(system: str, user: str, temperature: float = 0.1, max_tokens: int = 4096) -> str:
    response = _client.chat.completions.create(
        model=_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content


def run_formfill_analysis(document_text: str, lang: str = "en") -> str:
    """
    Analyse a form document and return a structured 'How to Fill' guide.
    Strict: only returns fields with direct evidence quotes from the document.
    """
    return _call(
        get_system_prompt(lang),
        formfill_prompt(document_text, lang),
        temperature=0.1,
        max_tokens=4096,
    )
