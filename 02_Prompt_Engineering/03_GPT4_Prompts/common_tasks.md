# GPT-4: Prompt Examples for Common Tasks

This document provides practical prompt examples for common tasks, specifically tailored for leveraging the capabilities of GPT-4. Remember to use the Chat Completions API structure with system and user messages for optimal results where applicable.

## 1. Text Summarization

GPT-4 excels at summarizing text with varying levels of detail and for different purposes.

**Example 1.1: Basic Summarization**

```
System:
You are a helpful AI assistant that summarizes texts accurately and concisely.

User:
Please summarize the following article in approximately 100 words. Focus on the main arguments and conclusions.

Article:
"""
[Insert long article text here. For example, a news report about a recent scientific discovery, detailing the methodology, findings, and implications. The article could be several paragraphs long.]
"""
```

**Example 1.2: Summarization with Specific Focus**

```
System:
You are an AI assistant specializing in extracting key financial information from texts.

User:
Summarize the provided company earnings report, focusing specifically on revenue growth, profit margins, and future outlook. Present the summary as a short paragraph followed by three bullet points for each key area (Revenue Growth, Profit Margins, Future Outlook).

Report:
"""
[Insert company earnings report text here. This text would include financial figures, management discussion, and forward-looking statements.]
"""
```

**Example 1.3: Summarization for a Specific Audience**

```
System:
You are an AI assistant that can explain complex topics simply.

User:
Summarize the following scientific paper on quantum entanglement for a high school student who has a basic understanding of physics but no prior knowledge of quantum mechanics. The summary should be no more than 150 words and highlight the core concept and its potential significance.

Paper Abstract:
"""
[Insert a dense, jargon-filled scientific paper abstract here.]
"""
```

## 2. Question Answering (QA)

GPT-4 can answer questions based on provided context or its general knowledge.

**Example 2.1: QA with Provided Context**

```
System:
You are an AI assistant that answers questions based *only* on the provided text. If the answer is not found in the text, state that clearly.

User:
Based on the text below, what were the main challenges faced by the project?

Text:
"""
The project, initiated in early 2022, aimed to develop a new sustainable energy source. Initial progress was swift, leveraging existing research. However, by mid-year, unexpected material shortages and a sudden withdrawal of a key funding partner led to significant delays. Furthermore, the engineering team encountered unforeseen technical hurdles related to scaling the prototype.
"""
```

**Example 2.2: Open-Domain QA (General Knowledge)**

```
System:
You are a knowledgeable AI assistant.

User:
Explain the main differences between nuclear fission and nuclear fusion in simple terms.
```

## 3. Translation

GPT-4 offers high-quality translation capabilities.

**Example 3.1: Simple Translation**

```
System:
You are an expert AI translator.

User:
Translate the following English sentence into German:
"The quick brown fox jumps over the lazy dog."
```

**Example 3.2: Translation with Contextual Nuance**

```
System:
You are an AI translator specializing in marketing copy. Your translations should be natural-sounding and persuasive for the target audience.

User:
Translate the following English marketing slogan into French. The target audience is young adults interested in sustainable fashion.

Slogan: "Wear the change you want to see."
```

## 4. Code Generation

GPT-4 can generate code snippets in various programming languages.

**Example 4.1: Generating a Python Function**

```
System:
You are an AI programming assistant proficient in Python.

User:
Write a Python function that takes a list of integers as input and returns a new list containing only the even numbers from the input list. Please include a docstring explaining what the function does.
```

**Example 4.2: Explaining Code and Suggesting Improvements**

```
System:
You are an AI code reviewer and programming expert.

User:
Explain what the following Python code does. Then, suggest any potential improvements or identify any bugs.

Code:
"""
_def_ _calculate_sum_(lst):
  total = 0
  _for_ i _in_ _range_(_len_(lst)):
    total += lst[i]
  _return_ total
"""
```

**Example 4.3: Generating Code with Specific Libraries/Frameworks**

```
System:
You are an AI programming assistant specializing in web development with Flask.

User:
Write a simple Python Flask route that handles a GET request to `/api/greet` and returns a JSON response like `{"message": "Hello, World!"}`.
```

---

These examples illustrate how to structure prompts for GPT-4 for common use cases. Remember to adapt the system message and user instructions based on the specifics of your task and desired output. Iteration and providing clear, detailed instructions are key to maximizing GPT-4's performance. 