from transformers import pipeline
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define path to the data file
DATA_DIR = "data"
TEXT_FILE = os.path.join(DATA_DIR, "sample_ner_text.txt")

# Define the pre-trained NER model to use from Hugging Face Hub
# Example: 'dbmdz/bert-large-cased-finetuned-conll03-english' is a popular choice
# You can explore other models on hf.co/models?pipeline_tag=token-classification&sort=downloads
MODEL_NAME = "dbmdz/bert-large-cased-finetuned-conll03-english"

# Load the NER pipeline
ner_pipeline = None

def load_ner_pipeline():
    """Loads the Hugging Face NER pipeline."""
    global ner_pipeline
    try:
        logger.info(f"Loading NER pipeline with model: {MODEL_NAME}...")
        # Using aggregation_strategy="simple" combines subword tokens into single entities (e.g., "Tim", "##Cook" -> "Tim Cook")
        ner_pipeline = pipeline("ner", model=MODEL_NAME, aggregation_strategy="simple")
        logger.info("NER pipeline loaded successfully.")
    except Exception as e:
        logger.error(f"Error loading NER pipeline: {e}")
        ner_pipeline = None

def load_text(file_path):
    """Loads text from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Text file not found at {file_path}")
        return None

def perform_ner_transformers(text):
    """Performs Named Entity Recognition using HF Transformers pipeline."""
    if ner_pipeline is None:
        print("NER pipeline not loaded. Cannot perform NER.")
        return None
        
    print("\n--- Processing text with Hugging Face Transformers --- ")
    try:
        entities = ner_pipeline(text)
    except Exception as e:
        logger.error(f"Error during NER pipeline execution: {e}")
        return None
        
    print("\n--- Identified Entities: ---")
    if entities:
        for entity in entities:
            print(f"  Text: {entity['word']:<25} | Label: {entity['entity_group']:<10} | Score: {entity['score']:.4f}")
            # Note: Transformers pipeline output includes start/end character indices if using default strategy,
            # but the "simple" aggregation strategy focuses on grouped entities.
    else:
        print("  No entities found by the model.")
        
    return entities

if __name__ == "__main__":
    load_ner_pipeline()
    if ner_pipeline:
        sample_text = load_text(TEXT_FILE)
        if sample_text:
            found_entities = perform_ner_transformers(sample_text)
            # Further processing or visualization could be added here if needed. 