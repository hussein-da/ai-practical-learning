# GPT-4: Prompt Examples for Advanced Techniques

This document explores more advanced prompting techniques tailored for GPT-4, focusing on its enhanced reasoning, creativity, and instruction-following capabilities. These examples often involve more complex scenarios, multi-turn interactions (simulated here with detailed system/user prompts), and sophisticated output requirements.

## 1. Advanced Role-Playing / Persona-Driven Interaction

GPT-4 can adopt complex personas and maintain them consistently, allowing for nuanced interactions.

**Example 1.1: Socratic Tutor for a Complex Topic**

```
System:
You are Socrates, a wise and patient tutor. Your goal is to help the user understand the concept of "General Relativity" through a series of guided questions, rather than direct explanations. Encourage the user to think critically and arrive at conclusions themselves. Respond to their answers by asking further probing questions or gently correcting misconceptions by leading them to a new line of thought.

User:
I'm trying to understand General Relativity. Can you explain it to me?

(GPT-4 as Socrates should now start asking questions, e.g., "Tell me, what is your current understanding of gravity, perhaps as Newton described it?")
```

**Example 1.2: Simulating a Technical Interview**

```
System:
You are an expert hiring manager conducting a technical interview for a Senior Python Developer position. Ask the user challenging questions related to Python internals, system design, and data structures. Evaluate their answers for correctness, clarity, and depth of understanding. Provide constructive feedback after each answer or a set of answers. Start by introducing yourself and the first question.

User:
I'm ready for my technical interview.

(GPT-4 should then initiate the interview, e.g., "Hello, I'm the lead engineer at TechSolutions Inc. Thanks for your time today. Let's start with this: Can you explain Python's Global Interpreter Lock (GIL) and its implications for concurrent programming?")
```

## 2. Multi-Step Reasoning and Complex Problem Solving

Leverage GPT-4's improved reasoning by breaking down complex problems or asking for step-by-step analysis.

**Example 2.1: Strategic Business Advice**

```
System:
You are a seasoned business strategist. The user will present a business challenge, and you need to provide a comprehensive analysis and a set of actionable recommendations.

User:
My e-commerce startup, specializing in handmade artisanal soaps, has seen a 20% decline in sales over the past quarter. Our marketing efforts on social media seem to be less effective, and customer acquisition cost is rising. We have a loyal but small customer base. Provide a step-by-step analysis of potential causes and suggest three distinct strategic initiatives to reverse this trend, including how to measure their success.

(GPT-4 should then provide a structured analysis: e.g., 1. Potential Causes (Market saturation? Competitor actions? Reduced ad effectiveness? Product fatigue?), 2. Strategic Initiative 1 (e.g., Loyalty Program Enhancement), 3. Strategic Initiative 2 (e.g., Explore New Marketing Channels/Partnerships), 4. Strategic Initiative 3 (e.g., Product Line Diversification/Refresh), with details on implementation and KPIs for each.)
```

**Example 2.2: Debugging and Explaining Complex Code Logic**

```
System:
You are an expert software engineer with deep knowledge of asynchronous programming in Python. Analyze the provided code, explain its intended logic, identify any potential bugs or race conditions, and suggest improvements for clarity and robustness.

User:
Can you help me understand this Python asyncio code? It's supposed to fetch data from multiple URLs concurrently and process them, but sometimes it behaves unexpectedly or throws errors.

Code:
"""
import asyncio
import aiohttp

async def fetch(session, url):
    # Intentionally simplified, potential issues might be more subtle in real code
    async with session.get(url) as response:
        # What if response is not 200?
        return await response.text()

async def main():
    urls = [
        "http://example.com/api/data1",
        "http://example.com/api/data2", # potentially slow or error-prone
        "http://example.com/api/data3",
    ]
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        results = await asyncio.gather(*tasks) # What if one task fails?
        for result in results:
            print(f"Processed data: {result[:50]}...") # Basic processing

asyncio.run(main())
"""

(GPT-4 should then break down the code, explain `asyncio`, `aiohttp`, `async/await`, `ClientSession`, `asyncio.gather`. It should point out lack of error handling for HTTP responses, implications of `asyncio.gather` failing if one task fails, and suggest using `return_exceptions=True` or more robust error handling per task, and perhaps more sophisticated processing.)
```

## 3. Generating Nuanced and Creative Content

Push GPT-4's creative boundaries with detailed prompts.

**Example 3.1: Writing in a Specific Author's Style**

```
System:
You are an AI assistant with a deep understanding of literary styles. Emulate the writing style of Ernest Hemingway to describe a simple, everyday scene.

User:
Describe a man drinking coffee alone at a diner on a rainy morning, in the style of Ernest Hemingway. Focus on concise sentences, objective descriptions, and an underlying sense of stoicism. The description should be about 150 words.
```

**Example 3.2: Developing a Complex Fictional Character**

```
System:
You are a creative writing assistant, expert in character development.

User:
Help me develop a main character for a science fiction novel. The character is a disillusioned ex-starship pilot named Kaelen, who now works as a smuggler on the fringes of a galactic empire. I need a detailed backstory (approx. 300 words) covering:
1.  Their early life and what led them to become a pilot.
2.  A pivotal event that caused their disillusionment with the empire and their discharge.
3.  How they transitioned into smuggling.
4.  Their core motivations and internal conflicts now.

Make Kaelen morally ambiguous but with a hidden code of honor.
```

**Example 3.3: Generating a Script with Specific Constraints**

```
System:
You are an AI screenwriter.

User:
Write a 2-page dialogue scene for a screenplay. The scene features two characters, ANNA (30s, a pragmatic detective) and LEO (50s, an eccentric informant), meeting in a dimly lit, cluttered antique shop. Anna needs information from Leo about a recent art heist. Leo is reluctant and speaks in riddles. The scene should build suspense and end with Leo giving Anna a cryptic clue. Adhere to standard screenplay formatting.
```

---

These advanced examples showcase GPT-4's versatility. The key is to provide rich context, clear objectives, and detailed constraints. Don't hesitate to iterate and refine your prompts based on the outputs, or even engage GPT-4 in a meta-conversation about how to improve the prompts for the desired task. 