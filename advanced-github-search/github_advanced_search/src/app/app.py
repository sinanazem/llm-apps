import streamlit as st
import yaml
import os
import psycopg2
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

import openai
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from streamlit_card import card
from src.llm import process_input_with_retrieval
from src.retrival import get_embeddings, get_top3_similar_docs

from dotenv import load_dotenv
load_dotenv()

# Database connection configuration
DB_CONFIG = {
    'dbname': os.getenv("DB_NAME", "postgres"),
    'user': os.getenv("DB_USER", "postgres"),
    'password': os.getenv("DB_PASSWORD", "mypass"),
    'host': os.getenv("DB_HOST", "localhost"),
    'port': os.getenv("DB_PORT", "5432"),
}

connection = psycopg2.connect(**DB_CONFIG)

with st.sidebar:

    # session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content="Hello, I am a bot. How can I help you?"),
        ]

    history = st.container(height=730)
    user_query = st.chat_input("Type your message here...")
    # conversation
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with history.chat_message("AI"):
                st.write(message.content)
        elif isinstance(message, HumanMessage):
            with history.chat_message("Human"):
                st.write(message.content)

    
    if user_query is not None and user_query != "":
        st.session_state.chat_history.append(HumanMessage(content=user_query))

        with history.chat_message("Human"):
            st.markdown(user_query)

        with history.chat_message("AI"):
            response = process_input_with_retrieval(user_query, connection)
            st.write(response)

        st.session_state.chat_history.append(AIMessage(content=response))
        

st.markdown("## Github Advanced Search Engine")
st.image("https://instawpcom.b-cdn.net/wp-content/uploads/2024/07/banner-772x250-22.webp")
search = st.text_input("")
search_button = st.button("search")

if search_button:
    query_embeddings = get_embeddings(search)
    top3 = get_top3_similar_docs(query_embeddings, connection)
    st.write(top3)


# if search_button:
#         col1 ,col2, col3= st.columns(3)
#         with col1:
#             res = card(
#                 title="Streamlit Card",
#                 text="This is a test card",
#                 image="https://media.graphassets.com/RwSaeleSmaBApIsBwsuS",
#                 styles={
#                     "card": {
#                         "width": "185px",
#                         "height": "250px",
#                         "border-radius": "30px",
#                         "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
#                     },
#                     "text": {
#                         "font-family": "serif",
#                     }
#                 }
#             )
            
#         with col2:
#             res = card(
#                 title="Stamlit Card",
#                 text="This is a t card",
#                 image="https://placekitten.com/500/500",
#                 styles={
#                     "card": {
#                         "width": "185px",
#                         "height": "250px",
#                         "border-radius": "30px",
#                         "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
#                     },
#                     "text": {
#                         "font-family": "serif",
#                     }
#                 }
#             )
            
#         with col3:
#             res = card(
#                 title="Streamlit rd",
#                 text="s a test card",
#                 image="https://placekitten.com/500/500",
#                 styles={
#                     "card": {
#                         "width": "185px",
#                         "height": "250px",
#                         "border-radius": "30px",
#                         "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
#                     },
#                     "text": {
#                         "font-family": "serif",
#                     }
#                 }
#             )