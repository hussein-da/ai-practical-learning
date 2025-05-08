# AI Practical Learning Modules

**A Comprehensive Learning Repository by Hussein Daoud** ([https://github.com/hussein-da](https://github.com/hussein-da))

Welcome! This repository offers a collection of 15 hands-on and conceptual learning modules designed to cover a wide spectrum of Artificial Intelligence topics, from foundational concepts to advanced architectures and deployment practices.

## 🎯 Project Goal

The primary goal of this project is to provide structured, practical learning materials for individuals looking to deepen their understanding and skills in various areas of AI. Each module aims to be relatively self-contained, offering explanations, code examples (where applicable), and resources to explore specific AI concepts and techniques.

## 🗂️ Module Overview

This repository is organized into the following 15 modules:

1.  **[01_RAG_FAQ_Chatbot](./01_RAG_FAQ_Chatbot/)**: Building a Retrieval-Augmented Generation (RAG) chatbot for answering questions based on a provided knowledge base (FAQ dataset). Includes Python code, Dockerfile, and setup instructions.
2.  **[02_Prompt_Engineering](./02_Prompt_Engineering/)**: Techniques for designing effective prompts to interact with large language models (LLMs) like GPT, Claude, and Gemini. Contains detailed Markdown guides and examples.
3.  **[03_Vector_Databases](./03_Vector_Databases/)**: Introduction to vector databases (Chroma, FAISS, Pinecone, Qdrant) with Python examples for efficient similarity search in AI applications.
4.  **[04_Microservices_with_AI](./04_Microservices_with_AI/)**: Creating a simple AI-powered microservice (Sentiment Analysis API) using FastAPI and Docker.
5.  **[05_Low_Code_No_Code_AI](./05_Low_Code_No_Code_AI/)**: Conceptual overview and examples of using Low-Code/No-Code platforms (Bubble.io, Zapier) to build AI-driven applications and automations.
6.  **[06_Practical_NLP_Applications](./06_Practical_NLP_Applications/)**: Hands-on Python examples of Named Entity Recognition (NER) and Text Classification using libraries like spaCy and Transformers.
7.  **[07_LLM_Knowledge_Base](./07_LLM_Knowledge_Base/)**: Building a simple knowledge base application using Streamlit and an LLM for querying content from documents. (Directory structure in place, implementation details in module README).
8.  **[08_Fine_tuning_LLMs](./08_Fine_tuning_LLMs/)**: Conceptual guide and considerations for fine-tuning smaller LLMs (e.g., Mistral models) on custom datasets for specific tasks. *(Focus on Mistral, other models like Llama not covered in detail).*
9.  **[09_Mobile_Apps_with_AI](./09_Mobile_Apps_with_AI/)**: Conceptual guide to integrating AI features into mobile applications, with a discussion on using frameworks like React Native and connecting to backend AI services.
10. **[10_Real_Time_Data_Pipelines](./10_Real_Time_Data_Pipelines/)**: Conceptual implementation of a real-time sentiment analysis pipeline using Apache Kafka and Python (e.g., with NLTK/VADER for sentiment scoring). (Directory structure in place for `kafka_tf_sentiment`).
11. **[11_AI_in_Cybersecurity](./11_AI_in_Cybersecurity/)**: Exploring applications of AI in cybersecurity, including conceptual examples for Network Intrusion Detection and Phishing URL Detection with illustrative Python snippets.
12. **[12_AI_Ethics_and_Responsible_AI](./12_AI_Ethics_and_Responsible_AI/)**: Discussing the crucial topics of AI Ethics, Bias in AI, Explainability (XAI), and Privacy in AI. This is a conceptual module with detailed readings.
13. **[13_Advanced_AI_Architectures](./13_Advanced_AI_Architectures/)**: Conceptual overview of advanced AI architectures like Transformers, Generative Adversarial Networks (GANs), Diffusion Models, and Graph Neural Networks (GNNs).
14. **[14_Deploying_AI_Models_MLOps](./14_Deploying_AI_Models_MLOps/)**: Introduction to MLOps principles, covering model packaging, containerization (with a conceptual Dockerfile example), deployment strategies, and model monitoring/retraining.
15. **[15_The_Future_of_AI_and_Next_Steps_in_Learning](./15_The_Future_of_AI_and_Next_Steps_in_Learning/)**: A look at current AI trends, potential future directions, and advice for continued learning in the field of AI.

## 📖 How to Use This Repository

1.  **Clone the repository:** `git clone https://github.com/hussein-da/ai-practical-learning.git` (Replace with your actual repo URL after creating it on GitHub)
2.  **Navigate to a Module:** Change into the directory of the module you are interested in (e.g., `cd 01_RAG_FAQ_Chatbot`).
3.  **Follow Module README:** Each module directory contains its own `README.md` file with specific instructions, prerequisites, setup steps, and explanations for that topic.
4.  **Virtual Environments:** For modules with Python code, it is highly recommended to create and activate a Python virtual environment within the module\'s directory before installing dependencies.
5.  **Install Dependencies:** Use the `requirements.txt` file provided within each relevant module to install necessary libraries: `pip install -r requirements.txt`.
6.  **Conceptual Modules:** Modules covering advanced topics, ethics, future trends, or specific conceptual guides (e.g., 05, 08, 09, 11, 12, 13, 14, 15) are primarily for learning through detailed READMEs and may contain illustrative/conceptual code rather than fully runnable, extensive applications.

## ⚙️ General Prerequisites

While specific prerequisites vary by module, a general familiarity with the following is beneficial:

*   **Python:** Basic to intermediate programming skills.
*   **Command Line/Terminal:** Basic navigation and execution of commands.
*   **Pip:** Python package manager.
*   **Git & GitHub:** Basic version control concepts.
*   **Docker & Docker Compose:** Required for modules involving containerization (e.g., 01, 04, 07, 10, conceptually in 14).
*   **Fundamental AI/ML Concepts:** A basic understanding of machine learning principles is helpful but modules aim to be accessible.

## ⚠️ Notes

*   **Conceptual vs. Code-Heavy Modules:** As indicated in the "Module Overview" and "How to Use This Repository", some modules are primarily conceptual and aim to provide understanding through detailed explanations and illustrative examples (e.g., Modules 05, 08, 09, 11, 12, 13, 14, 15). Other modules (e.g., 01, 03, 04, 06) contain more extensive, runnable code examples.
*   **API Keys:** Some modules require API keys (e.g., for OpenAI, Pinecone, or other third-party services). Remember to handle these securely and **never commit them directly** to your repository. Use environment variables or `.env` files (and ensure `.env` is added to your `.gitignore`).
*   **Work in Progress:** This repository is a comprehensive learning resource. While efforts are made for completeness, individual modules may be updated or expanded over time.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

*(Optional: Add contribution guidelines here if you wish to accept contributions.)*

---

Happy Learning! 