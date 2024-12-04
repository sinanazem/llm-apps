import openai
from pgvector.psycopg2 import register_vector
import numpy as np
from dotenv import load_dotenv
load_dotenv()


# Helper function: get embeddings for a text
def get_embeddings(text):
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input = text.replace("\n"," ")
    )
    embedding = response['data'][0]['embedding']
    return embedding

#Helper function: Get top 3 most similar documents from the database
def get_top3_similar_docs(query_embedding, connection):
    embedding_array = np.array(query_embedding)
    # Register pgvector extension
    register_vector(connection)
    cur = connection.cursor()
    # Get the top 3 most similar documents using the KNN <=> operator
    cur.execute("SELECT table_of_content, name, practice_exercises, github_link FROM embeddings ORDER BY embedding <=> %s LIMIT 3", (embedding_array,))
    top3_docs = cur.fetchall()
    return top3_docs
