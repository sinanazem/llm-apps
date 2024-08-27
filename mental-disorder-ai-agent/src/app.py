import streamlit as st
from langchain.memory import ConversationBufferMemory


st.title("Build an autonomous Agents: everything-about-book")

# initialize memory
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(memory_key="chat_history")
    
question = st.chat_input("Ask me any question...")

if question:
    with st.chat_message("Human"):
        st.markdown(question)
        
    assistance_response = "I don't know!"
    with st.chat_message("AI"):
        st.markdown(assistance_response)