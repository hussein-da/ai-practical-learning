# 02: Prompting Techniques

Beyond the general best practices, several specific techniques can significantly enhance your ability to guide Large Language Models (LLMs). This section explores some of the most effective and commonly used prompting techniques.

## 1. Zero-Shot Prompting

**Concept:** You ask the LLM to perform a task without providing any prior examples of how to do it. The model relies solely on its pre-trained knowledge to understand and execute the request.

**When to Use:**
*   For simple, straightforward tasks.
*   When the LLM has a strong inherent understanding of the task (e.g., basic summarization, simple Q&A, common sense reasoning).
*   As a baseline to see how well the model performs before trying more complex techniques.

**Example:**

```
Prompt:
Translate the following English text to French:
"Hello, how are your today?"

Expected Output (from a capable model):
"Bonjour, comment allez-vous aujourd'hui?"
```

**Pros:** Simple, quick to implement.
**Cons:** May not work well for complex or nuanced tasks, or if the desired output format is very specific.

## 2. Few-Shot Prompting

**Concept:** You provide the LLM with a few examples (typically 1 to 5) of the task you want it to perform, demonstrating the desired input-output pattern. The model learns from these examples and applies that pattern to new input.

**When to Use:**
*   When the task is more complex, and the LLM needs guidance on the expected format or style.
*   To steer the model towards a specific type of response or reasoning process.
*   When zero-shot prompting yields unsatisfactory results.

**Example (Sentiment Analysis):**

```
Prompt:
Classify the sentiment of the following movie reviews as Positive, Negative, or Neutral.

Review: "This movie was absolutely fantastic! The acting was superb, and the plot was gripping."
Sentiment: Positive

Review: "I was really disappointed. The story was boring and predictable."
Sentiment: Negative

Review: "It was an okay movie. Nothing special, but not terrible either."
Sentiment: Neutral

Review: "The special effects were incredible, but the characters felt underdeveloped."
Sentiment: 
```

**Expected Output (from the LLM):**
```
Neutral
```
*(Or potentially "Positive" if it weighs special effects heavily, or "Mixed" if it's capable of such nuance and the prompt allowed for it. This highlights the importance of clear example categories.)*

**Pros:** Significantly improves performance on many tasks, helps in specifying output format and style.
**Cons:** Requires crafting good examples, can increase prompt length (and token count).

## 3. Chain-of-Thought (CoT) Prompting

**Concept:** You encourage the LLM to generate a series of intermediate reasoning steps before arriving at the final answer. This is often achieved by including examples in few-shot prompts where the reasoning process is explicitly shown, or by simply adding phrases like "Let's think step by step."

**When to Use:**
*   For tasks requiring arithmetic, commonsense, or symbolic reasoning.
*   When the problem is complex and benefits from being broken down.

**Example (Simple Math Problem with Few-Shot CoT):**

```
Prompt:
Q: Roger has 5 tennis balls. He buys 2 more cans of tennis balls. Each can has 3 tennis balls. How many tennis balls does he have now?
A: Roger starts with 5 balls. He buys 2 cans, and each can has 3 balls. So, he gets 2 * 3 = 6 new balls. Therefore, he now has 5 + 6 = 11 tennis balls. The answer is 11.

Q: The cafeteria had 23 apples. If they used 20 to make lunch and bought 6 more, how many apples do they have?
A: The cafeteria starts with 23 apples. They used 20, so they have 23 - 20 = 3 apples left. Then they bought 6 more apples, so they now have 3 + 6 = 9 apples. The answer is 9.

Q: Natalia sold clips to Veda for $4 each. Veda bought 3 clips. Then Natalia spent $2 on a candy bar. How much money does Natalia have now?
A:
```

**Expected Output (from the LLM, showing reasoning):**
```
Natalia sold 3 clips to Veda for $4 each. So, Natalia made 3 * $4 = $12. Then Natalia spent $2 on a candy bar. So, Natalia now has $12 - $2 = $10. The answer is 10.
```

**Zero-Shot CoT Example:**

```
Prompt:
Q: A juggler can juggle 16 balls. Half of the balls are golf balls, and half of the golf balls are blue. How many blue golf balls are there?

A: Let's think step by step.
```

**Pros:** Significantly improves reasoning abilities of LLMs, makes the model's thinking process more interpretable.
**Cons:** Increases output length, may require careful example crafting for few-shot CoT.

## 4. Persona / Role Prompting

**Concept:** You instruct the LLM to adopt a specific role or persona. This helps to shape the tone, style, expertise level, and content of the response.

**When to Use:**
*   To generate text in a specific voice (e.g., expert, comedian, pirate).
*   To tailor responses for a particular audience.
*   To simulate conversations or scenarios.

**Example:**

```
Prompt:
Act as an experienced Python developer. Explain the concept of list comprehensions in Python to a beginner. Provide a simple example.
```

**Pros:** Powerful for controlling output style and content focus, enhances creativity and engagement.
**Cons:** The LLM's interpretation of the persona can sometimes be stereotypical or superficial if not guided well.

## 5. Instruction Prompting

**Concept:** This is a more direct form of prompting where you clearly state the task the LLM needs to perform. It often involves using action verbs and precise language. Many modern LLMs are fine-tuned on instructions, making them particularly responsive to this technique.

**When to Use:**
*   For most tasks where a clear directive can be given.
*   Often used in conjunction with other techniques (e.g., providing context and then an instruction).

**Example:**

```
Prompt:
###Instruction###
Summarize the following article into three key bullet points. Focus on the main outcomes and their implications.

###Article###
[Insert long article text here]

###Summary###
```

**Pros:** Clear, direct, and often effective, especially with instruction-tuned models.
**Cons:** Requires careful formulation of the instruction to avoid ambiguity.

## 6. Output Priming

**Concept:** You start the LLM's response with a word or phrase to guide it towards the desired output structure or content type.

**When to Use:**
*   To nudge the model towards a specific format (e.g., starting with `{"key":` for JSON output).
*   To initiate a particular style or thought process.

**Example:**

```
Prompt:
Extract the key findings from the research paper summary below. Present them as a numbered list.

Summary: [Insert research paper summary here]

Key Findings:
1. 
```

**Pros:** Simple way to influence output structure.
**Cons:** May not be sufficient for complex formatting; the model might ignore the prime if the rest of the prompt is contradictory or unclear.

## 7. Delimiter Usage

**Concept:** Using specific characters or strings (delimiters) to separate different parts of your prompt, such as instructions, context, examples, or input data. Common delimiters include `###`, `---`, `"""`, or XML-like tags (`<context>`, `</context>`).

**When to Use:**
*   When your prompt contains multiple distinct sections.
*   To help the LLM clearly distinguish between instructions and the text it needs to process.
*   To improve readability and organization of complex prompts.

**Example:**

```
Prompt:
###Instruction###
Translate the following user query from English to Spanish.

###User Query###
"I would like to book a flight to Madrid for next Tuesday."

###Spanish Translation###
```

**Pros:** Improves clarity and reduces ambiguity, especially for complex prompts.
**Cons:** Adds slightly to prompt length.

---

These techniques are not mutually exclusive and can often be combined for more sophisticated prompting strategies. Experimentation is key to finding what works best for your specific LLM and task. 