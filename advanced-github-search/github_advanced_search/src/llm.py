import openai
from src.retrival import get_top3_similar_docs, get_embeddings


# Helper function: get text completion from OpenAI API
# Note we're using the latest gpt-3.5-turbo-0613 model
def get_completion_from_messages(messages, model="gpt-4o", temperature=0, max_tokens=1000):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, 
        max_tokens=max_tokens, 
    )
    return response.choices[0].message["content"]


# Function to process input with retrieval of most similar documents from the database
def process_input_with_retrieval(user_input, connection):
    delimiter = "```"
    #Step 1: Get documents related to the user input from database
    related_docs = get_top3_similar_docs(get_embeddings(user_input), connection)
    #print(related_docs)
    # Step 2: Get completion from OpenAI API
    # Set system message to help set appropriate tone and context for model
    system_message = f"""
    You are a friendly Pytopia chatbot. \
    You can answer questions about Pytopia Python Programming Course Notebook and Github Repository, its features and its use cases. \
    You respond in a concise, technically credible tone. \
    """
    # Prepare messages to pass to model
    # We use a delimiter to help the model understand the where the user_input starts and ends
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"{delimiter}{user_input}{delimiter}"},
        {"role": "assistant", "content": f"Relevant Pytopia Python Programming Course Notebooks and GitHub repository information: \n {related_docs[0][0]} \n {related_docs[1][0]} {related_docs[2][0]}"}
    ]
    final_response = get_completion_from_messages(messages)
    return final_response