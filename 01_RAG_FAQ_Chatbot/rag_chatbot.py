import os
import pandas as pd
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# --- Configuration ---
DATA_FILE = "data/faq.csv"
ENV_FILE_PATH = ".env" # Path to the .env file

# --- Helper Functions ---

def load_api_key():
    """Loads OpenAI API key from .env file."""
    if not os.path.exists(ENV_FILE_PATH):
        print(f"Error: Environment file '{ENV_FILE_PATH}' not found.")
        print("Please create it by copying 'env.example.txt' to '.env' and adding your OpenAI API key.")
        return None
    load_dotenv(dotenv_path=ENV_FILE_PATH)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found in .env file.")
        print("Please ensure your .env file contains: OPENAI_API_KEY='your_key_here'")
        return None
    return api_key

def load_faqs(file_path):
    """Loads FAQs from a CSV file."""
    try:
        df = pd.read_csv(file_path)
        if 'Question' not in df.columns or 'Answer' not in df.columns:
            print("Error: CSV file must contain 'Question' and 'Answer' columns.")
            return None
        # Combine Question and Answer for better embedding context if desired,
        # or just use Questions for retrieval and then show the Answer.
        # For this example, we'll embed questions and retrieve answers.
        # We'll store Q&A pairs for context in the document metadata.
        faqs = [{"question": row["Question"], "answer": row["Answer"]} for index, row in df.iterrows()]
        print(f"Loaded {len(faqs)} FAQs from {file_path}")
        return faqs
    except FileNotFoundError:
        print(f"Error: FAQ file not found at {file_path}")
        return None
    except Exception as e:
        print(f"Error loading FAQs: {e}")
        return None

def create_vector_store(faqs, api_key):
    """Creates a FAISS vector store from FAQ questions."""
    if not faqs:
        return None
    try:
        embeddings = OpenAIEmbeddings(openai_api_key=api_key)
        # We embed the questions to find relevant FAQs
        texts = [faq["question"] for faq in faqs]
        # We store the full FAQ (Q&A) as metadata to be retrieved.
        # Langchain's FAISS implementation uses Document objects.
        # We can create Document objects with page_content=question and metadata=faq_item
        from langchain.docstore.document import Document
        documents = []
        for i, faq_item in enumerate(faqs):
            documents.append(Document(page_content=faq_item["question"], metadata={"answer": faq_item["answer"], "source": f"FAQ #{i+1}"}))
        
        print("Creating vector store...")
        vector_store = FAISS.from_documents(documents, embeddings)
        print("Vector store created successfully.")
        return vector_store
    except Exception as e:
        print(f"Error creating vector store: {e}")
        return None

def initialize_qa_chain(vector_store, api_key):
    """Initializes the RetrievalQA chain."""
    if not vector_store:
        return None
    try:
        llm = ChatOpenAI(openai_api_key=api_key, model_name="gpt-3.5-turbo", temperature=0.7)
        
        # Define a custom prompt template
        prompt_template = """Use the following pieces of context (FAQs) to answer the question at the end.
If you don't know the answer from the provided context, just say that you don't know, don't try to make up an answer.
Keep the answer concise and directly based on the retrieved FAQ. If an FAQ directly answers the question, primarily use its answer.

Context (FAQs):
{context}

Question: {question}

Helpful Answer:"""
        QA_CHAIN_PROMPT = PromptTemplate(
            input_variables=["context", "question"],
            template=prompt_template,
        )
        
        qa_chain = RetrievalQA.from_chain_type(
            llm,
            retriever=vector_store.as_retriever(),
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
            return_source_documents=True # To see which FAQ was retrieved
        )
        print("RAG QA chain initialized.")
        return qa_chain
    except Exception as e:
        print(f"Error initializing QA chain: {e}")
        return None

def ask_question(qa_chain):
    """Handles the user interaction loop for asking questions."""
    print("\n--- RAG FAQ Chatbot ---")
    print("Ask a question about the FAQs, or type 'exit' or 'quit' to leave.")
    while True:
        user_query = input("\nYour Question: ")
        if user_query.lower() in ["exit", "quit"]:
            print("Exiting chatbot. Goodbye!")
            break
        if not user_query.strip():
            print("Please enter a question.")
            continue

        try:
            print("Searching for answer...")
            result = qa_chain({"query": user_query})
            
            answer = result.get("result", "No answer found.")
            source_docs = result.get("source_documents")

            print(f"\nAnswer: {answer}")
            if source_docs:
                print("\nSources (Retrieved FAQs):")
                for doc in source_docs:
                    # The 'answer' is stored in metadata
                    retrieved_question = doc.page_content
                    retrieved_answer = doc.metadata.get('answer', 'N/A')
                    source_info = doc.metadata.get('source', 'N/A')
                    print(f"  - Source: {source_info}")
                    print(f"    Retrieved Question: {retrieved_question}")
                    print(f"    Retrieved Answer: {retrieved_answer}")
            else:
                print("  No specific source documents were retrieved by the chain.")
                
        except Exception as e:
            print(f"Error processing your question: {e}")

# --- Main Application Logic ---
def main():
    """Main function to run the RAG chatbot."""
    print("Initializing RAG FAQ Chatbot...")
    
    api_key = load_api_key()
    if not api_key:
        return # API key loading failed, messages already printed

    faqs = load_faqs(DATA_FILE)
    if not faqs:
        return # FAQ loading failed

    vector_store = create_vector_store(faqs, api_key)
    if not vector_store:
        return # Vector store creation failed

    qa_chain = initialize_qa_chain(vector_store, api_key)
    if not qa_chain:
        return # QA chain initialization failed

    ask_question(qa_chain)

if __name__ == "__main__":
    main() 