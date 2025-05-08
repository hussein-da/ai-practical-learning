from transformers import pipeline
import pandas as pd
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define path to the data file
DATA_DIR = "data"
CSV_FILE = os.path.join(DATA_DIR, "sample_classification_data.csv")

# --- Model Selection ---
# Choose the type of classification task and corresponding model
# Option 1: Sentiment Analysis (positive/negative)
TASK = "sentiment-analysis"
MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"

# Option 2: Topic Classification (Example - use a model fine-tuned for topics)
# TASK = "text-classification" # General text classification task
# MODEL_NAME = "SamLowe/roberta-base-go_emotions" # Example multi-label emotion classification
# MODEL_NAME = "facebook/bart-large-mnli" # Example for zero-shot classification (more complex setup)

# Load the classification pipeline
classifier_pipeline = None

def load_classification_pipeline():
    """Loads the Hugging Face text classification pipeline."""
    global classifier_pipeline
    try:
        logger.info(f"Loading text classification pipeline for task '{TASK}' with model: {MODEL_NAME}...")
        classifier_pipeline = pipeline(TASK, model=MODEL_NAME)
        logger.info("Text classification pipeline loaded successfully.")
    except Exception as e:
        logger.error(f"Error loading classification pipeline: {e}")
        classifier_pipeline = None

def load_data(file_path):
    """Loads text data from a CSV file."""
    try:
        df = pd.read_csv(file_path)
        df.fillna({'text': ''}, inplace=True)
        logger.info(f"Loaded {len(df)} records from {file_path}.")
        return df['text'].tolist()
    except FileNotFoundError:
        print(f"Error: CSV file not found at {file_path}")
        return None
    except Exception as e:
        print(f"Error loading data from {file_path}: {e}")
        return None

def perform_text_classification(texts):
    """Performs text classification using the loaded HF pipeline."""
    if classifier_pipeline is None:
        print("Text classification pipeline not loaded. Cannot classify.")
        return None
        
    print(f"\n--- Classifying {len(texts)} text samples --- ")
    results = []
    try:
        # Pipelines can often process lists directly for efficiency
        pipeline_results = classifier_pipeline(texts)
        
        print("\n--- Classification Results: ---")
        for i, text in enumerate(texts):
            result = pipeline_results[i]
            print(f"  Text:    \"{text}\"")
            print(f"  Predicted: Label='{result['label']}', Score={result['score']:.4f}")
            print("---")
            results.append({"text": text, "label": result['label'], "score": result['score']})
            
    except Exception as e:
        logger.error(f"Error during text classification pipeline execution: {e}")
        return None
        
    return results

if __name__ == "__main__":
    load_classification_pipeline()
    if classifier_pipeline:
        sample_texts = load_data(CSV_FILE)
        if sample_texts:
            classification_results = perform_text_classification(sample_texts)
            # Results are stored in classification_results if further processing is needed. 