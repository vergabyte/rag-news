from src.scraper import load_urls, scrape_articles, save_articles_to_json, load_articles_from_json
from src.embeddings import chunk_documents, create_vector_store, load_vector_store
from src.chatbot import create_rag_chain, query_chatbot, format_sources
from src.utils import logger
from config import URLS_FILE, SCRAPED_DATA_FILE, CHROMA_DB_PATH


def build_knowledge_base(force_rescrape=False):
    logger.info('Starting knowledge base build')
    
    if SCRAPED_DATA_FILE.exists() and not force_rescrape:
        print('Loading articles from JSON...\n')
        articles = load_articles_from_json(SCRAPED_DATA_FILE)
    else:
        print('Scraping articles...\n')
        urls = load_urls(URLS_FILE)
        articles = scrape_articles(urls)
        
        if not articles:
            logger.error('No articles scraped')
            raise ValueError('No articles were scraped')
        
        save_articles_to_json(articles, SCRAPED_DATA_FILE)
    
    chunks = chunk_documents(articles)
    vectorstore = create_vector_store(chunks, CHROMA_DB_PATH)
    logger.info('Vector store created successfully')
    
    return vectorstore


def initialize_chatbot(force_rescrape=False):
    logger.info('Starting RAG chatbot')
    
    if CHROMA_DB_PATH.exists() and not force_rescrape:
        print('Loading existing knowledge base...\n')
        vectorstore = load_vector_store(CHROMA_DB_PATH)
    else:
        print('Building knowledge base...\n')
        vectorstore = build_knowledge_base(force_rescrape)
    
    chain, retriever = create_rag_chain(vectorstore)
    logger.info('RAG chain initialized')
    
    return chain, retriever


def chat_loop(chain, retriever):
    print('RAG Chatbot ready! (type "exit" to quit)\n')
    
    while True:
        question = input('You: ').strip()
        
        if question.lower() in ['exit', 'quit']:
            logger.info('User exited')
            print('Goodbye!')
            break
        
        if not question:
            continue
        
        print('\nThinking...\n')
        answer, sources = query_chatbot(chain, retriever, question)
        
        print(f'Bot: {answer}\n')
        
        source_urls = format_sources(sources)
        if source_urls:
            print('Sources:')
            for url in source_urls:
                print(f'  - {url}')
        print()


def run_chatbot(force_rescrape=False):
    chain, retriever = initialize_chatbot(force_rescrape)
    chat_loop(chain, retriever)


if __name__ == '__main__':
    import sys
    run_chatbot('--rescrape' in sys.argv)