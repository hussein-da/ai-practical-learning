# Module 1: Retrieval-Augmented Generation (RAG) - FAQ Chatbot

**A Learning Guide by Hussein Daoud** ([https://github.com/hussein-da](https://github.com/hussein-da))

This project is part of a comprehensive collection of learning modules designed to explore various AI concepts and implementations. This specific module focuses on building a Retrieval-Augmented Generation (RAG) based FAQ chatbot.

We encourage you to explore, experiment, and adapt the code for your own learning and projects. Feedback and contributions are welcome!

## 🚀 Introduction

This module will guide you through the process of building an FAQ (Frequently Asked Questions) chatbot using Retrieval-Augmented Generation (RAG). RAG combines the power of large language models (LLMs) with external knowledge retrieval to provide more accurate and contextually relevant answers. We will be utilizing LangChain and OpenAI APIs to build this chatbot.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

*   Understand the core concepts of Retrieval-Augmented Generation.
*   Set up a vector store for efficient similarity search of FAQ data (using FAISS).
*   Integrate LangChain for orchestrating the RAG pipeline.
*   Utilize OpenAI embeddings for embedding text.
*   Connect to OpenAI's API (specifically `ChatOpenAI`) for the generative component.
*   Build a simple command-line interface to interact with the FAQ chatbot.
*   Structure a RAG project for clarity and scalability.
*   Containerize the application using Docker.

## 🛠️ Project Structure

```
01_RAG_FAQ_Chatbot/
│
├── data/
│   └── faq.csv         # Example FAQ data
├── rag_chatbot.py      # Main application script for the chatbot
├── requirements.txt    # Python dependencies
├── Dockerfile          # Dockerfile for containerization
├── env.example.txt     # Example environment file for API keys
└── README.md           # This file
```

## 📚 Prerequisites

*   Python 3.8 or higher.
*   Basic understanding of Large Language Models (LLMs).
*   Familiarity with APIs (specifically OpenAI).
*   An OpenAI API key.
*   Docker installed if you wish to containerize the application.

## ⚙️ Setup and Installation

1.  **Navigate to this module's directory:**
    ```bash
    cd 01_RAG_FAQ_Chatbot
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On macOS/Linux:
    source venv/bin/activate
    # On Windows:
    # venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your OpenAI API Key:**
    *   In the `01_RAG_FAQ_Chatbot/` directory, you will find a file named `env.example.txt`.
    *   Create a copy of this file and name it `.env`:
        ```bash
        cp env.example.txt .env
        ```
    *   Open the `.env` file with a text editor. Replace `"YOUR_OPENAI_API_KEY_HERE"` with your actual OpenAI API key:
        ```env
        OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        ```
    *   The `rag_chatbot.py` script is configured to load this key from the `.env` file. **This file must be present in the `01_RAG_FAQ_Chatbot/` directory when running the script or the Docker container locally.**

## 📖 Usage Instructions

There are two primary ways to run the RAG FAQ Chatbot: directly via Python or using Docker.

### 1. Running Directly with Python

Ensure you have completed all steps in the "Setup and Installation" section, especially activating your virtual environment and creating the `.env` file with your API key.

1.  **Navigate to the module directory (if not already there):**
    ```bash
    cd path/to/your/projects/ai-practical-learning/01_RAG_FAQ_Chatbot
    ```

2.  **Confirm your FAQ data:**
    *   The chatbot is configured to load FAQ data from `data/faq.csv`.
    *   This CSV file must contain "Question" and "Answer" columns. An example is provided.

3.  **Run the chatbot application:**
    Execute the Python script from the `01_RAG_FAQ_Chatbot` directory:
    ```bash
    python rag_chatbot.py
    ```

4.  **Interact with the chatbot:**
    *   Upon successful initialization (you'll see messages about loading data, creating the vector store, etc.), a prompt `Your Question:` will appear.
    *   Type your question and press Enter.
    *   The chatbot will display the generated answer and the source FAQs it retrieved.
    *   To exit, type `exit` or `quit` and press Enter.

### 2. Running with Docker

This method uses the `Dockerfile` to build a container image for the chatbot. Docker must be installed and running.

1.  **Navigate to the module directory:**
    Ensure your terminal is in the `01_RAG_FAQ_Chatbot` directory (where the `Dockerfile` and your `.env` file are located).
    ```bash
    cd path/to/your/projects/ai-practical-learning/01_RAG_FAQ_Chatbot
    ```

2.  **Ensure your `.env` file is ready:**
    *   The `.env` file (containing your `OPENAI_API_KEY`, created in "Setup and Installation" step 4) must be present in the current directory.

3.  **Build the Docker image:**
    Execute the following command to build the image. We'll tag it as `rag-faq-chatbot`:
    ```bash
    docker build -t rag-faq-chatbot .
    ```

4.  **Run the Docker container:**
    After the image is built, run it. You need to provide the `OPENAI_API_KEY` to the application inside the container. The recommended way for local development is using the `--env-file` option:

    ```bash
    docker run -it --rm --env-file .env rag-faq-chatbot
    ```
    *   `-it`: Runs the container in interactive mode (so you can type questions) and allocates a pseudo-TTY.
    *   `--rm`: Automatically removes the container when it exits.
    *   `--env-file .env`: Passes the environment variables defined in your local `.env` file to the container.

    *(Alternative for providing the API key, if `--env-file` is not preferred: You could mount the .env file using `-v "$(pwd)/.env:/app/.env"` on Linux/macOS or `-v "${PWD}/.env:/app/.env"` on PowerShell, or pass the variable directly with `-e OPENAI_API_KEY="your_key"` though this is less secure if the key appears in shell history.)*

5.  **Interact with the chatbot:**
    *   The chatbot will start inside the container, and you'll see the `Your Question:` prompt.
    *   Type `exit` or `quit` to stop the chatbot and the container (due to `--rm`).

## 💡 Key Concepts

*   **Retrieval-Augmented Generation (RAG):**
    *   **Retriever:** Fetches relevant documents/passages (in our case, FAQs) from a knowledge base using vector similarity search.
    *   **Generator:** Employs an LLM (like `gpt-3.5-turbo`) to synthesize an answer based on both the retrieved context and the user's original query.
*   **Vector Embeddings:** Dense numerical representations of text (created by `OpenAIEmbeddings`) that capture semantic meaning, allowing for similarity comparisons.
*   **Vector Stores:** Specialized databases (like `FAISS`) designed for efficient storage and retrieval of vector embeddings.
*   **LangChain:** A comprehensive framework used here to chain together the components: loading data, creating embeddings, vector storage, retrieval, and generation with an LLM.
*   **Prompt Engineering:** Crafting effective prompts (like our `QA_CHAIN_PROMPT`) to guide the LLM in generating the desired output based on the retrieved context.

## 📜 Code Implementation (`rag_chatbot.py`)

*(A brief overview of the script's structure will be added here. The code itself is commented to explain each step.)*

*   **Imports:** Necessary libraries from LangChain, OpenAI, Pandas, etc.
*   **Configuration:** Defines paths for data and environment files.
*   **`load_api_key()`:** Loads the `OPENAI_API_KEY` from the `.env` file.
*   **`load_faqs()`:** Reads Q&A pairs from the `data/faq.csv` file using Pandas.
*   **`create_vector_store()`:** 
    *   Initializes `OpenAIEmbeddings`.
    *   Creates LangChain `Document` objects from the FAQs (embedding questions, storing answers in metadata).
    *   Builds a `FAISS` vector store from these documents and their embeddings.
*   **`initialize_qa_chain()`:**
    *   Initializes `ChatOpenAI` (e.g., `gpt-3.5-turbo`).
    *   Defines a custom `PromptTemplate` to instruct the LLM on how to use the retrieved context.
    *   Creates a `RetrievalQA` chain, linking the LLM, the FAISS retriever, and the custom prompt.
*   **`ask_question()`:** Provides a command-line loop for user interaction, takes input, queries the QA chain, and prints the results (answer and source documents).
*   **`main()`:** Orchestrates the setup (API key, FAQs, vector store, QA chain) and starts the interaction loop.

## 🐳 Docker (`Dockerfile`)

The `Dockerfile` facilitates containerizing the RAG FAQ Chatbot for consistent execution and easier deployment.

**Key Dockerfile Instructions:**

*   `FROM python:3.9-slim`: Uses a lightweight Python 3.9 image.
*   `WORKDIR /app`: Sets the working directory inside the container.
*   `COPY requirements.txt .` and `RUN pip install --no-cache-dir -r requirements.txt`: Copies and installs dependencies.
*   `COPY rag_chatbot.py .`, `COPY data/ ./data/`, `COPY env.example.txt .`: Copies the application script, data, and example environment file into the image.
*   `ENV PYTHONIOENCODING=UTF-8 LANG=C.UTF-8`: Sets recommended environment variables for Python string handling.
*   `CMD ["python", "rag_chatbot.py"]`: Specifies the default command to run when the container starts.

For build and run commands, refer to the "Usage Instructions > Running with Docker" section.

## 🙏 Acknowledgements

*   The LangChain project and its contributors for the powerful framework.
*   OpenAI for their advanced language models and embedding APIs.
*   The FAISS library for efficient similarity search.
*   The broader open-source AI/ML community.

---

Happy Learning!
If you have any questions or suggestions, feel free to reach out or open an issue/pull request once this is part of the main repository. Creating an issue is a great way to provide feedback or ask for clarification. 