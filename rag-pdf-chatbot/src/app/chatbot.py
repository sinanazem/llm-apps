import streamlit as st
import json
from streamlit_lottie import st_lottie
from utils import call_llama
from src.chatbot import PDFChatbot

st.set_page_config(
    page_title='Ollama Chatbot',
    page_icon="🤖",
    layout='centered',
    initial_sidebar_state='collapsed'
    )


col11, col22 = st.columns(2)
with col11:
    st.header("📚 Upload PDF file")
    st.markdown("")
    st.write(""" 
    Meet Llama2,
    that transforms ideas into captivating
    content effortlessly.\n
    """)
    
    
    
with col22:
    
    st.image("/mnt/c/Users/user/OneDrive/Desktop/rag-pdf-chatbot/img/Upload-pana.png")
st.file_uploader(label="Upload File:")
st.markdown("<hr>", unsafe_allow_html=True)




@st.cache_data
def load_lottiefile(filepath: str):
    with open(filepath,"r") as f:
        return json.load(f)

col1, col2 = st.columns(2)
with col2:
    st.header("🦙LLAma2 Chatbot")
    st.markdown("")
    st.write(""" 
    Meet Llama2,
    that transforms ideas into captivating
    content effortlessly.\n
    """)
    
with col1:
    
    lottie11 = load_lottiefile("/mnt/c/Users/user/OneDrive/Desktop/rag-pdf-chatbot/src/app/animations/Animation_llama.json")
    st_lottie(lottie11,key='locMainImage', height=200, width=200)

st.markdown("<hr>", unsafe_allow_html=True)


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
if prompt := st.chat_input():
   
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    print(st.session_state.messages)
    # response = call_llama(model="llama3", prompt=st.session_state.messages[-1]['content'])
    # msg = response['response']
    local_path = "/mnt/c/Users/user/OneDrive/Desktop/rag-pdf-chatbot/data/WEF_The_Global_Cooperation_Barometer_2024.pdf"
    
    if not local_path:
        print("Upload a PDF file")
    
    chatbot = PDFChatbot(local_path=local_path, model="phi3")
    data = chatbot.load_pdf()
    chunks = chatbot.split_text(data)
    chatbot.create_vector_db(chunks)
    chatbot.setup_chain()
    
    response = chatbot.query_chain(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)