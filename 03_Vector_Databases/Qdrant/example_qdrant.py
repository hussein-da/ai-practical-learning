import os
import uuid
import pandas as pd
from dotenv import load_dotenv
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import PointStruct, Distance, VectorParams, Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer # For local embeddings
import openai # For OpenAI embeddings
import time
import numpy as np

# --- Configuration ---
load_dotenv()

# Qdrant connection details (choose one method)
QDRANT_HOST = os.getenv("QDRANT_HOST") # For local Docker
QDRANT_PORT = os.getenv("QDRANT_PORT", "6334") # gRPC port for local Docker
QDRANT_URL = os.getenv("QDRANT_URL")   # For Qdrant Cloud or specific URL, e.g., "http://localhost:6333"
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY") # For Qdrant Cloud or secured local instance

QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "semantic_search_qdrant")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") # Optional

# Embedding model choice: "sbert" or "openai"
EMBEDDING_CHOICE = "sbert" # or "openai"
SBERT_MODEL_NAME = 'all-MiniLM-L6-v2'
OPENAI_EMBEDDING_MODEL = 'text-embedding-ada-002'

if EMBEDDING_CHOICE == "sbert":
    EMBEDDING_DIMENSION = 384
elif EMBEDDING_CHOICE == "openai":
    EMBEDDING_DIMENSION = 1536
else:
    raise ValueError("Invalid EMBEDDING_CHOICE. Choose 'sbert' or 'openai'.")

SAMPLE_DATA_PATH = "data/sample_text.csv"

# --- Qdrant Client Initialization ---
qdrant_client = None

def initialize_qdrant_client():
    """Initializes connection to Qdrant."""
    global qdrant_client
    print("Initializing Qdrant client...")
    if QDRANT_URL: # Primarily for Qdrant Cloud or specific http endpoint
        print(f"Connecting to Qdrant at URL: {QDRANT_URL}")
        qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    elif QDRANT_HOST: # For local Docker using host and port
        print(f"Connecting to Qdrant at host: {QDRANT_HOST}, port: {QDRANT_PORT}")
        qdrant_client = QdrantClient(host=QDRANT_HOST, port=int(QDRANT_PORT), api_key=QDRANT_API_KEY) # gRPC port
        # If using HTTP port instead: qdrant_client = QdrantClient(host=QDRANT_HOST, http_port=int(QDRANT_PORT), api_key=QDRANT_API_KEY)
    else:
        print("Connecting to Qdrant at default localhost:6333 (HTTP). Ensure it's running.")
        qdrant_client = QdrantClient(host="localhost", port=6333) # Default to HTTP if no other config

    try:
        qdrant_client.list_collections()
        print("Successfully connected to Qdrant.")
    except Exception as e:
        print(f"Failed to connect to Qdrant: {e}")
        print("Please ensure Qdrant is running and accessible, and your .env configuration is correct.")
        qdrant_client = None
        return

    # Create collection if it doesn't exist
    try:
        collection_info = qdrant_client.get_collection(collection_name=QDRANT_COLLECTION_NAME)
        print(f"Collection '{QDRANT_COLLECTION_NAME}' already exists.")
        print(f"Collection info: {collection_info}")
    except Exception as e: # More specific: except models.UnexpectedResponse as e: if e.status_code == 404:
        if "404" in str(e) or "not found" in str(e).lower(): # Basic check for collection not found
            print(f"Collection '{QDRANT_COLLECTION_NAME}' does not exist. Creating it now...")
            qdrant_client.recreate_collection(
                collection_name=QDRANT_COLLECTION_NAME,
                vectors_config=VectorParams(size=EMBEDDING_DIMENSION, distance=Distance.COSINE)
            )
            print(f"Collection '{QDRANT_COLLECTION_NAME}' created.")
        else:
            print(f"An error occurred while checking collection: {e}")
            raise

# --- Embedding Generation (Reusing from Pinecone example for brevity) ---
sbert_model = None
def get_sbert_embeddings(texts_list):
    global sbert_model
    if sbert_model is None: sbert_model = SentenceTransformer(SBERT_MODEL_NAME)
    return sbert_model.encode(texts_list, show_progress_bar=True).tolist()

def get_openai_embeddings(texts_list):
    if not OPENAI_API_KEY: raise ValueError("OPENAI_API_KEY not set.")
    openai.api_key = OPENAI_API_KEY
    embeddings = [r['embedding'] for r in openai.Embedding.create(input=texts_list, model=OPENAI_EMBEDDING_MODEL)['data']]
    return embeddings

def generate_embeddings(texts_list):
    if EMBEDDING_CHOICE == "sbert": return get_sbert_embeddings(texts_list)
    elif EMBEDDING_CHOICE == "openai": return get_openai_embeddings(texts_list)
    else: raise ValueError("Invalid EMBEDDING_CHOICE.")

# --- Data Handling & Upsertion ---
def load_data(csv_path):
    df = pd.read_csv(csv_path)
    df['id'] = df['id'].astype(str) # Qdrant point IDs can be int or UUID string
    df.fillna({'text': '', 'category': 'unknown', 'author': 'unknown', 'year': 0}, inplace=True)
    df['year'] = df['year'].astype(int) # Ensure year is int for potential range filters
    return df

