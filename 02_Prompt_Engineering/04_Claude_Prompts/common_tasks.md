# Claude: Prompt Examples for Common Tasks (Using XML Tags)

This document provides practical prompt examples for common tasks, tailored for Anthropic's Claude models. A key recommendation for Claude is to use XML tags to structure prompts, clearly delineating instructions, context, input, and examples. This often leads to better and more predictable responses.

## 1. Text Summarization

Claude is proficient at summarizing texts. Using XML tags can help define the text to be summarized and the desired output format.

**Example 1.1: Basic Summarization**

```xml
<instructions>
Please summarize the following document concisely, highlighting the main points. Aim for a summary of about 3-4 sentences.
</instructions>

<document>
[Insert long document text here. For instance, a news article, a blog post, or a section from a research paper. The text can be multiple paragraphs long.]
</document>

<summary_output>
</summary_output>
```
*(Claude is expected to fill in the content for `<summary_output>`)*

**Example 1.2: Summarization with Specific Constraints**

```xml
<instructions>
Summarize the following customer feedback. Extract the following information:
1. The core issue the customer is facing.
2. The product or service mentioned.
3. The customer's expressed sentiment (e.g., Positive, Negative, Neutral, Mixed).

Present the summary in a structured format using the following XML tags:
<core_issue>...</core_issue>
<product_mentioned>...</product_mentioned>
<customer_sentiment>...</customer_sentiment>
</instructions>

<customer_feedback>
I recently purchased the new X1_PRO_HEADPHONES and I'm quite disappointed. While the sound quality is decent, the battery life is abysmal, lasting only about 2 hours on a full charge, not the advertised 8 hours. This is very frustrating for long commutes. I expected better for the price.
</customer_feedback>

<extracted_summary>
</extracted_summary>
```

## 2. Question Answering (QA)

Claude can answer questions based on provided context or its general knowledge. XML tags are excellent for separating the context and the question.

**Example 2.1: QA with Provided Context**

```xml
<instructions>
Based *only* on the provided document, answer the following question. If the answer is not found in the document, explicitly state "The answer is not found in the provided document."
</instructions>

<document>
The company's Q3 financial report highlighted a 15% increase in revenue, largely driven by the successful launch of its new software suite. However, operational costs also rose by 8% due to investments in R&D and expansion into new markets. The report expressed cautious optimism for Q4, contingent on stable market conditions.
</document>

<question>
What was the primary driver for the increase in revenue in Q3 according to the document?
</question>

<answer>
</answer>
```

**Example 2.2: Open-Domain QA (General Knowledge) with Persona**

```xml
<role_definition>
You are a helpful and knowledgeable historian specializing in ancient civilizations.
</role_definition>

<instructions>
Answer the user's question clearly and concisely, drawing upon your expertise as a historian.
</instructions>

<user_question>
What were some of the key factors contributing to the decline of the Roman Empire?
</user_question>

<response>
</response>
```

## 3. Creative Writing and Content Generation

Claude can assist with various creative writing tasks.

**Example 3.1: Generating a Short Story Idea**

```xml
<instructions>
Generate three distinct short story ideas based on the following theme. Each idea should include a brief plot summary, a main character concept, and a potential conflict.
</instructions>

<theme>
A world where dreams can be recorded and replayed.
</theme>

<story_ideas>
</story_ideas>
```

**Example 3.2: Writing an Email (Role Prompting)**

```xml
<role_definition>
You are a professional and courteous customer support representative for an online retail company.
</role_definition>

<instructions>
Draft an email responding to a customer who received a damaged item. The email should:
1. Apologize for the inconvenience.
2. Explain the options available to the customer (e.g., refund or replacement).
3. Provide clear instructions on how to proceed.
4. Maintain a polite and helpful tone.
</instructions>

<customer_query_summary>
Customer Name: Jane Doe
Order Number: 12345XYZ
Item: "Blue Ceramic Vase"
Issue: Received item broken.
</customer_query_summary>

<email_draft>
Subject: Regarding your recent order #12345XYZ

Dear Jane Doe,

</email_draft>
```

## 4. Few-Shot Prompting with XML

Providing examples within an XML structure can be very effective.

**Example 4.1: Classifying Customer Support Tickets**

```xml
<instructions>
Classify the following customer support tickets into one of these categories: "Billing Issue", "Technical Problem", "Feature Request", or "General Inquiry".
</instructions>

<example>
  <ticket_text>I think I was overcharged on my last invoice.</ticket_text>
  <category>Billing Issue</category>
</example>

<example>
  <ticket_text>The app crashes every time I try to upload a file.</ticket_text>
  <category>Technical Problem</category>
</example>

<example>
  <ticket_text>It would be great if you could add a dark mode to the interface.</ticket_text>
  <category>Feature Request</category>
</example>

<ticket_to_classify>
  <ticket_text>I'm just wondering what your opening hours are for next Monday.</ticket_text>
  <category></category>
</ticket_to_classify>
```

---

These examples demonstrate the utility of XML tags in structuring prompts for Claude across various tasks. This practice enhances clarity and often leads to more reliable and accurate outputs. Remember to adapt the tags and content to your specific needs. 