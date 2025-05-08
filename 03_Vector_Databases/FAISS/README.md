# FAISS (Facebook AI Similarity Search) Examples

This section demonstrates how to use FAISS, a library developed by Facebook AI, for efficient similarity search of vector embeddings.

## About FAISS

FAISS (Facebook AI Similarity Search) is a highly optimized library for searching in sets of dense vectors. It is not a full-fledged vector database (which typically offers managed services, metadata storage, APIs, etc.) but rather a powerful toolkit for performing nearest neighbor searches. It's particularly useful when you need to build and search indexes locally or as a core component within a larger system.

**Key Features:**

*   **High Performance:** Optimized for speed and memory efficiency, especially for large datasets.
*   **Variety of Index Types:** Offers many different index types (e.g., `IndexFlatL2`, `IndexIVFFlat`, `IndexHNSWFlat`) to balance speed, accuracy, and memory usage.
*   **CPU and GPU Support:** Can leverage both CPU and GPU for indexing and searching.
*   **Scalability:** Can handle billions of vectors.

For these examples, we will focus on `faiss-cpu` for broader accessibility.

## Example in `example_faiss.py`

The `example_faiss.py` script will demonstrate:

1.  **Generating Sample Embeddings:** Using `sentence-transformers`.
2.  **Building a FAISS Index:** Creating a simple index (e.g., `IndexFlatL2` for exact search using L2 distance).
3.  **Adding Embeddings to the Index:** Populating the index with the generated vector embeddings.
4.  **Performing a Similarity Search:** Using a query vector to find the k-nearest neighbors in the index.
5.  **Interpreting Results:** Retrieving the distances and indices of the similar items and mapping them back to the original sentences.

## Setup

1.  **Navigate to this directory:**
    ```bash
    cd 03_Vector_Databases/FAISS
    ```
2.  **Ensure you are in the parent virtual environment:**
    Make sure you have activated the virtual environment created in the `03_Vector_Databases` directory. Common dependencies (`sentence-transformers`, `python-dotenv`, `numpy`) should be installed.

3.  **Install FAISS specific dependencies:**
    Install the `faiss-cpu` library from the local `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Example

From within the `03_Vector_Databases/FAISS/` directory, run:

```bash
python example_faiss.py
```
The script will output the steps of creating embeddings, building the FAISS index, and the similarity search results. 