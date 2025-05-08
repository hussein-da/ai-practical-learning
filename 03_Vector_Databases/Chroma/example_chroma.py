import os
import pandas as pd
from dotenv import load_dotenv
import chromadb
from chromadb.utils import embedding_functions
import time
from sentence_transformers import SentenceTransformer
import numpy as np

# --- Configuration ---
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "semantic_search_chroma")
CHROMA_PERSIST_PATH = os.getenv("CHROMA_PERSIST_PATH") # If None, Chroma runs in-memory

# Embedding function choice: "default_sbert" or "openai"
# Chroma uses sentence-transformers/all-MiniLM-L6-v2 by default if no embedding_function is specified for a collection
# or if you use chromadb.utils.embedding_functions.DefaultEmbeddingFunction()
EMBEDDING_FUNC_CHOICE = "default_sbert" # or "openai"

OPENAI_EMBEDDING_MODEL_NAME = "text-embedding-ada-002"
# If using a specific SentenceTransformer model other than Chroma's default internal one:
# SBERT_MODEL_NAME_FOR_CHROMA = "all-mpnet-base-v2" # Example

SAMPLE_DATA_PATH = "data/sample_text.csv"

MODEL_NAME = 'all-MiniLM-L6-v2'
COLLECTION_NAME = "my_chroma_collection_v3" # New name to avoid conflicts

# --- Chroma Client and Embedding Function Initialization ---
chroma_client = None
embedding_function = None

def initialize_chroma():
    """Initializes Chroma client and embedding function."""
    global chroma_client, embedding_function
    print("Initializing Chroma...")

    # Setup embedding function
    if EMBEDDING_FUNC_CHOICE == "openai":
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in .env file for OpenAI embedding function.")
        print(f"Using OpenAI embedding function with model: {OPENAI_EMBEDDING_MODEL_NAME}")
        embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key=OPENAI_API_KEY,
            model_name=OPENAI_EMBEDDING_MODEL_NAME
        )
    # elif EMBEDDING_FUNC_CHOICE == "custom_sbert": # Example if you want a specific SBERT model via Chroma's utility
    #     print(f"Using SentenceTransformer embedding function with model: {SBERT_MODEL_NAME_FOR_CHROMA}")
    #     embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    #         model_name=SBERT_MODEL_NAME_FOR_CHROMA
    #     )
    else: # Default SBERT
        print("Using Chroma's default SentenceTransformer embedding function (all-MiniLM-L6-v2).")
        embedding_function = embedding_functions.DefaultEmbeddingFunction()

    # Setup Chroma client
    if CHROMA_PERSIST_PATH:
        print(f"Using persistent Chroma client, storing data in: {CHROMA_PERSIST_PATH}")
        # Ensure the directory exists if you want to avoid potential issues with Chroma creating it
        os.makedirs(CHROMA_PERSIST_PATH, exist_ok=True)
        chroma_client = chromadb.PersistentClient(path=CHROMA_PERSIST_PATH)
    else:
        print("Using in-memory Chroma client.")
        chroma_client = chromadb.Client() # Ephemeral client
    
    print("Chroma client and embedding function initialized.")
    print(f"Available collections: {chroma_client.list_collections()}")

# --- Helper Functions ---
def get_embeddings(texts, model):
    """Generates embeddings for a list of texts."""
    print(f"Embedding {len(texts)} texts using {model.config.model_card_data.name}...")
    return model.encode(texts)

# --- Data Handling & Upsertion ---
def load_data(csv_path):
    df = pd.read_csv(csv_path)
    df['id'] = df['id'].astype(str) # Chroma IDs must be strings
    df.fillna({
        'text': '',
        'category': 'unknown',
        'author': 'unknown',
        'year': 0,
        'status': 'unknown'
    }, inplace=True)
    df['year'] = df['year'].astype(int)
    print(f"Loaded {len(df)} records from {csv_path}.")
    return df

