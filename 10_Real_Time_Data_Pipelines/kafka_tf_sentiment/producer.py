import time
import json
from kafka import KafkaProducer
import random

# Configuration
KAFKA_BROKER = 'localhost:9092'
TOPIC_NAME = 'raw_text_topic'
MESSAGES_PER_SECOND = 2
PRODUCER_ID = random.randint(1, 1000) # To differentiate if multiple producers are run

# Sample sentences for demonstration
SAMPLE_SENTENCES = [
    "I love this product, it's amazing!",
    "This is the worst experience I have ever had.",
    "The weather today is quite pleasant.",
    "I'm not sure how I feel about this update.",
    "Customer service was very helpful and friendly.",
    "The documentation is confusing and lacks detail.",
    "What a fantastic movie, I highly recommend it.",
    "I am feeling neutral about the current situation.",
    "This new feature is a game changer!",
    "The application keeps crashing on my device."
]

def create_producer():
    """Creates and returns a KafkaProducer instance."""
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            acks='all',  # Strongest delivery guarantee
            retries=5,   # Retry up to 5 times
            linger_ms=100 # Batch messages for 100ms
        )
        print(f"Producer (ID: {PRODUCER_ID}) connected to Kafka broker at {KAFKA_BROKER}")
        return producer
    except Exception as e:
        print(f"Error connecting to Kafka: {e}")
        return None

def send_message(producer, topic, message_data):
    """Sends a single message to the specified Kafka topic."""
    try:
        future = producer.send(topic, message_data)
        # Block for 'synchronous' sends, wait for ack from broker
        record_metadata = future.get(timeout=10)
        # print(f"Message sent to {record_metadata.topic} partition {record_metadata.partition} offset {record_metadata.offset}")
        return True
    except Exception as e:
        print(f"Error sending message: {e}")
        return False

if __name__ == "__main__":
    producer = create_producer()

    if producer:
        print(f"Starting to send messages to topic '{TOPIC_NAME}' every {1/MESSAGES_PER_SECOND:.2f} seconds. Press Ctrl+C to stop.")
        message_count = 0
        try:
            while True:
                sentence = random.choice(SAMPLE_SENTENCES)
                message_id = f"msg_{PRODUCER_ID}_{int(time.time())}_{message_count}"
                
                message = {
                    'id': message_id,
                    'text': sentence,
                    'source': f'producer_{PRODUCER_ID}',
                    'timestamp': time.time()
                }
                
                if send_message(producer, TOPIC_NAME, message):
                    print(f"Sent: {message['id']} - '{message['text'][:50]}...'")
                    message_count += 1
                
                time.sleep(1 / MESSAGES_PER_SECOND)
        
        except KeyboardInterrupt:
            print("\nShutting down producer...")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            if producer:
                print("Flushing remaining messages and closing producer.")
                producer.flush(timeout=10) # Ensure all async messages are sent
                producer.close()
                print("Producer closed.")
    else:
        print("Failed to create Kafka producer. Exiting.") 