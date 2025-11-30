# agents/summarizer_agent.py
from core.ai_client import ask_model
import textwrap

def summarize_text_blocks(blocks, prompt_extra=""):
    """
    blocks: list of dicts {"url","title","text"}
    returns a structured markdown summary
    """
    # Build a short combined prompt
    coll = []
    for b in blocks:
        snippet = b["text"][:1500]  # safety slice
        coll.append(f"Source: {b.get('title') or b.get('url')}\n{snippet}\n")
    combined = "\n\n".join(coll)
    prompt = f"""You are a research assistant. Given the following source snippets, produce:
1) a concise Executive Summary (3-6 lines)
2) Key findings (5 bullets)
3) Conflicts or contradictions (if any)
4) Top 5 citations with short snippets and urls

{prompt_extra}

SOURCES:
{combined}

Return the answer in MARKDOWN.
"""
    resp = ask_model(prompt)
    return resp
