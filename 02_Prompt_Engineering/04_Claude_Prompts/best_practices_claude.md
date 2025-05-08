# Claude: Best Practices and Nuanced Techniques

Beyond the common task examples, this document outlines specific best practices and nuanced techniques for getting the most out of Anthropic's Claude models. These are often highlighted in Anthropic's own recommendations and by experienced users.

## 1. Leverage XML Tags for Structure and Clarity

As demonstrated in `common_tasks.md`, using XML-like tags to structure your prompts is highly recommended for Claude. This helps the model clearly distinguish between different parts of your input, such as instructions, context, examples, and the specific question or data to process.

*   **Commonly Used Tags:** `<instructions>`, `<document>`, `<text_to_analyze>`, `<question>`, `<user_input>`, `<example>`, `<context>`, `<role>`, `<output_format>`, etc. You can define your own meaningful tags.
*   **Why it Works:** It provides a clear, machine-readable structure that Claude is trained to recognize and utilize effectively, reducing ambiguity.

**Example: Complex Instruction Set**
```xml
<instructions>
Your task is to analyze the provided customer review and perform the following actions:
1.  Identify the main product mentioned.
2.  Extract up to three key positive points the customer made.
3.  Extract up to three key negative points or areas for improvement.
4.  Assign an overall sentiment score from 1 (very negative) to 5 (very positive).

Please format your output as a JSON object with the keys: "product_name", "positive_points" (list of strings), "negative_points" (list of strings), and "sentiment_score" (integer).
</instructions>

<customer_review>
I bought the new "AcousticBliss X100" headphones last week. The sound clarity is absolutely phenomenal, truly immersive! Also, the noise cancellation is top-notch. However, I found the headband a bit too tight for long listening sessions, and the carrying case feels rather flimsy for such premium headphones. Battery life is decent, though.
</customer_review>

<output_json>
</output_json>
```

## 2. Be Explicit About the Persona/Role

Claude responds very well to role prompting. Clearly defining the persona you want Claude to adopt can significantly influence its tone, style, and the type of information it provides.

*   **Placement:** You can define the role at the beginning of the prompt, often within `<role_definition>` or `<instructions>` tags.
*   **Specificity:** The more specific your role definition, the better. Instead of "You are an expert," try "You are an expert astrophysicist explaining black holes to a curious teenager."

## 3. Iterative Prompt Development with Claude

Don't expect the first prompt to be perfect. Engage in an iterative process:
*   **Start Simple:** Begin with a basic prompt and observe Claude's response.
*   **Analyze Output:** Identify what's good and what needs improvement.
*   **Refine:** Add more clarity, context, examples, or constraints. Adjust the role. Use more specific XML tags.
*   **Claude Can Help:** You can even ask Claude for suggestions on how to improve your prompt for a specific task. For example: "How can I rephrase my previous prompt to get a more concise summary?"

## 4. Handling Long Contexts

Claude models generally have large context windows.
*   **Place Important Instructions at the End:** Some evidence suggests that for very long contexts, instructions or questions placed towards the end of the prompt might be more heavily weighted or attended to by the model. This is sometimes referred to as "recency bias" in LLMs.
*   **Summarize if Necessary:** If dealing with extremely long conversational histories or documents that exceed the effective context window, consider periodically summarizing previous information and re-injecting it into the prompt.

## 5. Requesting Specific Output Formats

Clearly specify the desired output format. Claude is adept at generating structured data like JSON, Markdown, XML, etc., when instructed.

*   **Use Examples:** Show the desired format in few-shot examples.
*   **Explicit Instructions:** Clearly state "Format the output as a JSON object with the following keys..." or "Provide the answer as a Markdown table with columns..."
*   **Priming the Output:** You can start the expected output section with the beginning of the desired format (e.g., `{"product_name":`) as shown in the JSON example above.

## 6. Temperature and Other Generation Parameters

While not part of the prompt text itself, API parameters are crucial:
*   **Temperature:** Controls randomness. Lower values (e.g., 0.0-0.3) make the output more deterministic and focused, good for factual recall or specific formatting. Higher values (e.g., 0.7-1.0) encourage creativity and diversity.
*   **Max Tokens to Sample:** Ensure this is set appropriately to allow Claude to generate a complete response.

## 7. Pre-filling Claude's Responses (Assistant Prompting)

In a conversational setup (especially via API), you can pre-fill the beginning of Claude's (the "Assistant's") turn. This can strongly guide its subsequent generation.

**Example:**

```
Human: Analyze this financial report and give me the key takeaways in bullet points.
<financial_report_text>...
</financial_report_text>

Assistant: Okay, I have analyzed the report. Here are the key takeaways:
*   
```
By providing the start `*   `, you are priming Claude to continue with a bulleted list.

## 8. Understanding Claude's "Helpful, Harmless, and Honest" Design

Claude's underlying training with Constitutional AI aims to make it avoid generating harmful, unethical, or deeply biased content. Keep this in mind:
*   **Refusals:** If a prompt is ambiguous or could lead to problematic content, Claude might refuse to answer or ask for clarification. This is often a sign to rephrase or make your request more explicit and aligned with ethical AI principles.
*   **Steerability:** This design also means Claude can be more readily steered towards helpful and constructive outputs when prompted appropriately.

## 9. Testing and Evaluation

*   **Create a Test Suite:** For important or complex prompting tasks, create a small suite of test cases (various inputs) to evaluate how well your prompt performs consistently.
*   **Measure Quality:** Define what a "good" response looks like for your use case and evaluate Claude's outputs against these criteria.

By incorporating these best practices, you can significantly improve the quality, reliability, and steerability of responses from Claude models. 