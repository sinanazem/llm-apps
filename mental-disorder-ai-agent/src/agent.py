from langchain_community.embeddings import OpenAIEmbeddings
from qdrant_client import QdrantClient
from langchain_community.vectorstores import Qdrant

import os
from dotenv import load_dotenv

# Specify the path to your .env file

ENV_PATH = '/mnt/c/Users/user/OneDrive/Desktop/llm-apps/mental-disorder-ai-agent/.env'

# Load environment variables from the specified .env file
load_dotenv(dotenv_path=ENV_PATH)


from langchain.document_loaders import PyPDFDirectoryLoader

loader = PyPDFDirectoryLoader("/mnt/c/Users/user/OneDrive/Desktop/llm-apps/mental-disorder-ai-agent/data")
data= loader.load_and_split()


from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
documents = text_splitter.split_documents(data)

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
def create_db(documents):
    return Qdrant.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name="my_documents",
        location=":memory:",
        force_recreate=False,
    )
db = create_db(documents)


from langchain.tools import BaseTool, StructuredTool, tool

from langchain_openai import ChatOpenAI

from langchain.chains import (
    StuffDocumentsChain, LLMChain, ConversationalRetrievalChain
)

session_state = {}

@tool
def find_relevant_books(user_query):
    """
    Return all relevant books based on user query.
    Important: This function should be called only for queries that require finding specific books.
    For general queries that do not require finding specific books, use other available functions.
    """
    retriever = db.as_retriever(
        search_type="mmr", search_kwargs={"k": 4, "lambda_mult": 0.25}
    )
    relevant_docs = retriever.get_relevant_documents(user_query)
    session_state["relevant_docs"] = relevant_docs
    session_state["retriever"] = retriever
    return relevant_docs

llm = ChatOpenAI(
    model="gpt-4o", 
    temperature=0, 
    openai_api_key=os.getenv("OPEN_AI_KEY")
)
@tool
def qa(user_query):
    """
    Answer user questions based on the retrieved documents
    """
    retriever = session_state["retriever"]
    relevant_docs = session_state.get("relevant_docs")
    if relevant_docs is None:
        # If no documents are stored, retrieve them
        relevant_docs = retriever.get_relevant_documents(user_query)
        session_state["relevant_docs"] = relevant_docs
    
    # Create a chain to answer questions using stored documents
    qa = ConversationalRetrievalChain.from_llm(llm, retriever)
    chat_history = []
    result = qa(
        {"question": user_query, "chat_history": chat_history, "context": relevant_docs}
    )
    return result


from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

# Define the prompt template
prompt_template = """
You are a helpful AI assistant specializing in answering questions 
related to books from users. Use retrieved relevant books to 
answer questions.
====================
{relevant_docs}
"""
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are helpful AI assistant. Use the following 
               template for your actions and observations."""
        ),
        ("user", prompt_template),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.tools import format_tool_to_openai_function
from langchain.tools import Tool

# These are custom functions for finding books, answering questions, and creating topic networks.
tools = [find_relevant_books, qa]
# OpenAI Function Formatting. This converts the tools into a format compatible with OpenAI's function calling feature.
functions = [format_tool_to_openai_function(f) for f in tools]
#This sets up the GPT-4o model with the defined functions.
model = ChatOpenAI(
    temperature=0,
    model_name="gpt-4o",
).bind(functions=functions)


from langchain.agents import AgentExecutor
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.memory import ConversationBufferMemory

# Set up the agent chain.
# including assigning relevant documents and agent scratchpad, applying the prompt, running the model, and parsing the output.

agent_chain = (
    RunnablePassthrough.assign(
        agent_scratchpad=lambda x: format_to_openai_functions(x["intermediate_steps"]),
        relevant_docs=lambda x: "\n".join(
            str(doc) for doc in session_state.get("relevant_docs", [])
        ),
    )
    | prompt
    | model
    | OpenAIFunctionsAgentOutputParser()
)
# Set up a memory component to store conversation history.
memory = ConversationBufferMemory(
    return_messages=True,
    memory_key="chat_history",
    input_key="input",
    output_key="output",
)
# Initialize an agent with the agent and defined tools
# This combines all components into an executable agent that can process queries and maintain conversation context.
# With AgentExecutor, the agent is equipped with the tools and verbose output is enabled, allowing for detailed logging.


agent = AgentExecutor(agent=agent_chain, tools=tools, verbose=True, memory=memory)

def get_agent_response(query):
    
    return agent.invoke({"input": query})