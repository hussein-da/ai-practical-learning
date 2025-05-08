# OpenAI GPT Prompts

This section provides examples and guidance for prompt engineering with OpenAI's GPT (Generative Pre-trained Transformer) models, such as GPT-3.5-turbo and GPT-4.

## Key Considerations for GPT Models

*   **System Message:** GPT models (especially chat-based ones like `gpt-3.5-turbo` and `gpt-4`) benefit from a "system" message that sets the overall behavior, persona, or context for the AI. This is often the first message in a chat sequence.
*   **User Message:** This is the main input or question from the user.
*   **Assistant Message:** This is where the model's response would go. In few-shot prompting, you can provide example assistant messages.
*   **Clarity and Detail:** Be explicit. The more detailed your prompt, the better the model can understand your intent.
*   **Iterative Refinement:** Start simple and iteratively add complexity or constraints to your prompt as you test and observe responses.
*   **Temperature and Top_p:** These parameters control the randomness and creativity of the response. Lower values (e.g., temperature 0.2) make the output more focused and deterministic, while higher values (e.g., temperature 0.8) make it more random and creative.

## Examples in `example_gpt_prompts.py`

The `example_gpt_prompts.py` script demonstrates:

1.  **Basic Instruction Following:** A simple prompt asking the model to perform a straightforward task.
2.  **Persona Prompting:** Instructing the model to adopt a specific persona.
3.  **Few-Shot Prompting:** Providing a couple of examples within the prompt to guide the model's response format and content for a custom task.
4.  **Text Summarization (Zero-Shot):** Asking the model to summarize a piece of text.

## Setup

1.  **Navigate to this directory:**
    ```bash
    cd 03_GPT_Prompts
    ```
2.  **Create your `.env` file:**
    Copy `env.example.txt` to `.env`:
    ```bash
    cp env.example.txt .env
    ```
3.  **Add your OpenAI API Key:**
    Open the `.env` file and replace `"YOUR_OPENAI_API_KEY_HERE"` with your actual OpenAI API key.
    ```env
    OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ```
4.  **Ensure you are in the parent virtual environment:**
    Make sure you have activated the virtual environment created in the `02_Prompt_Engineering` directory and installed the `requirements.txt` from there.

## Running the Examples

From within the `02_Prompt_Engineering/03_GPT_Prompts/` directory, run:

```bash
python example_gpt_prompts.py
```
The script will execute each example prompt and print the LLM's response. 