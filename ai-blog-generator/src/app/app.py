import streamlit as st
import time
import json
import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
from langchain.chains import LLMChain


# Intro ------------------------------------------------------------------
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
    lottie11 = load_lottiefile("/mnt/c/Users/user/OneDrive/Desktop/ai-blog-sn-20240108/src/app/animations/Animation-4.json")
    st_lottie(lottie11,key='locMainImage', height=300, width=300)

st.markdown("<hr>", unsafe_allow_html=True)

# Model ------------------------------------------------------------------
from langchain.prompts import PromptTemplate
from langchain.llms.ctransformers import CTransformers

# function to get tesponse from llama model
def get_llama_response(input_text, number_words, blog_style):
    
    # load LLAma2 model
    llm = CTransformers(model="/mnt/c/Users/user/OneDrive/Desktop/ai-blog-sn-20240108/models/llama-2-7b.ggmlv3.q8_0.bin",
                       model_type="llama",
                       config={"max_new_tokens":256, "temperature":0.01})
    
    # Prompt Template
    template = """
    
    Write a blog for {blog_style} job profile for a topic {input_text}
    within {number_words} words.
    
    
    """
    prompt = PromptTemplate(input_variables=["input_text", "number_words", "blog_style"], template=template)
    
    # generate the response from llama2 model
    
    llm_chain = LLMChain(prompt=prompt, llm=llm)

    response = llm_chain.run("What is AI?")
    
    return response
    


input_text = st.text_input(label='Enter the blpg Topic ')

col3, col4 = st.columns(2)

with col3:
    number_words = st.text_input(label="number of words: ")
with col4:
    blog_style = st.selectbox("Writing the Blog for ...", ["Data Scientists", "Data Engineers", "BI Analysts"], index=0)


submit = st.button("Generate")

if submit:
    st.write(get_llama_response(input_text, number_words, blog_style))
    