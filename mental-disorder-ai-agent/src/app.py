import streamlit as st
import time
import json
import streamlit as st
# from streamlit_lottie import st_lottie
# from streamlit_option_menu import option_menu
from langchain.chains import LLMChain

from agent import get_agent_response


# Intro ------------------------------------------------------------------
st.set_page_config(
    page_title='Generate blogs',
    page_icon="🤖",
    layout='centered',
    initial_sidebar_state='collapsed'
    )

# @st.cache_data
# def load_lottiefile(filepath: str):
#     with open(filepath,"r") as f:
#         return json.load(f)

col1, col2 = st.columns(2)
with col1:
    st.header("AI Blog Generator")
    st.markdown("")
    st.write(""" 
    Meet Llama2, the AI Blog Generator
    that transforms ideas into captivating
    content effortlessly.\n
    Powered by a pre-trained model,
    Llama2 delivers high-quality,
    customizable blog posts in seconds.
    """)
    
with col2:
    # lottie11 = load_lottiefile("/mnt/c/Users/user/OneDrive/Desktop/ai-blog-sn-20240108/src/app/animations/Animation-4.json")
    # st_lottie(lottie11,key='locMainImage', height=300, width=300)
    st.write("aaa")

st.markdown("<hr>", unsafe_allow_html=True)

# Model ------------------------------------------------------------------
from langchain.prompts import PromptTemplate
from langchain.llms.ctransformers import CTransformers

# function to get tesponse from llama model


input_text = st.text_input(label='Enter the blpg Topic ')


submit = st.button("Generate")

if submit:
    st.write(get_agent_response(input_text))