def prepare_and_add_to_collection(collection, df):
    """Prepares data and adds it to the Chroma collection."""
    print(f"Preparing to add {len(df)} documents to collection '{collection.name}'...")
    
    documents = df['text'].tolist()
    ids = df['id'].tolist()
    metadatas = []
    for _, row in df.iterrows():
        meta = {
            "category": row['category'],
            "author": row['author'],
            "year": int(row['year']), # Ensure year is int
            "status": row['status"]
        }
        metadatas.append(meta)

    # Add to collection - Chroma handles embedding generation here
    # Upsert logic: if IDs already exist, they are updated.
    try:
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Successfully added/updated {len(documents)} documents to collection '{collection.name}'.")
        print(f"Collection '{collection.name}' now contains {collection.count()} documents.")
    except Exception as e:
        print(f"Error adding documents to collection: {e}")
        # You might want to add batching here for very large datasets, though Chroma's add can handle lists.
        # For very large scale, consider `collection.add` in smaller chunks.

# --- Querying ---
def query_chroma(collection, query_texts, n_results=3, where_filter=None, where_document_filter=None):
    """Queries the Chroma collection."""
    if not isinstance(query_texts, list):
        query_texts = [query_texts]
        
    print(f"\nQuerying collection '{collection.name}' with texts: {query_texts}")
    if where_filter:
        print(f"Applying metadata WHERE filter: {where_filter}")
    if where_document_filter:
        print(f"Applying document WHERE_DOCUMENT filter: {where_document_filter}")

    results = collection.query(
        query_texts=query_texts,
        n_results=n_results,
        where=where_filter, # Metadata filter
        where_document=where_document_filter # Document content filter
        # include=['metadatas', 'documents', 'distances'] # Default is all these
    )
    
    print("Results:")
    # Chroma query results are structured per query text if multiple query_texts are given
    # For simplicity, assuming one query text for printing, or iterate through results if multiple queries
    
    ids = results.get('ids', [[]])[0]
    documents = results.get('documents', [[]])[0]
    metadatas = results.get('metadatas', [[]])[0]
    distances = results.get('distances', [[]])[0]

    if not ids:
        print("  No matches found.")
        return results

    for i in range(len(ids)):
        print(f"  ID: {ids[i]}, Distance: {distances[i]:.4f}")
        print(f"  Text: {documents[i]}")
        print(f"  Metadata: {metadatas[i]}")
    return results

# --- Main Execution ---
def main():
    global chroma_client, embedding_function
    initialize_chroma()
    if not chroma_client or not embedding_function:
        print("Chroma client or embedding function not initialized. Exiting.")
        return

    # Get or create collection
    print(f"Getting/Creating collection: {CHROMA_COLLECTION_NAME}")
    try:
        collection = chroma_client.get_or_create_collection(
            name=CHROMA_COLLECTION_NAME,
            embedding_function=embedding_function # Assign the chosen embedding function
            # metadata={"hnsw:space": "cosine"} # Default is l2, cosine is often better for text
        )
        print(f"Using collection '{collection.name}' with {collection.count()} documents.")
    except Exception as e:
        print(f"Error getting or creating collection: {e}")
        return

    data_df = load_data(SAMPLE_DATA_PATH)
    
    # Check if data needs indexing (simple check)
    # For more robust check, you might query for existing IDs
    if collection.count() < len(data_df):
        print("Data not fully indexed or collection is new. Proceeding with adding documents.")
        prepare_and_add_to_collection(collection, data_df)
    else:
        print("Data appears to be already indexed. Skipping adding documents.")

    # Example Queries
    query_chroma(collection, "stories about mysteries or secrets")
    query_chroma(collection, "impact of technology on society", n_results=2)
    
    # Query with metadata filter
    query_chroma(collection, "scientific breakthroughs", 
                 where_filter={"category": "science", "year": {"$gte": 2023}})
                 
    query_chroma(collection, "articles by Story Teller", 
                 where_filter={"author": "Story Teller"})

    # Query with document content filter
    query_chroma(collection, "guides for home activities", 
                 where_document_filter={"$contains": "guide"})
                 
    query_chroma(collection, "discussions on consciousness", 
                 where_filter={"status": "archived"},
                 where_document_filter={"$contains": "consciousness"})

    query_chroma(collection, "non_existent_topic_for_testing_empty_results")

    # --- Optional: Cleanup (Commented out) ---
    # print("\n--- Cleanup --- (Commented out by default)")
    # To delete a collection (use with extreme caution!):
    # print(f"\nDeleting collection '{CHROMA_COLLECTION_NAME}'... (Commented out by default)")
    # chroma_client.delete_collection(name=CHROMA_COLLECTION_NAME)
    # print(f"Collection '{CHROMA_COLLECTION_NAME}' deleted.")
    # print(f"Available collections after delete: {chroma_client.list_collections()}")

    # If using persistent client and want to clear storage (MANUALLY DELETE THE FOLDER CHROMA_PERSIST_PATH)
    # If using in-memory, data is gone when script ends or client is reset.
    # chroma_client.reset() # Resets the entire database an in-memory client - USE WITH CAUTION

    # --- Main Script ---
    print(f"Initializing SentenceTransformer model: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)

    documents_text = [
        "The sky is blue and the sun is shining.",
        "Machine learning involves complex algorithms and data.",
        "Chroma is a vector database for AI applications.",
        "Exploring new recipes is a fun weekend activity.",
        "Vector embeddings capture semantic relationships in text."
    ]
    print(f"\n--- Original Documents ({len(documents_text)}) ---")
    for i, doc in enumerate(documents_text):
        print(f"  Doc {i+1}: {doc}")

    document_embeddings = get_embeddings(documents_text, model)
    if document_embeddings is None or len(document_embeddings) == 0:
        print("Error generating embeddings. Exiting.")
        return
    print(f"Generated {len(document_embeddings)} embeddings, each with dimension {document_embeddings.shape[1]}.")

    print("\n--- Initializing ChromaDB (In-Memory Client) ---")
    client = chromadb.Client() # Ephemeral client

    print(f"Attempting to create collection: '{COLLECTION_NAME}' (deleting if exists for clean run)")
    try:
        client.delete_collection(name=COLLECTION_NAME)
        print(f"  Successfully deleted pre-existing collection: '{COLLECTION_NAME}'.")
    except Exception:
        print(f"  Collection '{COLLECTION_NAME}' did not pre-exist or could not be deleted (normal for first run).")
        pass
    
    collection = client.create_collection(
        name=COLLECTION_NAME, 
        metadata={"hnsw:space": "cosine"} # Using cosine similarity
    )
    print(f"Collection '{COLLECTION_NAME}' created.")

    print("\n--- Adding Documents to ChromaDB Collection ---")
    doc_ids = [f"id_{i}" for i in range(len(documents_text))]
    metadatas_list = [{"source": "simple_script", "length": len(text)} for text in documents_text]

    collection.add(
        embeddings=document_embeddings.tolist(),
        documents=documents_text,
        metadatas=metadatas_list,
        ids=doc_ids
    )
    print(f"Added {collection.count()} documents to '{COLLECTION_NAME}'.")

    query_text = "Tell me about AI vector databases."
    print(f"\n--- Performing Similarity Search ---")
    print(f"Query Text: \"{query_text}\"")
    query_embedding = get_embeddings([query_text], model)

    num_results = 2
    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=num_results,
        include=['documents', 'distances', 'metadatas']
    )

    print(f"\n--- Search Results (Top {num_results}) ---")
    if results and results.get('ids') and results['ids'][0]:
        for i in range(len(results['ids'][0])):
            print(f"  Result {i+1}:")
            print(f"    ID: {results['ids'][0][i]}")
            print(f"    Document: \"{results['documents'][0][i]}\"")
            print(f"    Distance: {results['distances'][0][i]:.4f}")
            print(f"    Metadata: {results['metadatas'][0][i]}")
    else:
        print("No results found or error in query structure.")
        print(f"Debug Results: {results}")
    
    print("\n--- Cleaning up: Deleting collection ---")
    client.delete_collection(name=COLLECTION_NAME)
    print(f"Collection '{COLLECTION_NAME}' deleted.")
    print("ChromaDB example script finished.")

if __name__ == "__main__":
    main() 