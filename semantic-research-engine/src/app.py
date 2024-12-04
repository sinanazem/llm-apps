import uuid
import os
import posthog
import streamlit as st
from langchain.chains import LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate



from langchain.chat_models.ollama import ChatOllama
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
load_dotenv()

# def task(distinct_id, input, output, event="llm-task", timestamp=None, session_id=None, properties=None):
#     props = properties if properties else {}
#     props["$llm_input"] = input
#     props["$llm_output"] = output

#     if session_id:
#         props["$session_id"] = session_id

#     posthog.capture(
#         distinct_id=distinct_id, event=event, properties=props, timestamp=timestamp, disable_geoip=False
#     )


# def predict(message):
#     response = chain.invoke({"input": message})
#     return response["response"]

# try:
#     posthog.api_key = os.environ["POSTHOG_API_KEY"]
#     posthog.host = os.environ['POSTHOG_HOST']
# except KeyError:
#     raise ValueError("Please set POSTHOG_API_KEY and POSTHOG_HOST environment variables")

# model_name = "llama3:latest"
# llm = ChatOllama(temperature=0.0, model=model_name)
# memory = ConversationBufferMemory()


# template = """Question: {question}

# Answer: Let's think step by step."""

# prompt = ChatPromptTemplate.from_template(template)


# chain = ConversationChain(llm=llm, memory=memory, verbose=True)



# st.title(f"Ollama model: {model_name}")

# if "messages" not in st.session_state or "session_id" not in st.session_state:
#     st.session_state.messages = []
#     st.session_state.session_id = uuid.uuid4().hex
#     st.session_state.user_id = uuid.uuid4().hex


# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# if prompt := st.chat_input("Type here..."):
#     st.chat_message("user").markdown(prompt)
#     st.session_state.messages.append({"role": "user", "content": prompt})

#     response = predict(prompt)

#     with st.chat_message("assistant"):
#         st.markdown(response)

#     st.session_state.messages.append({"role": "assistant", "content": response})

#     task(
#         distinct_id=st.session_state.user_id,
#         input=prompt,
#         output=response,
#         event="llm-task",
#         session_id=st.session_state.session_id,
#         properties={"model": model_name},
#     )

# if __name__ == '__main__':
#     print(chain.invoke({"question": "What is Python?"}))

from langchain.memory.buffer import ConversationBufferMemory

conversation_memory = ConversationBufferMemory(
    memory_key="chat_history",
    max_len=50,
    return_messages=True,
    )


from langchain.prompts import PromptTemplate

ice_cream_assistant_template = """
You are an ice cream assistant chatbot named "Scoopsie". Your expertise is 
exclusively in providing information and advice about anything related to 
ice creams. This includes flavor combinations, ice cream recipes, and general
ice cream-related queries. You do not provide information outside of this 
scope. If a question is not about ice cream, respond with, "I specialize 
only in ice cream related queries."
Chat History: {chat_history}
Question: {question}
Answer:"""

ice_cream_assistant_prompt_template = PromptTemplate(
    input_variables=["chat_history", "question"],
    template=ice_cream_assistant_template
)

import chainlit as cl

@cl.on_chat_start
def quey_llm():
    model_name = "llama3:latest"
    llm = ChatOllama(temperature=0.0, model=model_name)
    
    conversation_memory = ConversationBufferMemory(memory_key="chat_history",
                                                   max_len=50,
                                                   return_messages=True,
                                                   )
    
    # llm_chain = prompt | ollama_llm
    llm_chain = ConversationChain(llm=llm, memory=conversation_memory, verbose=True)
    # llm_chain = LLMChain(llm=llm, 
    #                      prompt=ice_cream_assistant_prompt_template,
    #                      memory=conversation_memory)
    
    cl.user_session.set("llm_chain", llm_chain)
    
@cl.on_message
async def query_llm(message: cl.Message):
    llm_chain = cl.user_session.get("llm_chain")
    
    response = await llm_chain.acall(message.content, 
                                     callbacks=[
                                         cl.AsyncLangchainCallbackHandler()])
    
    await cl.Message(response["text"]).send()