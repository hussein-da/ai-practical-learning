# Conceptual Guide: Building an AI Chatbot in Bubble.io

This guide outlines the conceptual steps for building a simple AI-powered chatbot within the Bubble.io no-code platform, typically by integrating with an external AI API like OpenAI.

**Disclaimer:** This is a conceptual guide. The actual implementation involves using Bubble's visual editor, workflows, and plugins. No code files are provided here.

## Goal

To create a web page in Bubble with an input field where a user can type a message, and a display area where the AI's response appears.

## Key Bubble Concepts Used

*   **Design Tab:** For creating the user interface (input fields, buttons, text elements).
*   **Data Tab:** (Optional) For storing chat history if desired.
*   **Workflow Tab:** For defining the logic (e.g., what happens when the user clicks "Send").
*   **Plugins:** Specifically, the `API Connector` plugin to connect to external APIs (like OpenAI).

## Conceptual Steps

1.  **Set up Bubble Application:**
    *   Create a new application in Bubble ([https://bubble.io/](https://bubble.io/)).

2.  **Design the User Interface (Design Tab):**
    *   Add an `Input` element for the user to type their message.
    *   Add a `Button` element (e.g., labeled "Send" or "Ask").
    *   Add a `Text` element or a `Repeating Group` element to display the chat conversation (user messages and AI responses).
    *   (Optional) Use `Custom States` on the page element to temporarily store the conversation history or the latest AI response.

3.  **Configure the API Connector Plugin:**
    *   Go to the **Plugins** tab and add the `API Connector` plugin if it's not already installed.
    *   Configure a new API connection:
        *   **API Name:** e.g., "OpenAI API"
        *   **Authentication:** Set up authentication for your chosen AI provider (e.g., for OpenAI, use `Private key in header` with `Authorization: Bearer YOUR_OPENAI_API_KEY`). Remember to keep your API key secure and use Bubble's private key settings.
    *   Define a specific API call within this connection:
        *   **Name:** e.g., "Chat Completion"
        *   **Use as:** `Action` (since it will be triggered by a workflow).
        *   **Method:** `POST`
        *   **URL:** The endpoint URL for your AI provider's chat completion API (e.g., `https://api.openai.com/v1/chat/completions`).
        *   **Headers:** Include `Content-Type: application/json` and the `Authorization` header.
        *   **Body (JSON):** Define the JSON structure required by the API. Make parts dynamic using `<>` syntax. Example for OpenAI:
            ```json
            {
              "model": "gpt-3.5-turbo",
              "messages": [
                {"role": "system", "content": "You are a helpful assistant."}, 
                {"role": "user", "content": "<user_message>"} 
              ],
              "temperature": 0.7
            }
            ```
            *   Mark `user_message` as non-private so you can set it dynamically in the workflow.
            *   Initialize the call by providing a sample value for `<user_message>` and clicking "Initialize Call" to ensure Bubble understands the API response structure.

4.  **Create the Workflow (Workflow Tab):**
    *   Select the "Send" button and click "Start/Edit workflow".
    *   **Action 1:** Add an action `Plugins -> OpenAI API - Chat Completion` (or whatever you named your API call).
        *   In the action properties, set the dynamic `user_message` value to be the `Input element's value`.
    *   **Action 2:** (Optional) Add the user's message to the display. This could involve:
        *   Adding the input value to a custom state list (if using custom states for the conversation).
        *   Creating a new entry in the database (if storing history in the Data tab).
    *   **Action 3:** Display the AI's response. This depends on how you choose to display:
        *   If using custom states: Set a custom state (e.g., `latest_ai_response`) to `Result of step 1 (API Call)'s body.choices[0].message.content` (adjust based on the actual API response structure Bubble parsed).
        *   If using database: Create a new entry with the AI's response.
        *   Update the `Text` element or `Repeating Group` data source to reflect the new state or data.
    *   **Action 4:** (Optional) Clear the user's input field.

5.  **Testing and Iteration:**
    *   Preview your Bubble application.
    *   Type a message and click "Send".
    *   Use Bubble's debugger to inspect workflow steps and API responses if it doesn't work as expected.
    *   Refine the UI, workflow logic, and API call parameters as needed.

## Further Learning

*   **Bubble Documentation:** [https://manual.bubble.io/](https://manual.bubble.io/)
*   **Bubble API Connector Guide:** [https://manual.bubble.io/core-resources/bubble-made-plugins/api-connector](https://manual.bubble.io/core-resources/bubble-made-plugins/api-connector)
*   Search for Bubble tutorials on YouTube related to "OpenAI integration" or "building AI chatbot".

This guide provides a high-level overview. The specific clicks and settings within Bubble require navigating its interface. 