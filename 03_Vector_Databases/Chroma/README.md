# Using Chroma DB for Semantic Search

**A Learning Guide by Hussein Daoud** ([https://github.com/hussein-da](https://github.com/hussein-da))

This part of Module 3 introduces **Chroma DB**, an open-source embedding database focused on simplicity and developer productivity. It makes it easy to build AI applications with semantic search capabilities directly within your Python environment or as a lightweight server.

## 🚀 Introduction to Chroma DB

Chroma is designed to be "just work" for developers. It can run in-memory (great for quick experiments and notebooks), persist data to disk, or be run as a client-server application.

**Key Features of Chroma DB:**

*   **Open Source:** Actively developed and community-driven.
*   **Python-Native:** Designed with Python developers in mind, offering a very intuitive client API.
*   **Multiple Running Modes:**
    *   **In-memory:** Transient storage, good for testing and development.
    *   **Persistent:** Saves data to disk for durability.
    *   **Client/Server:** Run Chroma as a separate server and connect from multiple clients.
*   **Automatic Embedding Generation (Optional):** Can integrate with embedding functions (like Sentence Transformers or OpenAI) directly, simplifying the process of adding documents.
*   **Metadata Filtering:** Supports filtering search results based on metadata associated with embeddings.
*   **LangChain Integration:** Popular in the LangChain ecosystem as a vector store.

## 🎯 Learning Objectives

*   Understand how to install and set up Chroma DB.
*   Use Chroma in its different modes: in-memory and persistent.
*   Create collections and add documents (with Chroma handling embeddings or providing them manually).
*   Perform similarity searches (queries) with and without metadata filters.
*   Understand how Chroma manages data and embeddings.

## 🛠️ Project Structure

```
Chroma/
│
├── README.md           # This file
├── example_chroma.py   # Python script demonstrating Chroma DB usage
├── requirements.txt    # Python dependencies for this example
└── data/               # Optional: Directory for sample data
    └── sample_text.csv # Example text data to embed and index
```

## 📚 Prerequisites

*   Python 3.8 or higher.
*   An OpenAI API key if you choose to use OpenAI for generating embeddings (or Chroma can use its default Sentence Transformers model).
*   Basic understanding of vector embeddings.

## ⚙️ Setup and Installation

1.  **Set up your Python Environment:**
    *   Create and activate a virtual environment:
        ```bash
        python -m venv chroma_env
        source chroma_env/bin/activate # On Windows: chroma_env\Scripts\activate
        ```
    *   Install the necessary libraries from this directory:
        ```bash
        pip install -r requirements.txt
        ```

2.  **Environment Variables for `example_chroma.py`:**
    *   Create a `.env` file in this `Chroma/` directory.
    *   If you plan to use OpenAI embeddings with Chroma, add your API key:
        ```env
        OPENAI_API_KEY="YOUR_OPENAI_API_KEY" # Required if using OpenAIEmbeddingFunction
        CHROMA_COLLECTION_NAME="semantic_search_chroma"
        # For persistent storage, you can specify a path:
        CHROMA_PERSIST_PATH="./chroma_db_storage" 
        ```
    *If `CHROMA_PERSIST_PATH` is set, the example script will try to use persistent storage. Otherwise, it will run in-memory.*

## 📖 Usage (Conceptual Steps for `example_chroma.py`)

The `example_chroma.py` script will demonstrate:

1.  **Client Initialization:** Creating a Chroma client (either in-memory or persistent).
2.  **Embedding Function Setup:** Configuring an embedding function (Chroma's default, Sentence Transformers, or OpenAI).
3.  **Collection Creation/Loading:** Getting or creating a collection, associating it with an embedding function.
4.  **Adding Documents:** Ingesting documents (texts with metadata and unique IDs) into the collection. Chroma can automatically embed these texts using the specified function.
5.  **Querying:** Performing similarity searches using query texts, with options for metadata filtering (`where` clauses).

## 💡 Key Chroma Concepts

*   **Client:** The main entry point to interact with Chroma.
*   **Collection:** A named group of documents, their embeddings, and metadata.
*   **Embedding Function:** A function that Chroma uses to convert documents into vector embeddings. Chroma provides defaults (e.g., Sentence Transformers) and allows custom ones (e.g., OpenAIEmbeddingsFunction).
*   **Documents:** The raw text content you want to store and search.
*   **Metadatas:** A list of dictionaries containing metadata associated with each document.
*   **IDs:** A list of unique identifiers for each document.
*   **`add()` method:** Used to add documents, metadatas, and ids to a collection. Embeddings are generated automatically if not provided.
*   **`query()` method:** Used to search the collection with query texts, returning similar documents.
*   **`where` filter:** A dictionary used in `query()` to filter results based on metadata (e.g., `{"category": "technology"}`).
*   **`where_document` filter:** A dictionary used in `query()` to filter based on the content of the documents themselves (e.g., using `$contains`).

---

Explore `example_chroma.py` to see these concepts in action. Remember to set up your `.env` file if you intend to use OpenAI embeddings or specify a persistent storage path. 