# 01: Named Entity Recognition (NER)

Named Entity Recognition (NER) is a fundamental task in Natural Language Processing (NLP) that involves identifying and classifying named entities within unstructured text into predefined categories.

**What are Named Entities?**

These are typically real-world objects or concepts that can be referred to with a proper name. Common categories include:

*   **PERSON:** People's names (e.g., "Elon Musk", "Marie Curie").
*   **ORG:** Organizations, companies, institutions (e.g., "Google", "United Nations", "Stanford University").
*   **GPE (Geopolitical Entity):** Countries, cities, states (e.g., "Germany", "Paris", "California").
*   **LOC:** Non-GPE locations, mountain ranges, bodies of water (e.g., "Mount Everest", "the Nile", "Silicon Valley").
*   **DATE:** Absolute or relative dates (e.g., "June 2024", "yesterday", "the 21st century").
*   **TIME:** Times (e.g., "4 PM", "midnight").
*   **MONEY:** Monetary values (e.g., "$50 million", "€19.99").
*   **PERCENT:** Percentage values (e.g., "20%", "fifty percent").
*   **PRODUCT:** Objects, vehicles, foods, etc. (e.g., "iPhone", "Tesla Model S").
*   **EVENT:** Named hurricanes, battles, wars, sports events, etc. (e.g., "World War II", "the Olympics").
*   **NORP (Nationalities or Religious or Political groups):** (e.g., "German", "Christian", "Democrats").
*   **FAC (Facility):** Buildings, airports, highways, bridges, etc. (e.g., "Eiffel Tower", "JFK Airport").
*   **LAW:** Named documents made into laws.
*   **LANGUAGE:** Any named language.

*(Note: The exact set of entity types can vary depending on the model or system used.)*

**Why is NER Useful?**

NER is a crucial first step in many NLP pipelines for:

*   **Information Extraction:** Automatically pulling structured information (like names, locations, dates) from unstructured text (news articles, reports, emails).
*   **Content Categorization:** Helping to understand the main topics or subjects discussed in a document.
*   **Question Answering:** Identifying key entities in a question and searching for answers related to those entities in documents.
*   **Search Engine Improvement:** Enhancing search relevance by understanding the entities mentioned in queries and documents.
*   **Customer Support:** Automatically extracting product names, order numbers, or customer names from support tickets.
*   **Recommendation Systems:** Identifying entities mentioned in user reviews or content to make better recommendations.

## Examples in this Section

We will explore NER using two popular libraries:

1.  **`example_ner_spacy.py`:** Demonstrates how to use spaCy's pre-trained statistical models for efficient and general-purpose NER.
2.  **`example_ner_transformers.py`:** Shows how to use the Hugging Face Transformers library, leveraging potentially larger and more specialized pre-trained models available on the Hugging Face Hub.

Both examples will use the sample text provided in `data/sample_ner_text.txt`. 