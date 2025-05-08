from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
import logging
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Model Loading ---
# Load the sentiment analysis pipeline from Hugging Face Transformers
# This will download the model on first run if not cached.
# We load it globally so it's done only once when the application starts.
SENTIMENT_MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"
sentiment_pipeline = None

def load_model():
    """Loads the Hugging Face pipeline."""
    global sentiment_pipeline
    try:
        logger.info(f"Loading sentiment analysis model: {SENTIMENT_MODEL_NAME}...")
        sentiment_pipeline = pipeline("sentiment-analysis", model=SENTIMENT_MODEL_NAME)
        logger.info("Sentiment analysis model loaded successfully.")
    except Exception as e:
        logger.error(f"Error loading sentiment analysis model: {e}")
        # Depending on the desired behavior, you might want the app to fail startup
        # or continue without the model (and handle errors at the endpoint)
        sentiment_pipeline = None 

# --- Pydantic Models ---
class SentimentRequest(BaseModel):
    text: str

class SentimentResponse(BaseModel):
    text: str
    label: str
    score: float

# --- FastAPI Application ---
app = FastAPI(
    title="Sentiment Analysis API",
    description="A simple API to analyze the sentiment of a piece of text using a Hugging Face model.",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    """Load the model when the application starts."""
    load_model()

@app.get("/")
def read_root():
    """Root endpoint providing basic API information."""
    return {"message": "Welcome to the Sentiment Analysis API. Use the /analyze endpoint to analyze text."}

@app.post("/analyze", response_model=SentimentResponse)
def analyze_sentiment(request: SentimentRequest):
    """Analyzes the sentiment of the input text."""
    if sentiment_pipeline is None:
        logger.error("Sentiment analysis model is not loaded. Cannot process request.")
        raise HTTPException(status_code=503, detail="Sentiment analysis model is not available.")
    
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")

    try:
        logger.info(f"Analyzing text: \"{request.text[:50]}...\"")
        # The pipeline returns a list of dictionaries, e.g., [{'label': 'POSITIVE', 'score': 0.999...}]
        results = sentiment_pipeline(request.text)
        
        if not results:
             # Should not happen with standard models unless input is highly unusual
             raise ValueError("Sentiment analysis returned no results.")
             
        # Extract the primary result
        analysis = results[0]
        
        response = SentimentResponse(
            text=request.text,
            label=analysis['label'],
            score=analysis['score']
        )
        logger.info(f"Analysis complete: Label={response.label}, Score={response.score:.4f}")
        return response

    except Exception as e:
        logger.error(f"Error during sentiment analysis for text '{request.text[:50]}...': {e}")
        raise HTTPException(status_code=500, detail=f"An internal error occurred during analysis: {e}")

# To run locally (optional, usually handled by uvicorn command):
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000) 