import os
import pandas as pd
from dotenv import load_dotenv
from langchain.document_loaders import CSVLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Load environment variables from .env file
load_dotenv()

# Ensure your OPENAI_API_KEY is set in the .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please set it in the .env file.")

# --- Constants ---
FAQ_DATA_PATH = "data/faq.csv"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
VECTOR_STORE_PATH = "faiss_index_faq"
CHAT_MODEL_NAME = "gpt-3.5-turbo"

def load_and_process_data(data_path: str):
    """Loads FAQ data from a CSV file."""
    loader = CSVLoader(file_path=data_path, encoding="utf-8", csv_args={
        'delimiter': ',',
        'quotechar': '"',
        'fieldnames': ['Question', 'Answer']
    })
    documents = loader.load()
    print(f"Loaded {len(documents)} FAQ entries.")
    return documents

def create_vector_store(documents, embedding_model_name: str, vector_store_path: str):
    """Creates and saves a FAISS vector store from the documents."""
    print(f"Using embedding model: {embedding_model_name}")
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
    
    # Create FAISS vector store from documents
    print("Creating FAISS vector store...")
    vector_store = FAISS.from_documents(documents, embeddings)
    
    # Save the vector store locally
    vector_store.save_local(vector_store_path)
    print(f"Vector store saved to {vector_store_path}")
    return vector_store

def load_vector_store(embedding_model_name: str, vector_store_path: str):
    """Loads an existing FAISS vector store."""
    print(f"Loading vector store from {vector_store_path}...")
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
    vector_store = FAISS.load_local(vector_store_path, embeddings, allow_dangerous_deserialization=True)
    print("Vector store loaded successfully.")
    return vector_store

def setup_retrieval_qa_chain(llm_model_name: str, vector_store):
    """Sets up the RetrievalQA chain."""
    print(f"Using LLM: {llm_model_name}")
    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name=llm_model_name, temperature=0.7)

    # Define a prompt template
    prompt_template = """
    You are an AI assistant for answering questions based on the provided context.
    Answer the question based only on the following context. If you don't know the answer, just say that you don't know.
    Do not use any information outside of the provided context.

    Context:
    {context}

    Question: {question}

    Answer:
    """
    
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    chain_type_kwargs = {"prompt": PROMPT}
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={"k": 3}), # Retrieve top 3 relevant documents
        chain_type_kwargs=chain_type_kwargs,
        return_source_documents=True
    )
    print("RetrievalQA chain created.")
    return qa_chain

def ask_question(chain, query: str):
    """Asks a question to the QA chain and prints the response."""
    print(f"\nQuery: {query}")
    response = chain({"query": query})
    print(f"Answer: {response['result']}")
    
    # Optionally print source documents for verification
    # print("\nSource Documents:")
    # for doc in response.get('source_documents', []):
    #     print(f"- {doc.page_content}")
    return response

def main():
    """Main function to orchestrate the RAG chatbot setup and interaction."""
    print("Starting RAG FAQ Chatbot setup...")

    # Load FAQ data
    documents = load_and_process_data(FAQ_DATA_PATH)

    # Create or load vector store
    if not os.path.exists(VECTOR_STORE_PATH):
        print(f"No existing vector store found at {VECTOR_STORE_PATH}. Creating a new one.")
        vector_store = create_vector_store(documents, EMBEDDING_MODEL_NAME, VECTOR_STORE_PATH)
    else:
        vector_store = load_vector_store(EMBEDDING_MODEL_NAME, VECTOR_STORE_PATH)

    # Setup QA chain
    qa_chain = setup_retrieval_qa_chain(CHAT_MODEL_NAME, vector_store)

    print("\nRAG FAQ Chatbot is ready. Type 'exit' to quit.")
    print("-" * 30)

    # Interactive loop
    while True:
        user_query = input("Ask a question: ")
        if user_query.lower() == 'exit':
            print("Exiting chatbot. Goodbye!")
            break
        if user_query.strip():
            ask_question(qa_chain, user_query)
        else:
            print("Please enter a question.")

if __name__ == "__main__":
    main() 