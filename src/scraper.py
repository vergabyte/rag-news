import time
import json
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from src.utils import logger
from config import REQUEST_TIMEOUT, SCRAPE_DELAY


def load_urls(filepath):
    with open(filepath, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]
    return urls


def fetch_article(url, timeout=REQUEST_TIMEOUT):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    if 'wikipedia.org' in url:
        for unwanted in soup.select('.mw-editsection, .navbox, .vertical-navbox, '
                                   '.sistersitebox, .noprint, .mw-jump-link, '
                                   '.printfooter, .catlinks, #toc, .infobox, '
                                   '.reflist, .refbegin'):
            unwanted.decompose()
        
        content = soup.find('div', {'id': 'mw-content-text'})
        if content:
            paragraphs = content.find_all('p')
            text = ' '.join([p.get_text(separator=' ', strip=True) for p in paragraphs])
        else:
            text = soup.get_text(separator=' ', strip=True)
    else:
        article = soup.find('article')
        text = article.get_text(separator=' ', strip=True) if article else soup.get_text(separator=' ', strip=True)
    
    text = ' '.join(text.split())
    
    if not text or len(text) < 100:
        raise ValueError(f'Extracted text too short for {url}')
    
    return {'url': url, 'content': text}


def scrape_articles(urls, delay=SCRAPE_DELAY):
    articles = []
    
    for i, url in enumerate(urls, 1):
        print(f'Fetching {i}/{len(urls)}: {url}')
        
        article = fetch_article(url)
        articles.append(article)
        
        if i < len(urls):
            time.sleep(delay)
    
    logger.info(f'Successfully fetched {len(articles)}/{len(urls)} articles')
    print(f'\nSuccessfully fetched {len(articles)}/{len(urls)} articles')
    
    return articles


def save_articles_to_json(articles, filepath):
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)
    
    logger.info(f'Saved {len(articles)} articles to {filepath}')


def load_articles_from_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    logger.info(f'Loaded {len(articles)} articles from {filepath}')
    return articles