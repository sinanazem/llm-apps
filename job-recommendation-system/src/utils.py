import openai
from dotenv import load_dotenv
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_embeddings(text):
   response = openai.Embedding.create(
       model="text-embedding-ada-002",
       input = text.replace("\n"," ")
   )
   embedding = response['data'][0]['embedding']
   return embedding