from llama_index.llms.ollama import Ollama
from llama_parse import LlamaParse
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, PromptTemplate
from llama_index.core.embeddings import resolve_embed_model



llm = Ollama(model="llama3", request_timeout=120.0)
resp = llm.complete("Who is Paul Graham?")
print(resp)

