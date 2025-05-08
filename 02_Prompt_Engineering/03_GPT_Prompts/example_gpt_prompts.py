import os
from openai import OpenAI
from dotenv import load_dotenv

# --- Configuration ---
ENV_FILE_PATH = ".env"

def load_api_key():
    """Loads OpenAI API key from .env file in the current directory."""
    if not os.path.exists(ENV_FILE_PATH):
        print(f"Error: Environment file '{ENV_FILE_PATH}' not found in the current directory ('{os.getcwd()}').")
        print(f"Please create it by copying 'env.example.txt' to '.env' and adding your OpenAI API key.")
        return None
    load_dotenv(dotenv_path=ENV_FILE_PATH)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found in .env file.")
        print("Please ensure your .env file contains: OPENAI_API_KEY='your_key_here'")
        return None
    return api_key

# --- OpenAI Client Initialization ---
api_key = load_api_key()
if not api_key:
    print("Exiting due to missing API key.")
    exit()

client = OpenAI(api_key=api_key)
MODEL_NAME = "gpt-3.5-turbo" # You can change to "gpt-4" if you have access

# --- Helper Function to Interact with OpenAI API ---
def get_gpt_response(messages, model=MODEL_NAME, temperature=0.7, max_tokens=150):
    """Gets a response from the OpenAI Chat API."""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error interacting with OpenAI API: {e}"

# --- Prompt Examples ---

def example_basic_instruction():
    """Example of a basic instruction-following prompt."""
    print("\n--- Example: Basic Instruction Following ---")
    prompt_text = "Translate the following English text to French: 'Hello, how are you today?'"
    messages = [
        {"role": "system", "content": "You are a helpful translation assistant."},
        {"role": "user", "content": prompt_text}
    ]
    print(f"User Prompt:\n{prompt_text}")
    response = get_gpt_response(messages)
    print(f"GPT Response:\n{response}")

def example_persona_prompting():
    """Example of persona prompting."""
    print("\n--- Example: Persona Prompting ---")
    system_persona = "You are a cheerful pirate captain who loves to talk about treasure and adventure. You end your sentences with 'Ahoy!' or 'Matey!'"
    user_query = "Tell me a short story about finding a hidden island."
    messages = [
        {"role": "system", "content": system_persona},
        {"role": "user", "content": user_query}
    ]
    print(f"System Persona:\n{system_persona}")
    print(f"User Query:\n{user_query}")
    response = get_gpt_response(messages, max_tokens=200)
    print(f"GPT Response (as Pirate Captain):\n{response}")

def example_few_shot_prompting():
    """Example of few-shot prompting for sentiment classification."""
    print("\n--- Example: Few-Shot Prompting (Sentiment Classification) ---")
    user_prompt = (
        "Classify the sentiment of the following movie reviews as Positive, Negative, or Neutral.\n\n" \
        "Review: 'This movie was an absolute masterpiece! The acting, plot, and cinematography were all superb.'\n" \
        "Sentiment: Positive\n\n" \
        "Review: 'I was really bored throughout the entire film. Not recommended.'\n" \
        "Sentiment: Negative\n\n" \
        "Review: 'The movie was okay, had some good parts and some slow parts.'\n" \
        "Sentiment: Neutral\n\n" \
        "Review: 'What a fantastic and uplifting story! I loved every minute of it.'\n" \
        "Sentiment:"
    )
    messages = [
        {"role": "system", "content": "You are a highly accurate sentiment classification assistant."},
        {"role": "user", "content": user_prompt}
    ]
    print(f"User Prompt (with examples):\n{user_prompt}")
    response = get_gpt_response(messages, temperature=0.2, max_tokens=10) # Low temp for classification
    print(f"GPT Response:\n{response}")

def example_text_summarization():
    """Example of zero-shot text summarization."""
    print("\n--- Example: Text Summarization (Zero-Shot) ---")
    long_text = ( """
    The Industrial Revolution, which took place from the 18th to 19th centuries, was a period during which predominantly agrarian, rural societies in Europe and America became industrial and urban. 
    Prior to the Industrial Revolution, manufacturing was often done in people's homes, using hand tools or basic machines. Industrialization marked a shift to powered, special-purpose machinery, factories and mass production. 
    The iron and textile industries, along with the development of the steam engine, played central roles in the Industrial Revolution. It also saw improved systems of transportation, communication and banking. 
    While industrialization brought about an increased volume and variety of manufactured goods and an improved standard of living for some, it also resulted in often grim employment and living conditions for the poor and working classes.
    """
    )
    prompt_text = f"Summarize the following text in one concise sentence:\n\nText:\n{long_text}\n\nSummary:"
    messages = [
        {"role": "system", "content": "You are an expert in text summarization, skilled at extracting the core message concisely."},
        {"role": "user", "content": prompt_text}
    ]
    print(f"User Prompt for Summarization:\n{prompt_text}")
    response = get_gpt_response(messages, max_tokens=80)
    print(f"GPT Response (Summary):\n{response}")

if __name__ == "__main__":
    print(f"Using OpenAI Model: {MODEL_NAME}")
    example_basic_instruction()
    example_persona_prompting()
    example_few_shot_prompting()
    example_text_summarization() 