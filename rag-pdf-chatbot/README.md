# RAG PDF Chatbot
<div>
    <img src="https://github.com/sinanazem/rag-pdf-chatbot/blob/main/img/Chat%20bot-cuate.png"  width="300" align="left" hspace="10">
    
Welcome to the RAG PDF Chatbot repository!<br><br>
This project demonstrates how to build a chatbot capable of interacting with PDF documents using Retrieval-Augmented Generation (RAG).<br><br>
The chatbot leverages LangChain, Streamlit, MongoDB, and Docker to provide an interactive and efficient user experience.
</div>
<br><br><br><br>

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)

## Features

- **PDF Document Interaction**: Upload and interact with PDF documents.
- **Retrieval-Augmented Generation**: Combines document retrieval with language generation for accurate responses.
- **User-Friendly Interface**: Built with Streamlit for an easy-to-use web interface.
- **Scalable Data Storage**: Utilizes MongoDB for efficient data storage and retrieval.
- **Containerized Deployment**: Easily deploy the application using Docker.

## Installation

To get started with the RAG PDF Chatbot, follow these steps:

### Local Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/sinanazem/rag-pdf-chatbot.git
    cd rag-pdf-chatbot
    ```

2. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Set up MongoDB**:
    - Ensure you have a running instance of MongoDB.
    - Update the MongoDB connection string in the configuration file.

### Docker Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/sinanazem/rag-pdf-chatbot.git
    cd rag-pdf-chatbot
    ```

2. **Build the Docker image**:
    ```sh
    docker build -t rag-pdf-chatbot .
    ```

3. **Run the Docker container**:
    ```sh
    docker run -d -p 8501:8501 --name rag-pdf-chatbot rag-pdf-chatbot
    ```

## Usage

### Local Usage

To run the chatbot locally, execute the following command:

```sh
streamlit run app.py
```

This will start a Streamlit server, and you can interact with the chatbot through your web browser at `http://localhost:8501`.

### Docker Usage

To run the chatbot using Docker, ensure the container is running (see Docker Installation). Access the chatbot through your web browser at `http://localhost:8501`.

