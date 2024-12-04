from typing import List, Any, Dict
from langchain_community.document_loaders import PyPDFLoader
from pprint import pprint
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever

class PDFChatbot:
    def __init__(self, local_path: str, model: str = "llama3"):
        self.local_path = local_path
        self.model = model
        self.vector_db = None
        self.llm = ChatOllama(model=model)
        self.chain = None

    def load_pdf(self) -> List[Dict[str, Any]]:
        """Load PDF from a local path."""
        loader = PyPDFLoader(file_path=self.local_path)
        return loader.load()

    def split_text(self, data: List[Dict[str, Any]], chunk_size: int = 7500, chunk_overlap: int = 100) -> List[Dict[str, Any]]:
        """Split text into chunks."""
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        return text_splitter.split_documents(data)

    def create_vector_db(self, chunks: List[Dict[str, Any]], collection_name: str = 'local-rag') -> None:
        """Create a vector database from text chunks."""
        self.vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=OllamaEmbeddings(model="nomic-embed-text", show_progress=True),
            collection_name=collection_name
        )

    def setup_chain(self) -> None:
        """Setup the retrieval augmented generation (RAG) chain."""
        QUERY_PROMPT = PromptTemplate(
            input_variables=["question"],
            template="""You are an AI language model assistant. Your task is to generate five
            different versions of the given user question to retrieve relevant documents from
            a vector database. By generating multiple perspectives on the user question, your
            goal is to help the user overcome some of the limitations of the distance-based
            similarity search. Provide these alternative questions separated by newlines.
            Original question: {question}""",
        )

        retriever = MultiQueryRetriever.from_llm(
            self.vector_db.as_retriever(),
            self.llm,
            prompt=QUERY_PROMPT
        )

        # RAG prompt
        template = """Answer the question based ONLY on the following context:
        {context}
        Question:{question}"""

        prompt = ChatPromptTemplate.from_template(template)

        self.chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )

    def query_chain(self, question: str) -> Any:
        """Invoke the chain with a question."""
        return self.chain.invoke(question)


def main():
    local_path = "/mnt/c/Users/user/OneDrive/Desktop/rag-pdf-chatbot/data/WEF_The_Global_Cooperation_Barometer_2024.pdf"
    
    if not local_path:
        print("Upload a PDF file")
        return
    
    chatbot = PDFChatbot(local_path=local_path)
    data = chatbot.load_pdf()
    chunks = chatbot.split_text(data)
    chatbot.create_vector_db(chunks)
    chatbot.setup_chain()
    
    response = chatbot.query_chain("What are the 5 pillars of global cooperation?")
    pprint(response)


if __name__ == '__main__':
    main()