import spacy
from spacy import displacy
import os

# Define path to the data file
DATA_DIR = "data"
TEXT_FILE = os.path.join(DATA_DIR, "sample_ner_text.txt")

# Load the pre-trained spaCy English model
# Ensure you've downloaded it: python -m spacy download en_core_web_sm
MODEL_NAME = "en_core_web_sm"

try:
    nlp = spacy.load(MODEL_NAME)
    print(f"Loaded spaCy model '{MODEL_NAME}'")
except OSError:
    print(f"spaCy model '{MODEL_NAME}' not found.")
    print(f"Please download it by running: python -m spacy download {MODEL_NAME}")
    nlp = None

def load_text(file_path):
    """Loads text from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Text file not found at {file_path}")
        return None

def perform_ner_spacy(text):
    """Performs Named Entity Recognition using spaCy and prints results."""
    if not nlp:
        print("spaCy model not loaded. Cannot perform NER.")
        return None, None
        
    print("\n--- Processing text with spaCy --- ")
    doc = nlp(text)
    
    print("\n--- Identified Entities: ---")
    entities = []
    if doc.ents:
        for ent in doc.ents:
            print(f"  Text: {ent.text:<25} | Label: {ent.label_:<10} | Start: {ent.start_char:<5} | End: {ent.end_char:<5}")
            entities.append({
                "text": ent.text,
                "label": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char
            })
    else:
        print("  No entities found by the model.")
        
    return doc, entities

def visualize_entities(doc):
    """Generates HTML visualization data using displacy."""
    if not doc:
        print("No document processed, cannot visualize.")
        return
        
    # Render directly in Jupyter/compatible environment:
    # displacy.render(doc, style="ent", jupyter=True)
    
    # Get HTML string
    html = displacy.render(doc, style="ent", page=False)
    print("\n--- Visualization HTML (copy and save as .html file to view) ---")
    print(html)
    # You can save this HTML to a file:
    # with open("ner_visualization_spacy.html", "w", encoding="utf-8") as f:
    #     f.write(html)
    # print("\nVisualization saved to ner_visualization_spacy.html")


if __name__ == "__main__":
    sample_text = load_text(TEXT_FILE)
    
    if sample_text and nlp:
        processed_doc, found_entities = perform_ner_spacy(sample_text)
        if processed_doc:
             visualize_entities(processed_doc) 