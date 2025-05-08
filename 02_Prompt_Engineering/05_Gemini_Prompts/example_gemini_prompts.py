import os
import google.generativeai as genai
from dotenv import load_dotenv

# --- Configuration ---
ENV_FILE_PATH = ".env"

def load_api_key():
    """Loads Google API key from .env file in the current directory."""
    if not os.path.exists(ENV_FILE_PATH):
        print(f"Error: Environment file '{ENV_FILE_PATH}' not found in the current directory ('{os.getcwd()}').")
        print(f"Please create it by copying 'env.example.txt' to '.env' and adding your Google API key.")
        return None
    load_dotenv(dotenv_path=ENV_FILE_PATH)
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in .env file.")
        print("Please ensure your .env file contains: GOOGLE_API_KEY='your_key_here'")
        return None
    return api_key

# --- Google Gemini Client Initialization ---
api_key = load_api_key()
if not api_key:
    print("Exiting due to missing API key.")
    exit()

genai.configure(api_key=api_key)
# Model names: e.g., 'gemini-pro' for text-only, 'gemini-pro-vision' for multimodal
MODEL_NAME = "gemini-pro" 

# --- Helper Function to Interact with Gemini API ---
def get_gemini_response(prompt_text, model_name=MODEL_NAME, temperature=0.7, top_p=1.0, top_k=40, max_output_tokens=2048):
    """Gets a response from the Google Gemini API."""
    try:
        model = genai.GenerativeModel(model_name)
        generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            max_output_tokens=max_output_tokens
        )
        response = model.generate_content(prompt_text, generation_config=generation_config)
        # Handle potential lack of 'text' attribute if generation fails or is blocked
        if response.parts:
            return response.text
        else:
            # Try to get information from prompt_feedback if available
            feedback_info = "No specific feedback available."
            if hasattr(response, 'prompt_feedback') and response.prompt_feedback:
                feedback_info = str(response.prompt_feedback)
            return f"Content generation blocked or failed. Feedback: {feedback_info}"

    except Exception as e:
        return f"Error interacting with Gemini API: {e}"

# --- Prompt Examples ---

def example_basic_text_generation():
    """Example of basic text generation."""
    print("\n--- Example: Basic Text Generation (Gemini) ---")
    prompt = "Write a short, imaginative story about a robot who discovers a hidden garden on Mars."
    print(f"Prompt:\n{prompt}")
    response = get_gemini_response(prompt, max_output_tokens=300)
    print(f"Gemini Response:\n{response}")

def example_persona_prompting():
    """Example of persona prompting with Gemini."""
    print("\n--- Example: Persona Prompting (Gemini) ---")
    prompt = (
        "You are a historian specializing in ancient Rome. "
        "Describe the daily life of a Roman Centurion in the 1st century AD. "
        "Focus on their duties, living conditions, and challenges."
    )
    print(f"Prompt (with persona):\n{prompt}")
    response = get_gemini_response(prompt, max_output_tokens=400)
    print(f"Gemini Response (as Historian):\n{response}")

def example_few_shot_qa():
    """Example of few-shot prompting for context-based Q&A."""
    print("\n--- Example: Few-Shot Q&A (Gemini) ---")
    prompt = (
        "Answer the question based on the provided context. If the answer is not in the context, say 'I don\'t know.'\n\n"
        "Context: The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France. "
        "It is named after the engineer Gustave Eiffel, whose company designed and built the tower. "
        "Constructed from 1887 to 1889 as the entrance to the 1889 World's Fair, it was initially criticized by some of France's leading artists and intellectuals for its design, but it has become a global cultural icon of France and one of the most recognizable structures in the world.\n"
        "Question: Who designed the Eiffel Tower?\n"
        "Answer: Gustave Eiffel's company.\n\n"
        "Context: The Great Wall of China is a series of fortifications made of stone, brick, tamped earth, wood, and other materials, generally built along an east-to-west line across the historical northern borders of China to protect the Chinese states and empires against the raids and invasions of the various nomadic groups of the Eurasian Steppe.\n"
        "Question: What is the Great Wall of China made of?\n"
        "Answer: Stone, brick, tamped earth, wood, and other materials.\n\n"
        "Context: Photosynthesis is a process used by plants, algae, and certain bacteria to convert light energy into chemical energy, through a process that uses sunlight, water, and carbon dioxide. This chemical energy is stored in carbohydrate molecules, such as sugars, which are synthesized from carbon dioxide and water.\n"
        "Question: What is the capital of Japan?\n"
        "Answer: I don't know.\n\n"
        "Context: The Amazon rainforest is a moist broadleaf tropical rainforest in the Amazon biome that covers most of the Amazon basin of South America. This basin encompasses 7,000,000 km2 (2,700,000 sq mi), of which 5,500,000 km2 (2,100,000 sq mi) are covered by the rainforest.\n"
        "Question: How large is the Amazon rainforest?\n"
        "Answer:"
    )
    print(f"Prompt (Few-Shot Q&A):\n{prompt}")
    response = get_gemini_response(prompt, temperature=0.2, max_output_tokens=100)
    print(f"Gemini Response:\n{response}")

def example_zero_shot_classification():
    """Example of zero-shot text classification."""
    print("\n--- Example: Zero-Shot Classification (Gemini) ---")
    text_to_classify = "This new quantum computing breakthrough could revolutionize scientific research."
    prompt = (
        f"Classify the following text into one of these categories: Technology, Sports, Politics, or Health.\n\n"
        f"Text: '{text_to_classify}'\n\n"
        "Category:"
    )
    print(f"Prompt (Zero-Shot Classification):\n{prompt}")
    response = get_gemini_response(prompt, temperature=0.1, max_output_tokens=20)
    print(f"Gemini Response:\n{response}")

if __name__ == "__main__":
    print(f"Using Google Gemini Model: {MODEL_NAME}")
    example_basic_text_generation()
    example_persona_prompting()
    example_few_shot_qa()
    example_zero_shot_classification() 