from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from config import LLM_MODEL, GROQ_API_KEY, K_RETRIEVAL


def create_rag_chain(vectorstore, model=LLM_MODEL, k=K_RETRIEVAL):
    llm = ChatGroq(model=model, groq_api_key=GROQ_API_KEY, temperature=0.7)
    retriever = vectorstore.as_retriever(search_kwargs={'k': k})
    
    template = '''Answer the question based only on the following context:
{context}

Question: {question}

Answer:'''
    
    prompt = PromptTemplate.from_template(template)
    format_docs = lambda docs: '\n\n'.join([doc.page_content for doc in docs])
    
    chain = (
        {'context': retriever | format_docs, 'question': RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain, retriever


def query_chatbot(chain, retriever, question):
    answer = chain.invoke(question)
    sources = retriever.invoke(question)

    # # Debug: print what chunks were retrieved
    # print('\n--- Retrieved Chunks (Debug) ---')
    # for i, doc in enumerate(sources, 1):
    #     print(f'\nChunk {i}:')
    #     print(doc.page_content[:200])
    #     print('...')
    # print('--- End Chunks ---\n')

    return answer, sources


def format_sources(sources):
    return list({doc.metadata['source'] for doc in sources if 'source' in doc.metadata})