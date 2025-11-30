# agents/seo_agent.py
from core.ai_client import ask_model
import textwrap

def generate_seo_blog(topic, research_summary, tone="informative", word_count=800):
    prompt = f"""
You are an expert SEO content writer. Using the research summary below, create a complete SEO-optimized blog post on the topic "{topic}".
Requirements:
- Tone: {tone}
- Target length: approx {word_count} words
- Include: short meta description (max 160 chars), suggested 5 SEO keywords, an outline, and the full blog content with H2/H3 headings.
- Use the research summary as the factual basis. Add a final "References" section with bullet links.

Research Summary:
{research_summary}

Return in markdown.
"""
    return ask_model(prompt)
