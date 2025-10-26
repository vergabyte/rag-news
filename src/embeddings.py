from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from config import CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL


def chunk_documents(articles, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    
    chunks = []
    for article in articles:
        splits = splitter.split_text(article['content'])
        for split in splits:
            chunks.append({'content': split, 'metadata': {'source': article['url']}})
    
    print(f'Created {len(chunks)} chunks from {len(articles)} articles')
    return chunks


def create_vector_store(chunks, persist_directory):
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    
    texts = [chunk['content'] for chunk in chunks]
    metadatas = [chunk['metadata'] for chunk in chunks]
    
    vectorstore = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas,
        persist_directory=str(persist_directory)
    )
    
    print(f'Vector store created at {persist_directory}')
    return vectorstore


def load_vector_store(persist_directory):
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return Chroma(
        persist_directory=str(persist_directory),
        embedding_function=embeddings
    )