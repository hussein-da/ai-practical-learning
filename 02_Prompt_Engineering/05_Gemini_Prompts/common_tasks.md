# Gemini: Prompt Examples for Common Tasks

This document provides practical prompt examples for common tasks, tailored for Google's Gemini models. While Gemini excels in multimodal understanding, these initial examples will primarily focus on text-based inputs and outputs, but will be structured to easily accommodate multimodal elements where appropriate.

## 1. Text Analysis and Summarization

Gemini can perform sophisticated text analysis and summarization.

**Example 1.1: Comprehensive Article Summary**

```
User:
Please analyze the following news article. Provide a concise summary (approx. 100 words), identify the key entities mentioned (people, organizations, locations), and extract the main sentiment expressed (Positive, Negative, Neutral).

<article_text>
[Insert long news article text here. For example, an article discussing economic trends, technological advancements, or a political event.]
</article_text>

Desired output format:
Summary: [Your summary here]
Key Entities:
  People: [List]
  Organizations: [List]
  Locations: [List]
Main Sentiment: [Sentiment]
```

**Example 1.2: Comparative Analysis of Two Texts**

```
User:
Compare and contrast the following two product descriptions. Identify three key differences and three key similarities in their features and marketing angles. Present your findings in a table format.

<product_description_A>
**Product A: The EcoSphere Smart Thermostat**
Save energy and live smarter with EcoSphere! Our AI-powered thermostat learns your habits and optimizes your home's climate automatically. Features a sleek design, remote control via our intuitive app, and detailed energy usage reports. Made with recycled materials.
</product_description_A>

<product_description_B>
**Product B: The ThermoMax Pro Thermostat**
Experience ultimate comfort with ThermoMax Pro. Precision temperature control, programmable schedules, and a large, easy-to-read display. Built for reliability and compatible with all major HVAC systems. Professional installation recommended for optimal performance.
</product_description_B>

Output:
```

## 2. Cross-Modal Understanding (Conceptual Example with Text + Image Placeholder)

While direct API image input isn't shown here, prompts can be structured for future multimodal use.

**Example 2.1: Describing an Image and Answering Questions (Conceptual)**

```
User:
Consider the following image: [Placeholder for Image Data/Reference, e.g., <image_url> or <image_bytes>]

1.  Describe the scene depicted in the image in detail (3-4 sentences).
2.  What is the dominant color palette?
3.  Infer the possible time of day and season.
4.  If there are people in the image, what might they be doing or feeling?
```

## 3. Code Generation and Explanation

Gemini has strong coding capabilities.

**Example 3.1: Generating a Python Script with Specific Requirements**

```
User:
Write a Python script that performs the following actions:
1.  Takes a directory path as a command-line argument.
2.  Recursively finds all `.txt` files within that directory and its subdirectories.
3.  For each `.txt` file, counts the number of words.
4.  Prints the total word count for each file and a grand total word count for all files found.
Include error handling for invalid directory paths.
Please add comments to explain the main parts of your script.
```

**Example 3.2: Converting Code from One Language to Another**

```
User:
Translate the following JavaScript function into an equivalent Python function. Ensure the logic remains the same and explain any significant differences in syntax or approach between the two languages for this specific case.

<javascript_code>
function calculateFactorial(n) {
  if (n < 0) return -1; // Or throw an error
  if (n === 0) return 1;
  let result = 1;
  for (let i = 1; i <= n; i++) {
    result *= i;
  }
  return result;
}
</javascript_code>

<python_code_output>
</python_code_output>

<explanation_of_differences>
</explanation_of_differences>
```

## 4. Creative Content Generation

Gemini can be used for various creative writing tasks.

**Example 4.1: Brainstorming Marketing Slogans**

```
User:
I'm launching a new brand of eco-friendly coffee beans. The coffee is ethically sourced, sustainably farmed, and has a rich, smooth flavor. Generate 5 catchy marketing slogans that highlight these key aspects.
Slogans should be short (under 10 words each) and memorable.
```

**Example 4.2: Outlining a Blog Post**

```
User:
Create a detailed outline for a blog post titled "The Future of Remote Work: Trends and Technologies to Watch in 2025".
The outline should include:
*   A brief introduction.
*   At least 3 main section headings.
*   For each main section, 2-3 sub-points or topics to cover.
*   A brief conclusion.
```

---

These examples illustrate how to structure prompts for Gemini for common text-based and conceptually multimodal tasks. Clear instructions, context, and desired output formats are crucial. For actual multimodal prompting with image, audio, or video data, you would use the specific API mechanisms provided by Google for including that data alongside your text prompt. 