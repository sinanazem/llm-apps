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
