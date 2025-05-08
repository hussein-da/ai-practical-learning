# Kafka & AI Sentiment Analysis Pipeline

This directory contains the components for a real-time sentiment analysis pipeline using Apache Kafka and the NLTK VADER sentiment analysis tool.

## Architecture

1.  **Producer (`producer.py`):** Simulates generating text messages (like tweets or user comments) and sends them to a Kafka topic (`raw_text_topic`).
2.  **Apache Kafka:** Acts as the message broker, receiving messages from the producer and holding them for consumers. It runs in Docker via `docker-compose.yml`.
3.  **Consumer (`sentiment_analyzer_consumer.py`):** 
    *   Connects to Kafka and subscribes to the `raw_text_topic` topic.
    *   Reads messages one by one.
    *   Uses NLTK's VADER (Valence Aware Dictionary and sEntiment Reasoner) to analyze the sentiment of the message text.
    *   Prints the original message and its predicted sentiment (POSITIVE, NEGATIVE, NEUTRAL) and compound score to the console.

## Setup Instructions

1.  **Start Kafka & Zookeeper:**
    *   Ensure Docker and Docker Compose are installed and running.
    *   Navigate to this directory (`10_Real_Time_Data_Pipelines/kafka_tf_sentiment/`) in your terminal.
    *   Run the Docker Compose setup:
        ```bash
        docker-compose up -d
        ```
        *   This command downloads the necessary images (if not already present) and starts Kafka and Zookeeper containers in detached mode (`-d`).
        *   Kafka will be accessible to the Python scripts at `localhost:9092`.

2.  **Set Up Python Environment:**
    *   Create and activate a Python virtual environment (recommended):
        ```bash
        # In the 10_Real_Time_Data_Pipelines/kafka_tf_sentiment/ directory
        python -m venv venv_kafka
        # Activate:
        # macOS/Linux: source venv_kafka/bin/activate
        # Windows: venv_kafka\\Scripts\\activate
        ```
    *   Install the required Python libraries:
        ```bash
        pip install -r requirements.txt
        ```
        *Note: This includes `kafka-python` and `nltk`. The first time you run the consumer, it may download the VADER lexicon if not already present on your system.*

3.  **(Optional) Verify Kafka Topic:**
    *   You might need to wait a minute for Kafka to fully initialize after `docker-compose up`.
    *   The producer script (`producer.py`) uses the topic `raw_text_topic`. The Kafka broker configuration (`KAFKA_AUTO_CREATE_TOPICS_ENABLE="true"` in `docker-compose.yml`) should ensure this topic is created automatically when the producer first sends a message to it.

## Running the Pipeline

You need to run the producer and consumer scripts simultaneously, typically in separate terminal windows.

**Terminal 1: Run the Consumer**

1.  Navigate to this directory (`10_Real_Time_Data_Pipelines/kafka_tf_sentiment/`).
2.  Activate your virtual environment (`source venv_kafka/bin/activate` or similar).
3.  Run the consumer script:
    ```bash
    python sentiment_analyzer_consumer.py
    ```
    *   The consumer will connect to Kafka. If running for the first time, NLTK might download the `vader_lexicon`. It will then start listening for messages on the `raw_text_topic` topic.

**Terminal 2: Run the Producer**

1.  Navigate to this directory (`10_Real_Time_Data_Pipelines/kafka_tf_sentiment/`).
2.  Activate your virtual environment (`source venv_kafka/bin/activate` or similar).
3.  Run the producer script:
    ```bash
    python producer.py
    ```
    *   The producer will start sending sample messages to the `raw_text_topic` topic every few seconds.

**Observing the Output:**

*   In **Terminal 1** (Consumer), you should see messages appearing shortly after the producer starts sending them. Each message will be printed along with its analyzed sentiment label (e.g., POSITIVE, NEGATIVE, NEUTRAL) and the compound sentiment score.
*   In **Terminal 2** (Producer), you will see logs indicating that messages are being sent successfully.

## Stopping the Pipeline

1.  Stop the producer script in Terminal 2 (Press `Ctrl+C`).
2.  Stop the consumer script in Terminal 1 (Press `Ctrl+C`).
3.  Stop and remove the Kafka and Zookeeper containers using Docker Compose:
    ```bash
    # From the 10_Real_Time_Data_Pipelines/kafka_tf_sentiment/ directory
    docker-compose down
    ```
    This command stops and removes the containers defined in the `docker-compose.yml` file.

## Customization

*   **Producer:** Modify `producer.py` to generate different types of messages or read from a real data source.
*   **Consumer:** The `sentiment_analyzer_consumer.py` uses NLTK/VADER. You could adapt it to use a different sentiment analysis library or a more complex model. You could also implement different logic based on the sentiment result (e.g., store in a database, trigger alerts, send to another Kafka topic).
*   **Kafka Configuration:** Adjust settings in `docker-compose.yml` or client connection parameters for more advanced Kafka setups. 