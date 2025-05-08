# 02: Text Classification

Text Classification is another fundamental task in Natural Language Processing (NLP). It involves assigning one or more predefined categories or labels to a given piece of text (e.g., a sentence, paragraph, document).

**Common Text Classification Tasks:**

*   **Sentiment Analysis:** Classifying text based on the expressed sentiment (e.g., positive, negative, neutral). This is perhaps the most common text classification task.
*   **Topic Classification:** Assigning topics to text (e.g., labeling news articles as "sports", "technology", "politics", "business").
*   **Spam Detection:** Classifying emails or messages as "spam" or "not spam" (ham).
*   **Language Detection:** Identifying the language of a given text.
*   **Intent Recognition:** Determining the user's intent behind a query or statement (e.g., in chatbots - "book flight", "check weather", "general query").
*   **Urgency Detection:** Classifying customer support tickets or messages based on urgency (e.g., "high", "medium", "low").

**Why is Text Classification Useful?**

*   **Organizing Information:** Automatically sorting large volumes of text data (e.g., emails, support tickets, social media mentions).
*   **Understanding Customer Feedback:** Analyzing reviews or survey responses to gauge overall sentiment or identify common themes.
*   **Content Moderation:** Detecting harmful or inappropriate content.
*   **Routing Information:** Directing emails or support requests to the appropriate department based on topic or intent.
*   **Market Research:** Analyzing online discussions to understand public opinion about products or brands.

## Approach in this Section

While various libraries can perform text classification, the Hugging Face Transformers library provides easy access to a vast number of powerful, pre-trained models specifically fine-tuned for different classification tasks (like sentiment analysis, topic classification, etc.).

SpaCy also offers text classification capabilities (`textcat` component), but it often works best when trained or fine-tuned on your specific dataset and categories. Using a general-purpose pre-trained pipeline from Hugging Face is often simpler for demonstrating the concept with immediate results.

Therefore, this section will focus on using a Hugging Face pipeline:

*   **`example_text_classification_transformers.py`:** Demonstrates how to use a pre-trained text classification model (e.g., for sentiment analysis or topic classification) from the Hugging Face Hub.

The example will use sample data provided in `data/sample_classification_data.csv`. 