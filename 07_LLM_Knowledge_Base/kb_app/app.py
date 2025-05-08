import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter

# --- Configuration & Initialization ---
ENV_FILE_PATH = ".env"
KB_FILE_PATH = "data/kb_content.md"
MODEL_NAME = "gpt-3.5-turbo" # Or choose another model like "gpt-4"

# Load API Key
def load_api_key():
    """Loads OpenAI API key from .env file."""
    if not os.path.exists(ENV_FILE_PATH):
        st.error(f"Environment file '{ENV_FILE_PATH}' not found. Please create it by copying '.env.example' to '.env' and adding your OpenAI API key.")
        st.stop()
        return None
    load_dotenv(dotenv_path=ENV_FILE_PATH)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("OPENAI_API_KEY not found in .env file. Please add it.")
        st.stop()
        return None
    return api_key

api_key = load_api_key()
if not api_key:
    # Stop execution if API key is not loaded (error displayed in load_api_key)
    st.stop()

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Load Knowledge Base Content
def load_knowledge_base(file_path):
    """Loads text content from the knowledge base file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        st.error(f"Error: Knowledge base file not found at {file_path}")
        return None
    except Exception as e:
        st.error(f"Error loading knowledge base: {e}")
        return None

kb_text = load_knowledge_base(KB_FILE_PATH)
if not kb_text:
    st.stop()

# --- LLM Interaction Function ---
def get_answer_from_kb(question, context, model=MODEL_NAME):
    """Asks the LLM to answer a question based on provided context."""
    
    # Constructing a clear prompt is crucial
    system_prompt = "You are a helpful assistant answering questions based ONLY on the provided context. If the answer is not found in the context, say 'I cannot answer this question based on the provided context.' Do not make up information."
    user_prompt = f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.2, # Lower temperature for more factual answers based on context
            max_tokens=250 
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error querying OpenAI API: {e}")
        return "Sorry, an error occurred while trying to get an answer."

# --- Streamlit App UI ---
st.set_page_config(page_title="LLM Knowledge Base", layout="wide")
st.title("🤖 Interactive Knowledge Base")
st.write("Ask questions about the content loaded from the knowledge base file.")

# Display Knowledge Base Content (optional, good for demo)
st.divider()
with st.expander("View Knowledge Base Content"):
    st.markdown(kb_text)
st.divider()

# User Input
user_question = st.text_input("Ask your question:", key="user_query")

# Process Question and Display Answer
if user_question:
    st.write("Processing your question...")
    
    # Simple approach: Use the entire KB as context (works for small KBs)
    # For larger KBs, implement chunking and retrieval (e.g., using embeddings/FAISS/Chroma)
    # before passing relevant context to the LLM.
    context_to_use = kb_text 
    
    # Check if context is too large (very basic check, needs refinement for actual token limits)
    # A more robust check would use a tokenizer like tiktoken
    if len(context_to_use) > 12000: # Arbitrary character limit as proxy for tokens
         st.warning("Knowledge base is large. Using only the first 12,000 characters as context.")
         context_to_use = context_to_use[:12000]
         
    with st.spinner('Generating answer from knowledge base...'):
        answer = get_answer_from_kb(user_question, context_to_use)
        st.subheader("Answer:")
        st.markdown(answer)
else:
    st.info("Please enter a question above to query the knowledge base.")

# --- Footer / Info ---
st.divider()
st.caption(f"Powered by Streamlit and OpenAI ({MODEL_NAME}). Knowledge source: {KB_FILE_PATH}") 