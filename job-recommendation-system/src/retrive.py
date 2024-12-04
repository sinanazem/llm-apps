import numpy as np
from pgvector.psycopg2 import register_vector
from src.utils import get_embeddings


#Helper function: Get top 3 most similar documents from the database
def get_top3_similar_docs(query, conn):
    query_embedding = get_embeddings(query)
    embedding_array = np.array(query_embedding)
    # Register pgvector extension
    register_vector(conn)
    cur = conn.cursor()
    # Get the top 3 most similar documents using the KNN <=> operator
    cur.execute("SELECT * FROM embeddings ORDER BY embedding <=> %s LIMIT 9", (embedding_array,))
    top3_docs = cur.fetchall()
    return top3_docs


