# Google Gemini Prompts

This section provides examples and guidance for prompt engineering with Google's Gemini family of models.

## Key Considerations for Gemini Models

*   **Multimodality:** Gemini models are inherently multimodal, capable of understanding and processing information from text, images, audio, and video. Prompts can include these different types of content.
*   **Clarity and Context:** As with other LLMs, clear instructions and sufficient context are vital for good performance. Be specific about the task and the desired output.
*   **Safety Settings:** Gemini models have configurable safety settings to filter harmful content. Be aware of these settings and adjust them if necessary for your use case (though default settings are generally recommended).
*   **Instruction Following:** Gemini models are designed to follow instructions well. You can guide their behavior by clearly stating what you want them to do.
*   **Few-Shot Prompting:** Providing examples in your prompt (few-shot) can significantly improve performance on specific tasks or for desired output formats.
*   **Temperature and Top_p/Top_k:** These parameters control the randomness of the output. Use lower values for more deterministic responses and higher values for more creative or diverse outputs.
*   **Function Calling:** Gemini models support function calling, allowing them to interact with external tools and APIs, which can be integrated into prompts.

## Examples in `example_gemini_prompts.py`

The `example_gemini_prompts.py` script demonstrates:

1.  **Basic Text Generation:** A simple prompt to generate text based on an instruction.
2.  **Role-Playing/Persona Prompt:** Instructing Gemini to respond in a specific character or role.
3.  **Few-Shot Prompting (Q&A Format):** Providing examples to guide Gemini in answering questions based on a given context in a specific style.
4.  **Zero-Shot Task (Simple Classification):** Asking Gemini to classify text without explicit examples in the prompt, relying on its general knowledge.

*(Note: The current examples focus on text-only prompts. Multimodal prompting with Gemini typically involves using the SDK to send image/audio/video data alongside text.)*

## Setup

1.  **Navigate to this directory:**
    ```bash
    cd 05_Gemini_Prompts
    ```
2.  **Create your `.env` file:**
    Copy `env.example.txt` to `.env`:
    ```bash
    cp env.example.txt .env
    ```
3.  **Add your Google API Key:**
    Open the `.env` file and replace `"YOUR_GOOGLE_API_KEY_HERE"` with your actual Google API Key (often referred to as an API key for "Generative Language API" or similar, obtained from Google AI Studio or Google Cloud Console).
    ```env
    GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY_HERE"
    ```
4.  **Ensure you are in the parent virtual environment:**
    Make sure you have activated the virtual environment created in the `02_Prompt_Engineering` directory and installed the `requirements.txt` from there.

## Running the Examples

From within the `02_Prompt_Engineering/05_Gemini_Prompts/` directory, run:

```bash
python example_gemini_prompts.py
```
The script will execute each example prompt and print Gemini's response. 