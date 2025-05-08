# Qdrant Examples

This section demonstrates how to use Qdrant, an open-source vector similarity search engine and vector database.

## About Qdrant

Qdrant (pronounced quadrant) is designed to provide a production-ready service with a convenient API to store, search, and manage points (vectors) with an additional payload (metadata). Qdrant is built in Rust, making it fast and reliable.

**Key Features:**

*   **Performance:** Optimized for low-latency, high-throughput similarity search.
*   **Filtering:** Rich filtering capabilities, allowing combination of vector search with various conditions on payload data.
*   **Scalability:** Can be deployed as a distributed system for handling large datasets.
*   **Persistence:** Data is persisted on disk.
*   **Deployment Options:** Can be self-hosted (e.g., using Docker) or used via Qdrant Cloud (managed service).
*   **Rich Data Types for Payload:** Supports various data types for metadata.

For this example, we will primarily focus on using a local Qdrant instance (e.g., via Docker or an in-memory option if simple enough for the client).

## Example in `example_qdrant.py`

The `example_qdrant.py` script will demonstrate:

1.  **Generating Sample Embeddings:** Using `sentence-transformers`.
2.  **Initializing Qdrant Client:** Connecting to a Qdrant instance (e.g., local Docker container or in-memory).
3.  **Creating a Collection:** Setting up a collection with the appropriate vector parameters (size, distance metric).
4.  **Adding Points (Vectors & Payload):** Storing embeddings along with their IDs and associated metadata (payload).
5.  **Performing a Similarity Search:** Querying the collection with a new vector to find similar items, potentially with filtering.
6.  **Inspecting Results:** Showing the retrieved points, scores, and payloads.

## Setup

1.  **Qdrant Instance:**
    *   **Option A (Recommended for local testing): Docker**
        Run a Qdrant instance using Docker:
        ```bash
        docker run -p 6333:6333 -p 6334:6334 \
            -v $(pwd)/qdrant_storage:/qdrant/storage:z \
            qdrant/qdrant
        ```
        This will start Qdrant and persist its data in a `qdrant_storage` directory in your current path.
    *   **Option B: Qdrant Cloud**
        Sign up at [cloud.qdrant.io](https://cloud.qdrant.io/) and create a free cluster. You will get a URL and an API key.
    *   **Option C: In-memory (if script supports simply)**
        The script might try an in-memory setup if a URL is not provided, for very basic demos.

2.  **Navigate to this directory:**
    ```bash
    cd 03_Vector_Databases/Qdrant
    ```
3.  **Ensure you are in the parent virtual environment:**
    Make sure you have activated the virtual environment created in the `03_Vector_Databases` directory.

4.  **Install Qdrant specific dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Set up Environment Variables (Optional, but recommended for Docker/Cloud):**
    *   Copy `env.example.txt` to `.env` in this directory:
        ```bash
        cp env.example.txt .env
        ```
    *   Open the `.env` file. If using Docker locally with default ports, you might set:
        ```env
        QDRANT_URL="http://localhost:6333"
        # QDRANT_API_KEY="YOUR_QDRANT_CLOUD_API_KEY_IF_ANY" # Only if using Qdrant Cloud with an API key
        # QDRANT_COLLECTION_NAME="my_qdrant_collection" (Optional, can be set in script)
        ```
        If using Qdrant Cloud, use your cluster URL and API key.

## Running the Example

From within the `03_Vector_Databases/Qdrant/` directory, run:

```bash
python example_qdrant.py
```
The script will attempt to connect to Qdrant, create/use a collection, add data, search, and display results. 