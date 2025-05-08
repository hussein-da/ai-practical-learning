# Pinecone Examples

This section demonstrates how to use Pinecone, a managed vector database service, for storing and searching vector embeddings.

## About Pinecone

Pinecone is a fully managed vector database that makes it easy to build high-performance vector search applications. It handles the infrastructure, scaling, and maintenance, allowing developers to focus on building their applications.

**Key Features:**

*   **Fully Managed Service:** No need to manage infrastructure.
*   **Scalability:** Designed to scale to billions of vectors.
*   **Low Latency Search:** Optimized for fast similarity searches.
*   **Metadata Filtering:** Supports storing and filtering by metadata alongside vectors.
*   **Easy-to-Use API and SDKs:** Provides client libraries for popular languages.

## Example in `example_pinecone.py`

The `example_pinecone.py` script will demonstrate:

1.  **Generating Sample Embeddings:** Using `sentence-transformers`.
2.  **Initializing Pinecone Client:** Connecting to your Pinecone project using an API key and environment.
3.  **Creating/Connecting to an Index:** Ensuring a Pinecone index exists with the correct dimension and metric.
4.  **Upserting Data:** Adding (or updating) embeddings, their IDs, and associated metadata to the index.
5.  **Performing a Similarity Search:** Querying the index with a new vector to find similar items.
6.  **Deleting an Index (Cleanup):** Showing how to delete the index after the example.

## Setup

1.  **Pinecone Account:** You need a Pinecone account. You can typically start with a free tier.
    *   Go to [https://www.pinecone.io/](https://www.pinecone.io/) to sign up.
    *   Once logged in, you will need your **API Key** and **Environment** (e.g., "gcp-starter", "us-west1-gcp", etc.) from your Pinecone console.

2.  **Navigate to this directory:**
    ```bash
    cd 03_Vector_Databases/Pinecone
    ```
3.  **Ensure you are in the parent virtual environment:**
    Make sure you have activated the virtual environment created in the `03_Vector_Databases` directory. Common dependencies should be installed.

4.  **Install Pinecone specific dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Set up Environment Variables:**
    *   Copy `env.example.txt` to `.env` in this directory (`03_Vector_Databases/Pinecone/`):
        ```bash
        cp env.example.txt .env
        ```
    *   Open the `.env` file and add your Pinecone API Key and Environment:
        ```env
        PINECONE_API_KEY="YOUR_PINECONE_API_KEY"
        PINECONE_ENVIRONMENT="YOUR_PINECONE_ENVIRONMENT"
        # PINECONE_INDEX_NAME="my-pinecone-index" (Optional, can be set in script)
        ```

## Running the Example

From within the `03_Vector_Databases/Pinecone/` directory, run:

```bash
python example_pinecone.py
```
The script will attempt to connect to Pinecone, create/use an index, add data, search, and then clean up by deleting the index.

**Important:** The script is designed to create and delete an index for demonstration purposes. Be cautious if you adapt this for existing important indexes. 