def prepare_and_upsert_data(df):
    if not qdrant_client: return
    print(f"Preparing and upserting {len(df)} records...")
    
    texts_to_embed = df['text'].tolist()
    embeddings = generate_embeddings(texts_to_embed)
    
    points = []
    for idx, row in df.iterrows():
        # Qdrant point IDs can be integers or UUIDs. Using provided ID as string.
        # If your CSV IDs are not unique or suitable, generate UUIDs: point_id=str(uuid.uuid4())
        point_id = row['id'] 
        try:
            # Attempt to convert to int if it's a numeric string, otherwise use as string (UUID)
            point_id_int = int(point_id)
            point_id = point_id_int
        except ValueError:
            # If it's not a simple integer string, treat as UUID or string ID
            try:
                point_id = uuid.UUID(point_id) # Validate if it's a UUID string
            except ValueError:
                 # Keep as string if not int and not UUID
                 pass # point_id remains as is

        payload = {
            "text": row['text'],
            "category": row['category'],
            "author": row['author'],
            "year": int(row['year']) # Ensure year is int
        }
        points.append(PointStruct(id=point_id, vector=embeddings[idx], payload=payload))

    # Upsert in batches
    batch_size = 100
    for i in range(0, len(points), batch_size):
        batch = points[i:i + batch_size]
        try:
            qdrant_client.upsert(collection_name=QDRANT_COLLECTION_NAME, points=batch, wait=True)
            print(f"Upserted batch {i // batch_size + 1}/{len(points)//batch_size +1}")
        except Exception as e:
            print(f"Error upserting batch: {e}")
    print(f"Upsertion complete. Collection '{QDRANT_COLLECTION_NAME}' status:")
    print(qdrant_client.get_collection(collection_name=QDRANT_COLLECTION_NAME))

# --- Querying ---
def query_qdrant(query_text, top_k=3, filter_conditions=None):
    if not qdrant_client: return
    print(f"\nQuerying for: '{query_text}'")
    if filter_conditions:
        print(f"Applying filter: {filter_conditions}")
        
    query_embedding = generate_embeddings([query_text])[0]
    
    search_result = qdrant_client.search(
        collection_name=QDRANT_COLLECTION_NAME,
        query_vector=query_embedding,
        query_filter=filter_conditions, # Qdrant Filter object
        limit=top_k,
        with_payload=True # To get the payload/metadata back
    )
    
    print("Results:")
    if search_result:
        for hit in search_result:
            print(f"  ID: {hit.id}, Score: {hit.score:.4f}")
            print(f"  Text: {hit.payload.get('text','N/A')}")
            print(f"  Payload: {hit.payload}")
    else:
        print("  No matches found.")
    return search_result

# --- Main Execution ---
def main():
    initialize_qdrant_client()
    if not qdrant_client:
        return

    data_df = load_data(SAMPLE_DATA_PATH)
    
    # Check if data needs indexing
    try:
        collection_info = qdrant_client.get_collection(QDRANT_COLLECTION_NAME)
        # Qdrant counts can be eventually consistent. A small delay might give a more accurate count.
        time.sleep(1) 
        current_points_count = collection_info.points_count
        print(f"Current points in collection: {current_points_count}, Data to load: {len(data_df)}")
        if current_points_count < len(data_df):
             print("Data not fully indexed or collection is new. Proceeding with upsertion.")
             prepare_and_upsert_data(data_df)
        else:
            print("Data appears to be already indexed. Skipping upsertion.")
    except Exception as e:
        print(f"Error checking collection points count or during upsert decision: {e}. Attempting upsert anyway.")
        prepare_and_upsert_data(data_df)

    # Example Queries
    query_qdrant("healthy food recipes") # General query
    query_qdrant("books about space travel", top_k=2)
    
    # Query with filter
    tech_filter = Filter(must=[
        FieldCondition(key="category", match=MatchValue(value="technology"))
    ])
    query_qdrant("AI advancements", filter_conditions=tech_filter)

    history_filter_2020_plus = Filter(must=[
        FieldCondition(key="category", match=MatchValue(value="history")),
        FieldCondition(key="year", range=models.Range(gte=2020))
    ])
    # This will likely be empty given sample data for history is older, demonstrating filter working
    query_qdrant("modern historical events", filter_conditions=history_filter_2020_plus)

    # Query for specific author in technology
    author_tech_filter = Filter(must=[
        FieldCondition(key="author", match=MatchValue(value="Tech Trends")),
        FieldCondition(key="category", match=MatchValue(value="technology"))
    ])
    query_qdrant("machine learning", filter_conditions=author_tech_filter)

    query_qdrant("non_existent_topic_for_testing_empty_results")

    # --- Optional: Cleanup (Commented out) ---
    # print("\n--- Cleanup --- (Commented out by default)")
    # To delete a collection (use with extreme caution!):
    # print(f"\nDeleting collection '{QDRANT_COLLECTION_NAME}'... (Commented out by default)")
    # qdrant_client.delete_collection(collection_name=QDRANT_COLLECTION_NAME)
    # print(f"Collection '{QDRANT_COLLECTION_NAME}' deleted.")

if __name__ == "__main__":
    main() 