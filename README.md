# News Chat (Groq)

This project builds a Retrieval-Augmented Generation (RAG) chatbot over scraped news articles.
It uses BeautifulSoup for scraping, LangChain for the RAG chain, ChromaDB as the vector store, and sentence-transformers for embeddings.

## Key libraries

- beautifulsoup4 — scraping HTML
- langchain — RAG chain and tools
- chromadb — vector store
- sentence-transformers — embedding model
- python-dotenv — load environment variables

## Files and layout

- `main.py` — entrypoint; run the chat UI with `python main.py`.
- `config.py` — project configuration (paths, models, keys).
- `data/urls.txt` — list of URLs to scrape (one per line).
- `data/scraped_articles.json` — scraped articles cache (created after running).
- `chroma_db/` — local ChromaDB database (created automatically).
- `src/` — application source: scraper, embeddings, chatbot, utils.

## Quick start

1. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure secrets using `.env`

For safety, keep secrets out of Git. Copy the example file and add your API key(s):

```bash
cp .env.example .env
# then edit .env and set your key(s), e.g.:
# GROQ_API_KEY=your_groq_api_key_here
```

4. Add URLs to `data/urls.txt` (one URL per line) or use the included list.

5. Run the chatbot (interactive):

```bash
python main.py
```

If you want to force a re-scrape and rebuild of the knowledge base:

```bash
python main.py --rescrape
```

## Notes

- The Chroma DB files are stored in `chroma_db/` (see `config.py` for the exact path). You can delete this folder to rebuild from scratch.
- Embeddings use the `sentence-transformers/all-MiniLM-L6-v2` model by default (configured in `config.py`).
- The project expects reasonable `URLS_FILE` entries; invalid or unreachable URLs will be skipped.