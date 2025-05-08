from flask import Flask, request, jsonify
from transformers import pipeline
import os

# Initialize Flask app
app = Flask(__name__)

# Load the sentiment analysis pipeline from Hugging Face
# Using a distilled version for faster loading and inference, suitable for API
# You can choose other models like 'bert-base-uncased-finetuned-sst-2-english'
MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"
try:
    print(f"Loading sentiment analysis model: {MODEL_NAME}...")
    # Specify task explicitly for clarity
    sentiment_pipeline = pipeline("sentiment-analysis", model=MODEL_NAME)
    print("Sentiment analysis model loaded successfully.")
except Exception as e:
    print(f"Error loading sentiment analysis model: {e}")
    sentiment_pipeline = None

@app.route('/', methods=['GET'])
def home():
    """Basic route to check if the API is running."""
    return jsonify({"message": "Sentiment Analysis API is running. Use POST /analyze_sentiment to analyze text."}) 

@app.route('/analyze_sentiment', methods=['POST'])
def analyze_sentiment():
    """Analyzes the sentiment of the text provided in the request body."""
    if not sentiment_pipeline:
        return jsonify({"error": "Sentiment analysis model not loaded."}), 500

    if not request.is_json:
        return jsonify({"error": "Request must be JSON."}), 400

    data = request.get_json()
    text_to_analyze = data.get('text')

    if not text_to_analyze or not isinstance(text_to_analyze, str):
        return jsonify({"error": "Missing 'text' field or field is not a string in JSON body."}), 400
        
    if len(text_to_analyze.strip()) == 0:
        return jsonify({"error": "'text' field cannot be empty."}), 400

    try:
        print(f"Analyzing text: '{text_to_analyze[:100]}...'") # Log snippet
        results = sentiment_pipeline(text_to_analyze)
        # The pipeline returns a list of dictionaries, e.g., [{'label': 'POSITIVE', 'score': 0.9998...}]
        if results:
            result = results[0] # Get the first result
            response = {
                "text": text_to_analyze,
                "sentiment": result['label'],
                "score": result['score']
            }
            print(f"Analysis result: {response}")
            return jsonify(response)
        else:
            return jsonify({"error": "Sentiment analysis pipeline returned no results."}), 500
            
    except Exception as e:
        print(f"Error during sentiment analysis: {e}")
        return jsonify({"error": "An error occurred during analysis."}), 500

if __name__ == '__main__':
    # Use waitress as the production server
    from waitress import serve
    port = int(os.environ.get("PORT", 5000)) # Default to 5000 if PORT not set
    print(f"Starting server on port {port}...")
    serve(app, host='0.0.0.0', port=port)
    # For development only (single-threaded, not for production):
    # app.run(host='0.0.0.0', port=port, debug=True) 