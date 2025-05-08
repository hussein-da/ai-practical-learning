import time
import json
from kafka import KafkaConsumer, TopicPartition
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Configuration
KAFKA_BROKER = 'localhost:9092'
SOURCE_TOPIC_NAME = 'raw_text_topic'
CONSUMER_GROUP_ID = 'sentiment_analyzers_group' # Allows multiple consumers to parallelize work

# Download VADER lexicon if not already present (run once)
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except nltk.downloader.DownloadError:
    print("Downloading VADER lexicon for NLTK...")
    nltk.download('vader_lexicon')

# Initialize Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

def get_sentiment(text):
    """Analyzes sentiment of the text using VADER.
    Returns a dict with positive, negative, neutral, compound scores,
    and an overall sentiment label.
    """
    if not text or not isinstance(text, str):
        return {
            'positive': 0.0,
            'negative': 0.0,
            'neutral': 1.0,
            'compound': 0.0,
            'label': 'NEUTRAL'
        }

    scores = sia.polarity_scores(text)
    compound = scores['compound']
    
    label = 'NEUTRAL'
    if compound > 0.05:
        label = 'POSITIVE'
    elif compound < -0.05:
        label = 'NEGATIVE'
        
    return {
        'positive': scores['pos'],
        'negative': scores['neg'],
        'neutral': scores['neu'],
        'compound': compound,
        'label': label
    }

def create_consumer(broker, topic, group_id):
    """Creates and returns a KafkaConsumer instance."""
    try:
        consumer = KafkaConsumer(
            bootstrap_servers=broker,
            auto_offset_reset='latest', # Start reading at the end of the log if no offset is stored
            enable_auto_commit=True,      # Commit offsets automatically
            group_id=group_id,
            value_deserializer=lambda v: json.loads(v.decode('utf-8'))
        )
        consumer.subscribe([topic])
        print(f"Consumer (Group: {group_id}) connected to Kafka and subscribed to topic '{topic}'")
        return consumer
    except Exception as e:
        print(f"Error creating or connecting Kafka consumer: {e}")
        return None

if __name__ == "__main__":
    consumer = create_consumer(KAFKA_BROKER, SOURCE_TOPIC_NAME, CONSUMER_GROUP_ID)

    if consumer:
        print(f"Listening for messages on topic '{SOURCE_TOPIC_NAME}'. Press Ctrl+C to stop.")
        try:
            for message in consumer:
                # message.value will be the dict sent by the producer
                data = message.value
                text_to_analyze = data.get('text', '')
                message_id = data.get('id', 'N/A')
                
                print(f"\nReceived message ID: {message_id} from partition {message.partition} offset {message.offset}")
                print(f"  Raw text: '{text_to_analyze[:100]}...'")
                
                sentiment_scores = get_sentiment(text_to_analyze)
                
                print(f"  Sentiment: {sentiment_scores['label']} (Compound: {sentiment_scores['compound']:.4f})")
                # print(f"  Scores: Pos={sentiment_scores['positive']:.2f}, Neu={sentiment_scores['neutral']:.2f}, Neg={sentiment_scores['negative']:.2f}")
                
                # Here you could, for example, send the enriched data to another topic:
                # enriched_message = {**data, 'sentiment': sentiment_scores}
                # producer.send('analyzed_text_topic', enriched_message)
                
        except KeyboardInterrupt:
            print("\nShutting down consumer...")
        except Exception as e:
            print(f"An unexpected error occurred during message consumption: {e}")
        finally:
            if consumer:
                print("Closing Kafka consumer.")
                consumer.close()
                print("Consumer closed.")
    else:
        print("Failed to create Kafka consumer. Exiting.") 