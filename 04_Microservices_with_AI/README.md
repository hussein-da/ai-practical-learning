# Module 4: Microservices with AI - Building an AI-Powered API

**A Learning Guide by Hussein Daoud** ([https://github.com/hussein-da](https://github.com/hussein-da))

This module explores how to integrate AI models into a microservice architecture. We will build a simple web API that exposes an AI capability – specifically, sentiment analysis.

## 🚀 Introduction: AI in Microservices

Microservices architecture involves breaking down a large application into smaller, independent services that communicate over a network (typically HTTP APIs). Integrating AI into this architecture means encapsulating AI models and their logic within dedicated microservices.

**Benefits:**

*   **Scalability:** AI inference can be resource-intensive. An AI microservice can be scaled independently based on demand, without affecting other parts of the application.
*   **Independent Deployment:** Updates to the AI model or its surrounding logic can be deployed without redeploying the entire application.
*   **Technology Diversity:** The AI microservice can use the best tools and libraries for the job (Python, specific ML frameworks) without imposing those choices on other services.
*   **Clear Responsibility:** Encapsulates the AI functionality within a well-defined service boundary.

**Challenges:**

*   **Latency:** Network calls between services add latency compared to monolithic designs.
*   **Model Management:** Versioning, deploying, and monitoring the AI model within the service requires careful planning.
*   **Infrastructure Complexity:** Managing multiple services, potentially with different resource needs (CPU, GPU), adds complexity.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

*   Understand the rationale for wrapping AI models in microservices.
*   Build a simple web API using Flask to serve an AI model.
*   Utilize the Hugging Face Transformers library `pipeline` for easy model inference (sentiment analysis).
*   Containerize the AI microservice using Docker.
*   Interact with the API endpoint to get AI predictions.

## 🛠️ Module Structure: Sentiment Analysis API

We will build a basic API (`sentiment_api`) that accepts text input and returns its sentiment (positive/negative) using a pre-trained model.

```
04_Microservices_with_AI/
│
├── README.md               # This file: Introduction to AI Microservices & the example
│
└── sentiment_api/
    ├── app.py              # Flask application code
    ├── requirements.txt    # Python dependencies for the API
    ├── Dockerfile          # Dockerfile for containerizing the API
    └── .env.example        # Example environment variables (optional)
```

## 📚 Prerequisites

*   Python 3.8 or higher.
*   Basic understanding of web APIs (HTTP methods like POST, JSON format).
*   Familiarity with Flask (or willingness to learn the basics from the example).
*   Docker installed.
*   Understanding of virtual environments and `pip`.

## ⚙️ Setup & Usage

The following steps guide you through setting up and running the `sentiment_api` microservice.

### 1. Navigate to the Service Directory

Open your terminal and change into the `sentiment_api` directory:
```bash
cd 04_Microservices_with_AI/sentiment_api
```

### 2. Set Up Python Environment & Install Dependencies

It's recommended to use a virtual environment.

```bash
# Create a virtual environment (if you haven't already for this module)
python -m venv venv_ms

# Activate it
# On macOS/Linux:
# source venv_ms/bin/activate
# On Windows:
# venv_ms\Scripts\activate

# Install required packages
pip install -r requirements.txt
```
*Note: Installing PyTorch (`torch`) and `transformers` might take some time and download a significant amount of data.*

### 3. Running the API Directly (for Development/Testing)

You can run the Flask application directly using the Waitress server:

```bash
python app.py
```
This will typically start the server on `http://localhost:5000`. You'll see output indicating the server is running and loading the sentiment analysis model. You can then send requests to it (see Step 6).
Press `Ctrl+C` to stop the server.

### 4. Building the Docker Image

Make sure Docker is running on your system. From the `04_Microservices_with_AI/sentiment_api/` directory, build the Docker image:

```bash
docker build -t sentiment-analysis-api .
```
This command reads the `Dockerfile`, installs dependencies, and packages the application into an image named `sentiment-analysis-api`.

### 5. Running the Docker Container

Once the image is built, run it as a container:

```bash
docker run -p 5001:5000 --rm sentiment-analysis-api
```
*   `-p 5001:5000`: This maps port 5001 on your host machine to port 5000 inside the container (where Waitress is listening). You can access the API at `http://localhost:5001`.
*   `--rm`: Automatically removes the container when it stops.
*   `sentiment-analysis-api`: The name of the image you built.

You should see output indicating the server is running inside the container.

### 6. Interacting with the API

The API has two endpoints:

*   **`GET /`**: A simple health check endpoint.
    Open your browser to `http://localhost:5001` (if running Docker with the mapping above) or `http://localhost:5000` (if running directly). You should see: `{"message":"Sentiment Analysis API is running. Use POST /analyze_sentiment to analyze text."}`

*   **`POST /analyze_sentiment`**: Accepts JSON data with a "text" field and returns the sentiment.

    You can use `curl` (or tools like Postman, Insomnia) to send a POST request. Example using `curl` from your terminal:

    ```bash
    curl -X POST http://localhost:5001/analyze_sentiment \
         -H "Content-Type: application/json" \
         -d '{"text": "This course is incredibly helpful and well-structured!"}'
    ```

    **Expected Response:**
    ```json
    {
      "score": 0.9998815059661865,
      "sentiment": "POSITIVE",
      "text": "This course is incredibly helpful and well-structured!"
    }
    ```

    **Example with negative text:**
    ```bash
    curl -X POST http://localhost:5001/analyze_sentiment \
         -H "Content-Type: application/json" \
         -d '{"text": "The weather today is quite gloomy and disappointing."}'
    ```

    **Expected Response:**
    ```json
    {
      "score": 0.9997767806053162,
      "sentiment": "NEGATIVE",
      "text": "The weather today is quite gloomy and disappointing."
    }
    ```

### 7. Stopping the Container

If you ran the container interactively, press `Ctrl+C` in the terminal where it's running. If it was running in detached mode (using `-d`), you can use `docker stop <container_id>`.

---

This completes the setup and usage guide for the AI-powered sentiment analysis microservice! 