import os
import anthropic
from dotenv import load_dotenv

# --- Configuration ---
ENV_FILE_PATH = ".env"

def load_api_key():
    """Loads Anthropic API key from .env file in the current directory."""
    if not os.path.exists(ENV_FILE_PATH):
        print(f"Error: Environment file '{ENV_FILE_PATH}' not found in the current directory ('{os.getcwd()}').")
        print(f"Please create it by copying 'env.example.txt' to '.env' and adding your Anthropic API key.")
        return None
    load_dotenv(dotenv_path=ENV_FILE_PATH)
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not found in .env file.")
        print("Please ensure your .env file contains: ANTHROPIC_API_KEY='your_key_here'")
        return None
    return api_key

# --- Anthropic Client Initialization ---
api_key = load_api_key()
if not api_key:
    print("Exiting due to missing API key.")
    exit()

client = anthropic.Anthropic(api_key=api_key)
# Recommended models: "claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"
# Using Haiku for cost-effectiveness in examples.
MODEL_NAME = "claude-3-haiku-20240307" 

# --- Helper Function to Interact with Anthropic API ---
def get_claude_response(prompt_content, model=MODEL_NAME, max_tokens=1024, temperature=0.7):
    """Gets a response from the Anthropic Messages API."""
    try:
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[
                {
                    "role": "user",
                    "content": prompt_content
                }
            ]
        )
        return response.content[0].text
    except Exception as e:
        return f"Error interacting with Anthropic API: {e}"

# --- Prompt Examples ---

def example_basic_instruction():
    """Example of a basic instruction-following prompt."""
    print("\n--- Example: Basic Instruction Following (Claude) ---")
    # Claude expects the prompt to end with "Assistant:" to start generation,
    # but for the Messages API, we provide the full user content.
    prompt = "Human: Please tell me the capital of France.\n\nAssistant:"
    # For the Messages API, the user content is just the human part.
    user_content = "Please tell me the capital of France."
    
    print(f"User Content:\n{user_content}")
    response = get_claude_response(user_content)
    print(f"Claude Response:\n{response}")

def example_persona_prompting():
    """Example of persona prompting with Claude."""
    print("\n--- Example: Persona Prompting (Claude) ---")
    user_content = (
        "Human: You are a seasoned travel guide with a poetic flair. "
        "Describe the experience of watching a sunset over the Grand Canyon. "
        "Make it vivid and inspiring.\n\n"
        "Assistant:"
    )
    # For Messages API, user content is the Human turn. We can include the role definition in the user message.
    user_content_for_api = (
        "You are a seasoned travel guide with a poetic flair. "
        "Describe the experience of watching a sunset over the Grand Canyon. "
        "Make it vivid and inspiring."
    )
    print(f"User Content (with persona):\n{user_content_for_api}")
    response = get_claude_response(user_content_for_api, max_tokens=300)
    print(f"Claude Response (as Poetic Travel Guide):\n{response}")

def example_few_shot_prompting_xml():
    """Example of few-shot prompting for product category classification using XML tags."""
    print("\n--- Example: Few-Shot Prompting with XML (Claude) ---")
    user_content = (
        "You are a product categorization assistant. Your task is to classify products into given categories. "
        "Use the provided examples to understand the format.\n\n"
        "<examples>\n"
        "  <example>\n"
        "    <product_description>High-performance gaming laptop with RTX 4090</product_description>\n"
        "    <category>Electronics - Computers</category>\n"
        "  </example>\n"
        "  <example>\n"
        "    <product_description>Organic cotton t-shirt, soft and breathable</product_description>\n"
        "    <category>Apparel - Casual</category>\n"
        "  </example>\n"
        "  <example>\n"
        "    <product_description>'The Midnight Library' - a novel by Matt Haig</product_description>\n"
        "    <category>Books - Fiction</category>\n"
        "  </example>\n"
        "</examples>\n\n"
        "Now, classify the following product:\n"
        "<product_to_classify>\n"
        "  <product_description>Stainless steel chef\'s knife, 8-inch blade</product_description>\n"
        "</product_to_classify>\n\n"
        "Please provide only the category as the output."
    )
    # The full prompt including instructions and examples is the user_content
    print(f"User Content (with XML examples):\n{user_content}")
    response = get_claude_response(user_content, temperature=0.1, max_tokens=50)
    print(f"Claude Response:\n{response}")

def example_text_summarization_xml():
    """Example of zero-shot text summarization with XML tags for structure."""
    print("\n--- Example: Text Summarization with XML (Claude) ---")
    document_text = ( """
    Artificial intelligence (AI) is rapidly transforming various sectors, from healthcare to finance and entertainment. 
    Machine learning, a subset of AI, enables systems to learn from data and improve their performance over time without being explicitly programmed. 
    Deep learning, a further specialization, utilizes neural networks with many layers to analyze complex patterns in large datasets. 
    These technologies power applications like image recognition, natural language processing, and autonomous vehicles. 
    However, the development of AI also raises ethical considerations regarding bias, privacy, and job displacement, which require careful attention and regulation.
    """
    )
    user_content = (
        "Please summarize the following document into two key bullet points. "
        "The summary should be concise and capture the main essence of the text.\n\n"
        "<document_to_summarize>\n"
        f"{document_text}\n"
        "</document_to_summarize>\n\n"
        "<summary_instructions>Output format: Two bullet points, each starting with '*'.</summary_instructions>"
    )
    print(f"User Content for Summarization (with XML):\n{user_content}")
    response = get_claude_response(user_content, max_tokens=150)
    print(f"Claude Response (Summary):\n{response}")

if __name__ == "__main__":
    print(f"Using Anthropic Model: {MODEL_NAME}")
    example_basic_instruction()
    example_persona_prompting()
    example_few_shot_prompting_xml()
    example_text_summarization_xml() 