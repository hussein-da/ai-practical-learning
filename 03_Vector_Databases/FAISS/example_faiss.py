import os
import pandas as pd
from dotenv import load_dotenv
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import openai
import time

# --- Configuration ---
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "./faiss_index.bin")

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

# --- Embedding Generation (Reusing for brevity) ---
sbert_model = None
def get_sbert_embeddings(texts_list):
    global sbert_model
    if sbert_model is None: sbert_model = SentenceTransformer(SBERT_MODEL_NAME)
    print(f"Generating SBERT embeddings for {len(texts_list)} texts...")
    embeddings = sbert_model.encode(texts_list, show_progress_bar=True)
    return np.array(embeddings).astype('float32') # FAISS works with float32 numpy arrays

def get_openai_embeddings(texts_list):
    if not OPENAI_API_KEY: raise ValueError("OPENAI_API_KEY not set.")
    openai.api_key = OPENAI_API_KEY
    print(f"Generating OpenAI embeddings for {len(texts_list)} texts...")
    response = openai.Embedding.create(input=texts_list, model=OPENAI_EMBEDDING_MODEL)
    embeddings = [r['embedding'] for r in response['data']]
    return np.array(embeddings).astype('float32')

def generate_embeddings(texts_list):
    if EMBEDDING_CHOICE == "sbert": return get_sbert_embeddings(texts_list)
    elif EMBEDDING_CHOICE == "openai": return get_openai_embeddings(texts_list)
    else: raise ValueError("Invalid EMBEDDING_CHOICE.")

# --- Data Handling ---
def load_data(csv_path):
    df = pd.read_csv(csv_path)
    # Keep original index for mapping results, ensure ID is useful if needed
    df['original_id'] = df['id'].astype(str)
    df.fillna({'text': '', 'category': 'unknown', 'topic': 'unknown'}, inplace=True)
    print(f"Loaded {len(df)} records from {csv_path}.")
    # We will use the DataFrame index (0, 1, 2...) as the internal ID for FAISS
    return df

# --- FAISS Index Operations ---
def build_faiss_index(embeddings):
    """Builds a simple FAISS index (IndexFlatL2)."""
    print(f"Building FAISS IndexFlatL2 for {embeddings.shape[0]} vectors of dimension {embeddings.shape[1]}...")
    index = faiss.IndexFlatL2(embeddings.shape[1]) # L2 distance
    # For Cosine Similarity, use IndexFlatIP and normalize embeddings first
    # faiss.normalize_L2(embeddings)
    # index = faiss.IndexFlatIP(embeddings.shape[1]) # Inner Product
    index.add(embeddings)
    print(f"FAISS index built. Total vectors in index: {index.ntotal}")
    return index

def save_faiss_index(index, path):
    """Saves the FAISS index to disk."""
    print(f"Saving FAISS index to {path}...")
    faiss.write_index(index, path)
    print("Index saved.")

def load_faiss_index(path):
    """Loads a FAISS index from disk."""
    if os.path.exists(path):
        print(f"Loading FAISS index from {path}...")
        index = faiss.read_index(path)
        print(f"Index loaded. Total vectors: {index.ntotal}")
        return index
    else:
        print(f"FAISS index file not found at {path}.")
        return None

# --- Searching ---
def search_faiss(index, data_df, query_text, top_k=3):
    """Searches the FAISS index and maps results back to original data."""
    print(f"\nSearching for: '{query_text}'")
    
    # Generate embedding for the query text
    query_embedding = generate_embeddings([query_text])
    # faiss.normalize_L2(query_embedding) # Normalize if using IndexFlatIP
    
    # Perform the search
    # `search` returns distances (D) and indices (I) of neighbors
    distances, indices = index.search(query_embedding, top_k) 
    
    print("Results:")
    if len(indices[0]) > 0 and indices[0][0] != -1: # Check if any results found (-1 indicates no result)
        for i in range(len(indices[0])):
            faiss_index = indices[0][i]
            distance = distances[0][i]
            # Map FAISS index back to original DataFrame row
            original_data = data_df.iloc[faiss_index]
            print(f"  Match {i+1}: FAISS Index: {faiss_index}, Distance: {distance:.4f}")
            print(f"  Original ID: {original_data['original_id']}")
            print(f"  Text: {original_data['text']}")
            print(f"  Metadata: {{category: '{original_data['category']}', topic: '{original_data['topic']}'}}")
    else:
        print("  No matches found.")

# --- Main Execution ---
def main():
    data_df = load_data(SAMPLE_DATA_PATH)
    texts = data_df['text'].tolist()

    # Try to load index first
    index = load_faiss_index(FAISS_INDEX_PATH)

    if index is None:
        print("No existing index found, building a new one...")
        # Generate embeddings
        embeddings = generate_embeddings(texts)
        
        # Ensure embedding dimension matches config
        if embeddings.shape[1] != EMBEDDING_DIMENSION:
             raise ValueError(f"Generated embedding dimension ({embeddings.shape[1]}) does not match configured dimension ({EMBEDDING_DIMENSION}). Check your embedding model and configuration.")

        # Build index
        index = build_faiss_index(embeddings)
        
        # Optionally save the index
        save_faiss_index(index, FAISS_INDEX_PATH)
    elif index.d != EMBEDDING_DIMENSION:
         print(f"Warning: Loaded index dimension ({index.d}) does not match configured dimension ({EMBEDDING_DIMENSION}). Rebuilding index.")
         # Generate embeddings
         embeddings = generate_embeddings(texts)
         if embeddings.shape[1] != EMBEDDING_DIMENSION:
             raise ValueError(f"Generated embedding dimension ({embeddings.shape[1]}) does not match configured dimension ({EMBEDDING_DIMENSION}). Check your embedding model and configuration.")
         # Build index
         index = build_faiss_index(embeddings)
         # Save the new index
         save_faiss_index(index, FAISS_INDEX_PATH)
    else:
         print(f"Using loaded FAISS index with {index.ntotal} vectors.")

    # Example Searches
    search_faiss(index, data_df, "deep sea exploration")
    search_faiss(index, data_df, "history of art and culture", top_k=2)
    search_faiss(index, data_df, "computer programming basics")
    search_faiss(index, data_df, "healthy lifestyle tips")
    search_faiss(index, data_df, "non_existent_topic_for_testing_empty_results")

    # Note: FAISS itself doesn't have built-in metadata filtering like Pinecone/Qdrant/Chroma.
    # You would typically perform a broader FAISS search (e.g., top_k=50)
    # and then filter the results *after* the search based on the metadata 
    # stored separately (like in the data_df).
    # Example concept (not implemented fully here):
    # distances, indices = index.search(query_embedding, k=50)
    # filtered_results = []
    # for i in range(len(indices[0])):
    #     if indices[0][i] != -1:
    #         original_data = data_df.iloc[indices[0][i]]
    #         if original_data['category'] == 'technology': # Apply filter
    #             filtered_results.append(original_data)
    #         if len(filtered_results) == desired_top_k: # Stop when enough filtered results found
    #             break
    
    print("\nFAISS example complete.")

if __name__ == "__main__":
    main() 