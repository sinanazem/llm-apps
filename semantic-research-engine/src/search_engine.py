import os
import chainlit as cl
from langchain_community.document_loaders import ArxivLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv
load_dotenv()


prompt = ChatPromptTemplate([
    ("system", "You are a helpful assistant. Use provided {context} to answer user {question}"),
    ("human", "{user_input}"),
])


@cl.on_chat_start
async def retrieve_docs():
    # QUERY PORTION
    arxiv_query = None
    # Wait for the user to send in a topic
    while arxiv_query is None:
        arxiv_query = await cl.AskUserMessage(
            content="Please enter a topic to begin!", timeout=15).send()
    query = arxiv_query['output']

    # ARXIV DOCS PORTION
    arxiv_docs = ArxivLoader(query=arxiv_query, load_max_docs=3).load()
    # Prepare arXiv results for display
    arxiv_papers = [f"Published: {doc.metadata['Published']} \n "
                    f"Title: {doc.metadata['Title']} \n "
                    f"Authors: {doc.metadata['Authors']} \n "
                    f"Summary: {doc.metadata['Summary'][:50]}... \n---\n"
                    for doc in arxiv_docs]

    await cl.Message(content=f"{arxiv_papers}").send()

    await cl.Message(content=f"Downloading and chunking articles for {query} "
                             f"This operation can take a while!").send()

    # DB PORTION
    pdf_data = []
    for doc in arxiv_docs:
        text_splitter = RecursiveCharacterTextSplitter(
                        chunk_size=1000, chunk_overlap=100)
        texts = text_splitter.create_documents([doc.page_content])
        pdf_data.append(texts)
  
    llm = ChatOpenAI(model='gpt-3.5-turbo',
                         temperature=0)
    embeddings = HuggingFaceEmbeddings(
                 model_name="sentence-transformers/all-MiniLM-l6-v2")
    db = Chroma.from_documents(pdf_data[0], embeddings)

    # CHAIN PORTION
    chain = RetrievalQA.from_chain_type(llm=llm,
                                            chain_type="stuff",
                                            retriever=db.as_retriever(),
                                            chain_type_kwargs={
                                                "verbose": True,
                                                "prompt": prompt
                                            }
                                            )

    # Let the user know that the pipeline is ready
    await cl.Message(content=f"Database creation for `{query}` complete. "
                             f"You can now ask questions!").send()

    cl.user_session.set("chain", chain)
    cl.user_session.set("db", db)
    
@cl.on_message
async def retrieve_docs(message: cl.Message):
    question = message.content
    chain = cl.user_session.get("chain")
    db = cl.user_session.get("db")
    # Create a new instance of the callback handler for each invocation
    # cb = client.langchain_callback()
    variables = {"context": db.as_retriever(search_kwargs={"k": 1}), 
                 "query": question}
    database_results = await chain.acall(variables)
    results = [f"Question: {question} "
               f"\n Answer: {database_results['result']}"]
    await cl.Message(results).send()