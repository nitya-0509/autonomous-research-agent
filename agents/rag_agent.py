# agents/rag_agent.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import re
import time

# small helpers
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; research-agent/1.0)"}

def simple_search_duckduckgo(query, max_results=8):
    # Basic HTML DuckDuckGo search (no API)
    url = "https://duckduckgo.com/html/"
    params = {"q": query}
    r = requests.post(url, data=params, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(r.text, "lxml")
    results = []
    for a in soup.select(".result__a")[:max_results]:
        href = a.get("href")
        title = a.get_text(strip=True)
        if href:
            results.append({"title": title, "url": href})
    return results

def fetch_text_from_url(url, max_chars=15000):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "lxml")
        # remove scripts/styles
        for s in soup(["script", "style", "noscript", "header", "footer", "aside"]):
            s.decompose()
        text = soup.get_text(separator="\n")
        # basic cleanup
        text = re.sub(r"\n\s+\n", "\n", text)
        text = " ".join(text.split())
        return text[:max_chars]
    except Exception:
        return ""

class RAGAgent:
    def __init__(self):
        self.docs = []  # list of {"url", "title", "text"}
        self.vectorizer = None
        self.tfidf = None

    def build_corpus(self, query, max_pages=6):
        results = simple_search_duckduckgo(query, max_results=max_pages)
        docs = []
        for r in results:
            txt = fetch_text_from_url(r["url"])
            if txt and len(txt) > 200:
                docs.append({"url": r["url"], "title": r.get("title",""), "text": txt})
            time.sleep(0.5)  # be polite
        self.docs = docs
        return docs

    def index(self):
        texts = [d["text"] for d in self.docs]
        if not texts:
            self.tfidf = None
            self.vectorizer = None
            return
        self.vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
        self.tfidf = self.vectorizer.fit_transform(texts)

    def query(self, q, top_k=3):
        if not self.tfidf:
            return []
        qv = self.vectorizer.transform([q])
        sims = linear_kernel(qv, self.tfidf).flatten()
        idxs = sims.argsort()[::-1][:top_k]
        return [self.docs[i] for i in idxs if sims[i] > 0]

    def build_and_query(self, query, top_k=3):
        self.build_corpus(query, max_pages=6)
        self.index()
        return self.query(query, top_k=top_k)
