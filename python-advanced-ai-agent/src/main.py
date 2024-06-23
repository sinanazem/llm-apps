from llama_index.llms.ollama import Ollama
from llama_parse import LlamaParse
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, PromptTemplate
from llama_index.core.embeddings import resolve_embed_model


llm = Ollama(model="llama2", request_timeout=120.0)
# resp = llm.complete("Who is Paul Graham?")
# print(resp)

# parser = LlamaParse(result_type="markdown", api_key="llx-swyC8YQELkbRNWTCgK05APugGBE9IbglTQkTcJJD2pGVurZy")
# file_extractor = {".pdf": parser}
documents = SimpleDirectoryReader("/mnt/c/Users/user/OneDrive/Desktop/llm-apps/python-advanced-ai-agent/data").load_data()
# embed_model = resolve_embed_model("local:BAAI/bge-m3")
vector_index = VectorStoreIndex.from_documents(documents, embed_model='local')
query_engine = vector_index.as_query_engine(llm=llm)

query_engine.query("what are some of thr routes in the api?")