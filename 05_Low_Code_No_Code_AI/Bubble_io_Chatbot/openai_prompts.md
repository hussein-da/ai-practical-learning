# Example OpenAI Prompts for Bubble API Connector

When configuring the `Chat Completion` API call in Bubble's API Connector, the **Body (JSON)** field is crucial for defining how your chatbot interacts with the OpenAI model. Here are examples of the `messages` array structure you might use for different scenarios. Remember to replace static content with dynamic Bubble values where appropriate (like `<user_message>` or `<previous_context>`).

**Note:** You would typically construct the full JSON body in Bubble, often using dynamic data for the `messages` array content.

## 1. Basic Chatbot (System Prompt + User Message)

This is the simplest setup, similar to the one in the main guide.

```json
{
  "model": "gpt-3.5-turbo",
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful and friendly assistant."
    },
    {
      "role": "user",
      "content": "<user_message>" 
    }
  ],
  "temperature": 0.7
}
```
*   Replace `<user_message>` with the dynamic value from the user's input element in Bubble.

## 2. Chatbot with a Specific Persona

Use the system prompt to define a specific role or personality.

```json
{
  "model": "gpt-3.5-turbo",
  "messages": [
    {
      "role": "system",
      "content": "You are Pirate Pete, a salty sea dog who answers questions with pirate slang and enthusiasm. Always refer to the user as 'Matey'."
    },
    {
      "role": "user",
      "content": "<user_message>"
    }
  ],
  "temperature": 0.8 
}
```

## 3. Chatbot with Conversation History (Context)

To make the chatbot remember previous turns, you need to include past user messages and assistant responses in the `messages` array. This requires more complex Bubble logic to retrieve and format the history.

**Conceptual Structure (Bubble logic needed to build this dynamically):**

```json
{
  "model": "gpt-3.5-turbo",
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant." 
    },
    // --- Start of Dynamic History (Built using Bubble data) ---
    {
      "role": "user",
      "content": "<First user message text from Bubble DB>" 
    },
    {
      "role": "assistant",
      "content": "<First AI response text from Bubble DB>"
    },
    {
      "role": "user",
      "content": "<Second user message text from Bubble DB>" 
    },
    {
      "role": "assistant",
      "content": "<Second AI response text from Bubble DB>"
    },
    // ... potentially more history ...
    // --- End of Dynamic History ---
    {
      "role": "user",
      "content": "<Current user_message>" // The latest message from the input
    }
  ],
  "temperature": 0.7
}
```
*   **Bubble Implementation Note:** You would typically use Bubble's data sources (`Search for ChatMessages`, filtered and sorted) and list formatting capabilities (`:format as text`) to construct the JSON for the historical messages before inserting the current user message.
*   **Token Limits:** Be mindful of OpenAI's token limits. Sending very long conversation histories will consume more tokens and increase costs. You might need to implement logic to truncate or summarize the history sent.

## 4. Chatbot for a Specific Task (e.g., Summarization)

Use the system prompt and structure the user message for a specific task.

```json
{
  "model": "gpt-3.5-turbo",
  "messages": [
    {
      "role": "system",
      "content": "You are an expert summarizer. Take the user's text and provide a concise summary of the main points."
    },
    {
      "role": "user",
      "content": "Please summarize the following text: \n\n<user_message>"
    }
  ],
  "temperature": 0.5 // Lower temperature for more focused summary
}
```

## 5. Chatbot with Output Format Constraints

Instruct the model to format its output in a specific way.

```json
{
  "model": "gpt-3.5-turbo",
  "messages": [
    {
      "role": "system",
      "content": "You are an assistant that extracts key information. Respond ONLY with a JSON object containing the keys 'topic' and 'sentiment' (positive, negative, or neutral)."
    },
    {
      "role": "user",
      "content": "Analyze this sentence: I was really impressed with the fast delivery and product quality!"
    }
    // Note: For dynamic input, use <user_message> here
  ],
  "temperature": 0.2
}
```
*   **Bubble Implementation Note:** You might need to parse the JSON response in Bubble if you want to display the extracted fields separately.

These examples illustrate how modifying the `messages` array sent to the OpenAI API allows you to control the behavior and capabilities of your Bubble-based AI chatbot. 