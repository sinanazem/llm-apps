import streamlit as st

import streamlit as st
import json
from streamlit_lottie import st_lottie
from utils import call_llama

st.set_page_config(
    page_title='Generate blogs',
    page_icon="🤖",
    layout='centered',
    initial_sidebar_state='collapsed'
    )


@st.cache_data
def load_lottiefile(filepath: str):
    with open(filepath,"r") as f:
        return json.load(f)

col1, col2 = st.columns(2)
with col1:
    st.header("AI Blog Genrator")
    st.markdown("")
    st.write(""" 
    Meet Llama2,
    that transforms ideas into captivating
    content effortlessly.\n
    with this app you can add blog that ai generate it!
    """)
    
with col2:
    
    lottie11 = load_lottiefile("/mnt/c/Users/user/OneDrive/Desktop/llm-apps/ollama-blog-generator/src/app/animations/Animation-blog.json")
    st_lottie(lottie11,key='locMainImage', height=200, width=200)

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown("### Connect to PostgreSQL: ")

col3, col4 = st.columns(2)
with col3:
    username = st.text_input("**username:** ")
with col4:
    password = st.text_input("**password:** ", type="password")

col5, col6, col7 = st.columns(3)

with col5:
    host = st.text_input("**Host:** ")
with col6:
    port = st.text_input("**Port:** ")
with col7:
    db_name = st.text_input("**Database Name:** ")

btn = st.button("Connect")
if btn:
    st.success("You are connected!")
