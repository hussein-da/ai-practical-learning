# Module 6: Practical NLP Applications

**A Learning Guide by Hussein Daoud** ([https://github.com/hussein-da](https://github.com/hussein-da))

This project is part of a comprehensive collection of learning modules designed to explore various AI concepts and implementations. Module 6 focuses on practical applications of **Natural Language Processing (NLP)**, specifically Named Entity Recognition (NER) and Text Classification.

We encourage you to explore, experiment, and adapt the code and examples for your own learning and projects. Feedback and contributions are welcome!

## 🚀 Introduction

Natural Language Processing (NLP) is a field of Artificial Intelligence focused on enabling computers to understand, interpret, and generate human language. It powers many applications we use daily, from search engines and translation services to chatbots and voice assistants.

This module explores two core NLP tasks:

1.  **Named Entity Recognition (NER):** Identifying and categorizing named entities in text into pre-defined categories such as person names, organizations, locations, medical codes, time expressions, quantities, monetary values, percentages, etc.
2.  **Text Classification:** Assigning predefined categories or labels to a piece of text based on its content (e.g., sentiment analysis, topic classification, spam detection).

We will implement examples using two powerful Python libraries:

*   **spaCy:** An open-source software library for advanced Natural Language Processing, known for its speed, efficiency, and production readiness, especially for tasks like NER, part-of-speech tagging, and dependency parsing.
*   **Hugging Face Transformers:** Provides thousands of pre-trained models (including state-of-the-art ones) for a wide range of NLP tasks, including NER and text classification, along with easy-to-use pipelines.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

*   Understand the concepts of Named Entity Recognition and Text Classification.
*   Use spaCy to perform NER on text data.
*   Use Hugging Face Transformers pipelines for both NER and Text Classification.
*   Load and utilize pre-trained models for these NLP tasks.
*   Process text data and interpret the outputs from NLP models.
*   Recognize the strengths and common use cases for spaCy and Hugging Face Transformers in practical NLP.

## 🛠️ Module Structure

```
06_Practical_NLP_Applications/
│
├── README.md                       # This file: Introduction to Practical NLP
├── requirements.txt                # Combined requirements for the module
│
├── 01_Named_Entity_Recognition/
│   ├── README.md                   # Introduction to NER
│   ├── example_ner_spacy.py        # NER example using spaCy
│   ├── example_ner_transformers.py # NER example using Hugging Face Transformers
│   └── data/
│       └── sample_ner_text.txt     # Sample text for NER examples
│
└── 02_Text_Classification/
    ├── README.md                   # Introduction to Text Classification
    ├── example_text_classification_transformers.py # Text Classification example (using Transformers)
    └── data/
        └── sample_classification_data.csv # Sample data for classification
```

## 📚 Prerequisites

*   Python 3.8 or higher.
*   Basic Python programming skills.
*   (Optional) Familiarity with concepts from previous modules.

## ⚙️ Setup and Installation

1.  **Set up your Python Environment:**
    *   Navigate to the `06_Practical_NLP_Applications/` directory.
    *   Create and activate a virtual environment:
        ```bash
        python -m venv nlp_env
        source nlp_env/bin/activate # On Windows: nlp_env\Scripts\activate
        ```
    *   Install the necessary libraries:
        ```bash
        pip install -r requirements.txt
        ```
    *   **Download spaCy Model:** The spaCy example requires a language model. We'll use a small English model:
        ```bash
        python -m spacy download en_core_web_sm
        ```

## 💡 Key Concepts

*   **Tokenization:** Breaking text down into individual words or sub-words (tokens).
*   **Part-of-Speech (POS) Tagging:** Assigning grammatical categories (noun, verb, adjective) to tokens.
*   **Named Entities:** Real-world objects (like people, places, organizations) or concepts (like dates, quantities) that can be denoted with a proper name.
*   **Entity Types/Labels:** The categories assigned to named entities (e.g., `PERSON`, `ORG`, `GPE` (Geopolitical Entity), `DATE`).
*   **Classification Labels:** The predefined categories used in text classification (e.g., `positive`, `negative`, `spam`, `sports`, `technology`).
*   **Pipelines (Hugging Face):** High-level interfaces that simplify using pre-trained models for specific tasks.
*   **Pre-trained Models:** Models trained on large datasets that can be fine-tuned or used directly for specific NLP tasks.

---

Let's explore how to extract information and categorize text using these powerful NLP techniques. 