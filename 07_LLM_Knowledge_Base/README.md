# Module 7: LLM-Based Knowledge Bases with Streamlit

**A Learning Guide by Hussein Daoud** ([https://github.com/hussein-da](https://github.com/hussein-da))

This module demonstrates how to build an interactive knowledge base application using a Large Language Model (LLM) like GPT and a user-friendly web interface created with Streamlit.

## 🚀 Introduction: Conversational Knowledge Access

Traditional knowledge bases often rely on keyword search or navigating complex hierarchies. LLMs offer a more natural way to interact with information – users can ask questions in plain language, and the LLM can synthesize answers based on the underlying knowledge documents.

This approach involves providing the LLM with relevant context from the knowledge base alongside the user's query. The LLM then acts as a reasoning engine to formulate an answer grounded in the provided information.

**Benefits:**

*   **Natural Language Interaction:** Users can ask questions conversationally.
*   **Synthesized Answers:** LLMs can combine information from multiple parts of the knowledge base to provide comprehensive answers.
*   **Contextual Understanding:** LLMs can often understand the intent behind a query better than simple keyword matching.
*   **Rapid UI Development:** Streamlit allows for quick creation of interactive web interfaces for AI applications.

**Challenges:**

*   **Context Window Limits:** LLMs have limits on the amount of text (context) they can process at once. Strategies are needed to select relevant parts of the knowledge base.
*   **Hallucination:** Ensuring the LLM answers *only* based on the provided context and doesn't invent information.
*   **Cost:** API calls to powerful LLMs can incur costs.
*   **Knowledge Update:** Keeping the knowledge base content up-to-date.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

*   Understand how LLMs can power interactive knowledge bases.
*   Build a simple web application using Streamlit.
*   Load and process text content to serve as a knowledge base.
*   Integrate an LLM API (OpenAI GPT) into a Streamlit application.
*   Construct prompts that instruct the LLM to answer questions based on provided context.
*   Containerize the Streamlit application using Docker.

## 🛠️ Module Structure: Interactive FAQ App

We will build a simple Streamlit application (`kb_app`) that allows users to ask questions against a predefined text-based knowledge base (`kb_content.md`).

```
07_LLM_Knowledge_Base/
│
├── README.md           # This file: Introduction & Setup Instructions
│
└── kb_app/
    ├── app.py          # Streamlit application code
    ├── requirements.txt # Python dependencies for the app
    ├── Dockerfile      # Dockerfile for containerizing the app
    ├── data/
    │   └── kb_content.md # Sample knowledge base content
    └── .env.example    # Example for OpenAI API Key
```

## 📚 Prerequisites

*   Python 3.8 or higher.
*   Basic understanding of LLMs and APIs (OpenAI).
*   An OpenAI API key.
*   Familiarity with Streamlit (or willingness to learn from the example).
*   Docker installed.
*   Understanding of virtual environments and `pip`.

## ⚙️ Setup & Usage

Follow these steps to set up and run the interactive knowledge base application.

### 1. Navigate to the App Directory

Open your terminal and change into the `kb_app` directory:
```bash
cd 07_LLM_Knowledge_Base/kb_app
```

### 2. Set Up Python Environment & Install Dependencies

Create and activate a virtual environment (recommended):
```bash
# Create virtual environment
python -m venv venv_kb

# Activate it
# On macOS/Linux: source venv_kb/bin/activate
# On Windows: venv_kb\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 3. Set Up OpenAI API Key

*   Since `.env.example` creation might be blocked, manually create a file named `.env` in the `07_LLM_Knowledge_Base/kb_app/` directory.
*   Add your OpenAI API key to this file:
    ```env
    OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ```
    Replace the placeholder with your actual key.

### 4. Prepare Knowledge Base Content

*   The application reads knowledge from `data/kb_content.md`.
*   You can modify or replace this file with your own Markdown-formatted text content.
*   For the current simple implementation (which sends the whole text as context), keep the content relatively concise (e.g., under a few thousand words) to avoid exceeding LLM context limits or incurring high costs.

### 5. Running the App Directly with Streamlit

Ensure your virtual environment is activated and you are in the `kb_app` directory.

```bash
streamlit run app.py
```
Streamlit will start the application, and you can access it in your web browser (usually at `http://localhost:8501`).

### 6. Building and Running with Docker

Make sure Docker is running.

1.  **Build the Image:** From the `07_LLM_Knowledge_Base/kb_app/` directory:
    ```bash
docker build -t llm-knowledge-base .
    ```
2.  **Run the Container:**
    ```bash
docker run -p 8501:8501 --rm --env-file .env llm-knowledge-base
    ```
    *   `-p 8501:8501`: Maps your host port 8501 to the container's port 8501.
    *   `--rm`: Removes the container when it stops.
    *   `--env-file .env`: Passes the environment variables (including your `OPENAI_API_KEY`) from your local `.env` file to the container.
    *   `llm-knowledge-base`: The name you tagged the image with.

    You can then access the application in your browser at `http://localhost:8501`.

### 7. Interacting with the Knowledge Base

*   Once the app is running (either via Streamlit directly or Docker), open the web interface.
*   You can optionally expand the section to view the loaded knowledge base content.
*   Type a question related to the content in the `kb_content.md` file into the text input box.
*   The app will send your question along with the knowledge base context to the OpenAI API.
*   The LLM's answer, based on the provided context, will be displayed.

---

This completes the setup and usage guide for the LLM-based knowledge base application! 