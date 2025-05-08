import os
import time
import pandas as pd
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec, PodSpec
from sentence_transformers import SentenceTransformer # For local embeddings
import openai # For OpenAI embeddings
import numpy as np

# --- Configuration ---
# Load environment variables from .env file
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") # Optional

# Embedding model choice: "sbert" or "openai"
EMBEDDING_CHOICE = "sbert"  # or "openai"

# SBERT model name (if EMBEDDING_CHOICE is "sbert")
SBERT_MODEL_NAME = 'all-MiniLM-L6-v2'  # ~384 dimensions
# OpenAI model name (if EMBEDDING_CHOICE is "openai")
OPENAI_EMBEDDING_MODEL = 'text-embedding-ada-002' # 1536 dimensions

# Determine embedding dimension based on choice
if EMBEDDING_CHOICE == "sbert":
    # You might need to load the model once to get its dimension accurately
    # For now, common SBERT models like all-MiniLM-L6-v2 have 384 dimensions.
    # If you use a different model, update this dimension.
    EMBEDDING_DIMENSION = 384 
elif EMBEDDING_CHOICE == "openai":
    EMBEDDING_DIMENSION = 1536 # text-embedding-ada-002
else:
    raise ValueError("Invalid EMBEDDING_CHOICE. Choose 'sbert' or 'openai'.")

SAMPLE_DATA_PATH = "data/sample_text.csv"

# --- Pinecone Initialization ---
pc = None
index = None

def initialize_pinecone():
    """Initializes connection to Pinecone and gets the index."""
    global pc, index
    if not PINECONE_API_KEY or not PINECONE_ENVIRONMENT or not PINECONE_INDEX_NAME:
        raise ValueError(
            "Pinecone API Key, Environment, or Index Name not found. "
            "Please set them in your .env file and ensure PINECONE_INDEX_NAME is correct."
        )
    
    print(f"Initializing Pinecone with environment: {PINECONE_ENVIRONMENT}...")
    pc = Pinecone(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
    
    # Check if the index exists
    if PINECONE_INDEX_NAME not in pc.list_indexes().names:
        print(f"Index '{PINECONE_INDEX_NAME}' does not exist. Creating it now...")
        # To create a serverless index
        # pc.create_index(
        #     name=PINECONE_INDEX_NAME,
        #     dimension=EMBEDDING_DIMENSION,
        #     metric="cosine", # or "euclidean", "dotproduct"
        #     spec=ServerlessSpec(cloud="aws", region="us-west-2") # Specify your desired cloud and region
        # )
        # To create a pod-based index (ensure your environment supports it, e.g. free tier might use s1)
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=EMBEDDING_DIMENSION,
            metric="cosine",
            spec=PodSpec(
                environment=PINECONE_ENVIRONMENT, 
                pod_type="p1.x1", # Choose appropriate pod type e.g. "s1.x1" for free tier or starter, "p1.x1" etc. for paid
                pods=1
            )
        )
        # Wait for index to be ready
        while not pc.describe_index(PINECONE_INDEX_NAME).status['ready']:
            print("Waiting for index to be ready...")
            time.sleep(5)
        print(f"Index '{PINECONE_INDEX_NAME}' created successfully.")
    else:
        print(f"Index '{PINECONE_INDEX_NAME}' already exists.")

    index = pc.Index(PINECONE_INDEX_NAME)
    print(f"Connected to index '{PINECONE_INDEX_NAME}'.")
    print(index.describe_index_stats())

# --- Embedding Generation ---
sbert_model = None

def get_sbert_embeddings(texts):
    """Generates embeddings using a SentenceTransformer model."""
    global sbert_model
    if sbert_model is None:
        print(f"Loading SentenceTransformer model: {SBERT_MODEL_NAME}...")
        sbert_model = SentenceTransformer(SBERT_MODEL_NAME)
        print("SBERT model loaded.")
    print(f"Generating SBERT embeddings for {len(texts)} texts...")
    embeddings = sbert_model.encode(texts, show_progress_bar=True)
    return embeddings.tolist() # Convert to list of lists

def get_openai_embeddings(texts):
    """Generates embeddings using OpenAI API."""
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY not found. Please set it in your .env file.")
    openai.api_key = OPENAI_API_KEY
    print(f"Generating OpenAI embeddings for {len(texts)} texts using {OPENAI_EMBEDDING_MODEL}...")
    
    embeddings = []    
    # OpenAI API can handle multiple texts in one call, but has rate limits
    # For simplicity, embedding one by one here, but batching is better for production
    for text in texts:
        response = openai.Embedding.create(input=[text], model=OPENAI_EMBEDDING_MODEL)
        embeddings.append(response['data'][0]['embedding'])
    print(f"Generated {len(embeddings)} embeddings.")
    return embeddings

def generate_embeddings(texts):
    """Wrapper to generate embeddings based on EMBEDDING_CHOICE."""
    if EMBEDDING_CHOICE == "sbert":
        return get_sbert_embeddings(texts)
    elif EMBEDDING_CHOICE == "openai":
        return get_openai_embeddings(texts)
    else:
        raise ValueError("Invalid EMBEDDING_CHOICE.")

