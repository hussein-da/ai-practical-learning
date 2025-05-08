# 06: Comparative Prompt Examples (GPT-4, Claude, Gemini)

This section provides a comparative look at how one might approach prompting for a similar task across GPT-4, Claude, and Gemini. The goal is to highlight potential differences in prompt structure or emphasis based on the known characteristics and recommended practices for each model.

**Disclaimer:**
*   LLM performance can vary based on the specific version, API parameters, and the exact phrasing of the prompt.
*   These are illustrative examples; optimal prompts often require iteration and testing for your specific use case.
*   The fundamental principles of clarity, context, and specificity apply to all models.

## Task: Extracting Structured Information from Text

**Goal:** Extract the name of a product, its price, and a list of key features from a block of unstructured text. The output should be a JSON object.

**Input Text (Common for all examples):**

```text
Check out the brand new "Galactic Zoomer X5000" drone! It boasts an incredible 50-minute flight time, a 4K HDR camera, and advanced obstacle avoidance sensors. Perfect for professionals and hobbyists alike. Get yours today for only $799.99!
```

--- 

### GPT-4 Approach

GPT-4 is highly capable with instruction following and can often infer structure well. A system message can be used effectively to set the stage.

**Prompt Structure (Chat Completions API):**

```
System:
You are an AI assistant that excels at extracting structured information from text and formatting it as JSON.

User:
Extract the product name, price, and key features from the following text. The price should be a string, and key features should be a list of strings.

Text:
"""
Check out the brand new "Galactic Zoomer X5000" drone! It boasts an incredible 50-minute flight time, a 4K HDR camera, and advanced obstacle avoidance sensors. Perfect for professionals and hobbyists alike. Get yours today for only $799.99!
"""

Desired JSON Output Structure:
{
  "product_name": "<name>",
  "price": "<price>",
  "key_features": ["<feature1>", "<feature2>", ...]
}
```

**Expected Output (Conceptual):**
```json
{
  "product_name": "Galactic Zoomer X5000",
  "price": "$799.99",
  "key_features": ["50-minute flight time", "4K HDR camera", "advanced obstacle avoidance sensors"]
}
```

**Rationale for GPT-4:**
*   Clear instruction in the user message.
*   System message sets the AI's role and capability.
*   Providing the desired JSON structure as an example in the prompt helps ensure compliance.

--- 

### Claude Approach

Claude responds well to XML-tagged structures, which clearly delineate instructions, input text, and desired output format.

**Prompt Structure (Emphasis on XML):**

```xml
<instructions>
Your task is to extract the product name, price, and key features from the provided text. 
The output must be a valid JSON object with the following keys:
- "product_name" (string)
- "price" (string)
- "key_features" (list of strings)
</instructions>

<text_to_analyze>
Check out the brand new "Galactic Zoomer X5000" drone! It boasts an incredible 50-minute flight time, a 4K HDR camera, and advanced obstacle avoidance sensors. Perfect for professionals and hobbyists alike. Get yours today for only $799.99!
</text_to_analyze>

<json_output_example>
<!-- This is an example of the desired output structure, not the actual output for the text_to_analyze -->
{
  "product_name": "Example Product",
  "price": "$0.00",
  "key_features": ["Sample Feature 1", "Sample Feature 2"]
}
</json_output_example>

<final_json_output>
</final_json_output>
```

**Expected Output (Conceptual - Claude would fill `<final_json_output>`):**
```json
{
  "product_name": "Galactic Zoomer X5000",
  "price": "$799.99",
  "key_features": ["50-minute flight time", "4K HDR camera", "advanced obstacle avoidance sensors"]
}
```

**Rationale for Claude:**
*   Heavy use of XML tags (`<instructions>`, `<text_to_analyze>`, `<json_output_example>`, `<final_json_output>`) for clarity, as recommended by Anthropic.
*   Explicitly stating the output must be a *valid* JSON object.
*   Providing an example of the JSON structure within tags.

--- 

### Gemini Approach

Gemini models are also strong at instruction following and structured data generation. Similar to GPT-4, clarity and examples are key. For text-only tasks, the approach is similar to other advanced LLMs. If this were a multimodal task (e.g., extracting info from an image of a product box and its text), the prompt would include image data.

**Prompt Structure (Conceptual):**

```
User:
From the text below, extract the product name, its price, and a list of its key features.
Format the output as a JSON object where the product name and price are strings, and key features is a list of strings.

Text Input:
"""
Check out the brand new "Galactic Zoomer X5000" drone! It boasts an incredible 50-minute flight time, a 4K HDR camera, and advanced obstacle avoidance sensors. Perfect for professionals and hobbyists alike. Get yours today for only $799.99!
"""

Example JSON Output:
```json
{
  "product_name": "Sample Drone Pro",
  "price": "$123.45",
  "key_features": ["Long battery", "HD Camera", "GPS"]
}
```

Actual JSON Output:
```json
{ // Gemini would generate the actual JSON here
```

**Expected Output (Conceptual):**
```json
{
  "product_name": "Galactic Zoomer X5000",
  "price": "$799.99",
  "key_features": ["50-minute flight time", "4K HDR camera", "advanced obstacle avoidance sensors"]
}
```

**Rationale for Gemini:**
*   Clear and direct instruction.
*   Providing the input text clearly delineated.
*   Including an example of the desired JSON output to guide the model, followed by a clear spot for the actual output.
*   If an image of the drone box were provided, the prompt would include that data and the instructions might ask to correlate text features with visual elements.

--- 

## Key Takeaways from Comparison

*   **Core Principles:** All models benefit from clear instructions, context, and examples of the desired output.
*   **Model-Specific Structuring:**
    *   **Claude:** Shows a preference for XML-tagged structures for clarity.
    *   **GPT-4:** Works well with system messages for role-setting and clear user instructions.
    *   **Gemini:** Handles direct instructions well; prompt structure can easily incorporate multimodal data when applicable.
*   **Output Formatting:** Explicitly defining the desired output format (especially for structured data like JSON) is crucial for all models. Providing an example of the structure is a good practice.
*   **Iteration:** Regardless of the model, expect to iterate on your prompts to achieve optimal results for your specific task.

This comparative example should give you a starting point for adapting your prompting strategies based on the LLM you are working with. 