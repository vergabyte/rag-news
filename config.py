from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent

URLS_FILE = BASE_DIR / 'data' / 'urls.txt'
SCRAPED_DATA_FILE = BASE_DIR / 'data' / 'scraped_articles.json'
CHROMA_DB_PATH = BASE_DIR / 'chroma_db'

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

EMBEDDING_MODEL = 'sentence-transformers/all-MiniLM-L6-v2'
LLM_MODEL = 'llama-3.3-70b-versatile'
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
K_RETRIEVAL = 4

REQUEST_TIMEOUT = 10
SCRAPE_DELAY = 1