# --- Data Handling ---
def load_data(csv_path):
    """Loads data from a CSV file."""
    print(f"Loading data from {csv_path}...")
    df = pd.read_csv(csv_path)
    # Ensure 'id' is string for Pinecone, and handle potential NaN in text
    df['id'] = df['id'].astype(str)
    df['text'] = df['text'].fillna('') 
    print(f"Loaded {len(df)} records.")
    return df

def prepare_for_upsert(df, text_column='text', id_column='id', metadata_columns=None):
    """Prepares data for Pinecone upsert: generates embeddings and structures data."""
    print("Preparing data for upsert...")
    if metadata_columns is None:
        metadata_columns = [col for col in df.columns if col not in [id_column, text_column]]

    texts_to_embed = df[text_column].tolist()
    embeddings = generate_embeddings(texts_to_embed)
    
    vectors_to_upsert = []
    for i, row in df.iterrows():
        metadata = {col: row[col] for col in metadata_columns if col in df.columns}
        # Ensure metadata values are of supported types (string, number, boolean, or list of strings)
        for key, value in metadata.items():
            if pd.isna(value):
                metadata[key] = None # Or some default string like "N/A"
            elif not isinstance(value, (str, int, float, bool, list)):
                 metadata[key] = str(value) # Convert other types to string
        
        vectors_to_upsert.append({
            "id": row[id_column],
            "values": embeddings[i],
            "metadata": metadata
        })
    print(f"Prepared {len(vectors_to_upsert)} vectors for upsert.")
    return vectors_to_upsert

def upsert_data_batch(pinecone_index, vectors, batch_size=100):
    """Upserts data to Pinecone index in batches."""
    print(f"Upserting {len(vectors)} vectors in batches of {batch_size}...")
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i + batch_size]
        try:
            pinecone_index.upsert(vectors=batch)
            print(f"Upserted batch {i // batch_size + 1}")
        except Exception as e:
            print(f"Error upserting batch {i // batch_size + 1}: {e}")
            # Consider adding more robust error handling or retry logic here
    print("Upsert complete.")
    print(pinecone_index.describe_index_stats())

# --- Querying ---
def query_pinecone(pinecone_index, query_text, top_k=3, filter_metadata=None):
    """Generates embedding for query_text and queries Pinecone."""
    print(f"\nQuerying with text: '{query_text}'")
    if filter_metadata:
        print(f"Applying metadata filter: {filter_metadata}")
        
    query_embedding = generate_embeddings([query_text])[0]
    
    results = pinecone_index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        filter=filter_metadata
    )
    
    print("Results:")
    if results.matches:
        for match in results.matches:
            print(f"  ID: {match.id}, Score: {match.score:.4f}")
            print(f"  Text: {match.metadata.get('text', 'N/A') if match.metadata else 'N/A'}")
            print(f"  Metadata: {match.metadata}")
    else:
        print("  No matches found.")
    return results

# --- Main Execution ---
def main():
    """Main function to run the Pinecone example."""
    global index
    try:
        initialize_pinecone()
        if index is None:
            print("Pinecone index could not be initialized. Exiting.")
            return

        # Load data and prepare for upsert
        data_df = load_data(SAMPLE_DATA_PATH)
        # Check if data is already indexed (simple check based on count, could be more sophisticated)
        current_vector_count = index.describe_index_stats().total_vector_count
        if current_vector_count < len(data_df):
            print("Data not fully indexed. Proceeding with upsertion.")
            vectors_for_pinecone = prepare_for_upsert(data_df, metadata_columns=['category', 'author', 'text'])
            upsert_data_batch(index, vectors_for_pinecone)
        else:
            print("Data appears to be already indexed. Skipping upsertion.")

        # Example Queries
        query_pinecone(index, "stories about animals")
        query_pinecone(index, "controversial food opinions", top_k=2)
        query_pinecone(index, "latest technology news", filter_metadata={"category": "technology"})
        query_pinecone(index, "history facts", filter_metadata={"author": "Historian Monthly"})
        query_pinecone(index, "non_existent_topic_for_testing_empty_results")
        
        # --- Optional: Clean up / Delete --- 
        # print("\n--- Cleanup --- (Commented out by default)")
        # To delete specific vectors by ID:
        # delete_response = index.delete(ids=["1", "2"])
        # print(f"Delete response: {delete_response}")
        # print(index.describe_index_stats())

        # To delete all vectors in the index (use with extreme caution!):
        # print("\nDeleting all vectors from index... (Commented out by default)")
        # index.delete(delete_all=True)
        # print(index.describe_index_stats())
        
        # To delete the entire index (use with extreme caution!):
        # print(f"\nDeleting index '{PINECONE_INDEX_NAME}'... (Commented out by default)")
        # pc.delete_index(PINECONE_INDEX_NAME)
        # print(f"Index '{PINECONE_INDEX_NAME}' deleted.")

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 