# Anthropic Claude Prompts

This section provides examples and guidance for prompt engineering with Anthropic's Claude models.

## Key Considerations for Claude Models

*   **User and Assistant Turns:** Claude is typically prompted using a sequence of "Human:" (or "User:") and "Assistant:" turns. The prompt should end with an "Assistant:" turn to signal Claude to start generating its response.
*   **Clarity and Explicitness:** Like other LLMs, Claude benefits from clear, direct, and unambiguous instructions. Provide as much context as necessary.
*   **Role Playing:** You can instruct Claude to adopt a specific persona or role by defining it in the initial part of your prompt.
*   **XML Tags:** Claude responds well to prompts structured with XML tags to delineate different parts of the input, instructions, or examples. For instance, you can use `<document>`, `<question>`, `<examples>`, `<instructions>` tags.
*   **Few-Shot Examples:** Providing examples directly within the prompt is highly effective. Structure these examples clearly, often using the "Human:" and "Assistant:" format.
*   **Think Step-by-Step:** For complex reasoning, you can ask Claude to "think step by step" or to output its reasoning process before the final answer. Sometimes enclosing this request in XML tags like `<thinking_process>` can be beneficial.
*   **Max Tokens:** Be mindful of `max_tokens_to_sample` to ensure Claude has enough room to generate a complete response.

## Examples in `example_claude_prompts.py`

The `example_claude_prompts.py` script demonstrates:

1.  **Basic Instruction Following:** A simple prompt for a direct task.
2.  **Role-Playing/Persona Prompt:** Instructing Claude to respond as a specific character.
3.  **Few-Shot Prompting with XML Structure:** Using XML tags to structure a few-shot classification task.
4.  **Text Summarization (Zero-Shot):** Asking Claude to summarize a given text, with instructions for the output format.

## Setup

1.  **Navigate to this directory:**
    ```bash
    cd 04_Claude_Prompts
    ```
2.  **Create your `.env` file:**
    Copy `env.example.txt` to `.env`:
    ```bash
    cp env.example.txt .env
    ```
3.  **Add your Anthropic API Key:**
    Open the `.env` file and replace `"YOUR_ANTHROPIC_API_KEY_HERE"` with your actual Anthropic API key.
    ```env
    ANTHROPIC_API_KEY="sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ```
4.  **Ensure you are in the parent virtual environment:**
    Make sure you have activated the virtual environment created in the `02_Prompt_Engineering` directory and installed the `requirements.txt` from there.

## Running the Examples

From within the `02_Prompt_Engineering/04_Claude_Prompts/` directory, run:

```bash
python example_claude_prompts.py
```
The script will execute each example prompt and print Claude's response. 