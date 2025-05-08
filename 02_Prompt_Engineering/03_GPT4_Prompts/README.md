# Prompting GPT-4

This section focuses on providing examples and explanations for optimizing prompts specifically for OpenAI's GPT-4 model.

## Introduction to GPT-4

GPT-4 (Generative Pre-trained Transformer 4) is a large multimodal model created by OpenAI. It exhibits human-level performance on various professional and academic benchmarks. Compared to its predecessors like GPT-3.5, GPT-4 is more reliable, creative, and able to handle much more nuanced instructions.

**Key Strengths of GPT-4 Relevant to Prompting:**

*   **Advanced Reasoning:** GPT-4 shows improved capabilities in complex reasoning, including mathematical, logical, and commonsense reasoning.
*   **Instruction Following:** It is significantly better at following complex and nuanced instructions.
*   **Creativity and Collaboration:** GPT-4 can generate, edit, and iterate on creative and technical writing tasks with users, such as composing songs, writing screenplays, or learning a user's writing style.
*   **Longer Context Window:** GPT-4 can process and generate much longer texts, allowing for more extensive context in prompts.
*   **Multimodality (via API access for vision):** GPT-4 can accept image inputs and generate text outputs, opening up new prompting possibilities (though our examples here will focus on text-based prompting unless specified).

## General Tips for Prompting GPT-4

While the general prompt engineering principles and techniques discussed earlier apply, here are some considerations more specific to GPT-4:

1.  **Be Explicit and Detailed:** GPT-4 can handle very detailed instructions. Don't shy away from being verbose if it adds clarity to your request. The more specific you are, the better it can tailor the response to your exact needs.
2.  **Leverage its Reasoning:** For complex problems, explicitly ask GPT-4 to reason through the problem, or use Chain-of-Thought prompting. It's capable of sophisticated step-by-step analysis.
3.  **System Messages:** When using the Chat Completions API, the "system" message can be used effectively to set the persona, context, and high-level instructions for GPT-4. This can be more effective than putting all instructions in the user message, especially for conversational interactions.
    *Example System Message: "You are an expert AI assistant specializing in explaining complex scientific concepts to a lay audience. Your tone should be informative yet engaging and easy to understand. Avoid jargon where possible, or explain it clearly if necessary."*
4.  **Iterative Refinement:** Even with GPT-4, your first prompt might not be perfect. Use its responses as feedback to refine your prompt. You can even ask GPT-4 to help you improve your prompts for a specific task.
5.  **Specify Constraints:** Clearly define any constraints on the output, such as length (word count, number of paragraphs), style, tone, or information to include/exclude.
6.  **Experiment with Temperature:** For more creative or diverse outputs, a slightly higher temperature (e.g., 0.7-0.9) might be beneficial. For factual, precise answers, a lower temperature (e.g., 0.1-0.3) is usually better.
7.  **Ask for Specific Formats:** GPT-4 is very good at generating text in specific formats like JSON, XML, Markdown tables, etc. Clearly request the format you need.

## Structure of this Section

*   **`common_tasks.md`**: This file will provide prompt examples for common tasks such as text summarization, question answering, translation, and code generation, tailored for GPT-4.
*   **`advanced_techniques.md`**: This file will explore more advanced prompting techniques, including complex role-playing scenarios, multi-step reasoning, and generating nuanced creative content with GPT-4.

By exploring these examples, you'll gain a better understanding of how to effectively interact with GPT-4 to achieve your desired outcomes. 