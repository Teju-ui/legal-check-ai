"""
agent_leverage.py — Leverage Radar Agent
Responsible for: Power balance analysis, walk-away points, negotiation tactics.
Called by the orchestrator in agent.py.
"""
import os
from groq import Groq
from dotenv import load_dotenv
from prompts import get_system_prompt, leverage_mapping_prompt

load_dotenv()
_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
_MODEL = "llama-3.1-8b-instant"


def _call(system: str, user: str, temperature: float = 0.2) -> str:
    response = _client.chat.completions.create(
        model=_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=temperature,
        max_tokens=4096,
    )
    return response.choices[0].message.content


def run_leverage_mapping(document_text: str, lang: str = "en") -> str:
    """
    Full leverage scorecard: power balance, mutual/one-sided obligations,
    walk-away points, hidden leverage, negotiation tactics, bottom line.
    """
    return _call(get_system_prompt(lang), leverage_mapping_prompt(document_text, lang))


def extract_leverage_score(result: str) -> int | None:
    """Parse the numeric leverage score out of raw output. Returns None if not found."""
    if "Your Leverage Score:" not in result:
        return None
    try:
        score_line = [l for l in result.split("\n") if "Your Leverage Score:" in l][0]
        return int(''.join(filter(str.isdigit, score_line.split("Your Leverage Score:")[1][:5])))
    except Exception:
        return None
