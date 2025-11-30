# ui/app.py
import streamlit as st
import sys, os
# ensure project root in path (helpful if running from UI folder)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.rag_agent import RAGAgent
from agents.summarizer_agent import summarize_text_blocks
from agents.seo_agent import generate_seo_blog
from agents.pdf_agent import PDFReport
from core.storage import save_record, load_history

st.set_page_config(page_title="Autonomous Research Agent", layout="wide", initial_sidebar_state="expanded")

# Sidebar / Settings
st.sidebar.title("Settings & Tools")
dark = st.sidebar.checkbox("Dark mode", value=False)
st.sidebar.markdown("---")
st.sidebar.markdown("**Agents**")
use_rag = st.sidebar.checkbox("Use RAG (web + docs)", value=True)
use_seo = st.sidebar.checkbox("Enable SEO blog generator", value=True)
st.sidebar.markdown("---")
st.sidebar.markdown("Saved History")
history = load_history(10)
for i, h in enumerate(history[:5]):
    st.sidebar.write(f"{i+1}. {h.get('query')[:50]} ...")

# main UI
st.title("🤖 Autonomous Research Agent — Advanced MVP")
st.markdown("Enter a research query and choose actions. The agent can fetch web docs, summarize, produce SEO blogs, and export PDF.")

col1, col2 = st.columns([3,1])

with col1:
    query = st.text_area("Research Query", height=120)
    submit = st.button("Run Research")
    st.markdown("---")
    st.markdown("**Quick Actions**")
    if st.button("Generate SEO Blog (from last summary)"):
        st.session_state.get("generate_seo", True)

with col2:
    st.markdown("**Options**")
    top_k = st.number_input("RAG top k", min_value=1, max_value=10, value=3)
    max_pages = st.slider("Max pages to scrape", 1, 10, 6)
    download_json = st.button("Download History JSON")

# run pipeline
if submit and query.strip():
    st.session_state["last_query"] = query
    if use_rag:
        st.info("Running RAG (search + scrape)...")
    else:
        st.info("Skipping RAG, using LLM only...")

    rag = RAGAgent()
    blocks = []
    if use_rag:
        with st.spinner("Searching and scraping web..."):
            docs = rag.build_corpus(query, max_pages=max_pages)
            rag.index()
            blocks = rag.query(query, top_k=top_k)
            st.success(f"Fetched {len(rag.docs)} pages; returning top {len(blocks)}")
            for b in blocks:
                st.markdown(f"**Source:** [{b.get('title') or b.get('url')}]({b.get('url')})")
                st.write(b.get('text')[:400] + ("..." if len(b.get('text'))>400 else ""))
                st.markdown("---")
    # Summarize using summarizer agent
    with st.spinner("Synthesizing summary..."):
        if blocks:
            summary_md = summarize_text_blocks(blocks)
        else:
            # fallback to asking LLM directly
            from core.ai_client import ask_model
            summary_md = ask_model(f"Give a concise research summary for: {query}")
    st.markdown("## Research Summary")
    st.markdown(summary_md)

    # Save history
    save_record({"query": query, "summary": summary_md, "sources": [b.get("url") for b in blocks]})

    # Actions
    colA, colB, colC = st.columns(3)
    with colA:
        if st.button("Download PDF Report"):
            pdf = PDFReport(title=f"Research - {query[:40]}")
            pdf.add_markdown(f"# Research on: {query}\n\n{summary_md}")
            fname = pdf.save()
            with open(fname, "rb") as f:
                st.download_button("Download PDF", f, file_name="research_report.pdf", mime="application/pdf")
    with colB:
        if st.button("Generate SEO Blog"):
            if not summary_md:
                st.error("No summary available yet.")
            else:
                with st.spinner("Generating SEO blog..."):
                    blog_md = generate_seo_blog(query, summary_md, word_count=900)
                st.markdown("## SEO Blog Post")
                st.markdown(blog_md)
                save_record({"query": query, "summary": summary_md, "blog": blog_md})
    with colC:
        if st.button("Save JSON of this result"):
            import json, tempfile
            rec = {"query": query, "summary": summary_md, "sources":[b.get("url") for b in blocks]}
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
            tmp.write(json.dumps(rec, ensure_ascii=False, indent=2).encode("utf-8"))
            tmp.close()
            with open(tmp.name, "rb") as f:
                st.download_button("Download JSON", f, file_name="research_result.json", mime="application/json")

# history viewer
st.markdown("---")
st.subheader("Recent history")
hist = load_history(10)
for h in hist:
    st.markdown(f"**{h.get('query')}** — saved at {h.get('_saved_at')}")
    st.write(h.get("summary")[:600] + ("..." if len(h.get("summary"))>600 else ""))
    st.markdown("---")

# optional download history
if download_json:
    import json, io
    allh = load_history(200)
    buf = io.BytesIO(json.dumps(allh, ensure_ascii=False, indent=2).encode("utf-8"))
    st.download_button("Download full history", buf, file_name="history.json", mime="application/json")
