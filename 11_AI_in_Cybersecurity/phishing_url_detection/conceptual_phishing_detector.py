import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
from urllib.parse import urlparse # For basic URL parsing
import re # For IP address regex

# Optional: For more advanced domain parsing. Install with: pip install tldextract
# import tldextract

# --- Configuration & Constants ---
DATA_FILE = 'sample_urls.csv'
TARGET_COLUMN = 'label'
TEST_SIZE = 0.3
RANDOM_STATE = 42

# --- Feature Extraction Functions (Very Basic Lexical Features) ---

def has_ip_address(url):
    """Check if the hostname in the URL is an IP address."""
    try:
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname
        if hostname and re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", hostname):
            return 1
    except Exception:
        return 0 # Error in parsing
    return 0

def url_length(url):
    return len(url)

def count_dots(url):
    return url.count('.')

def count_hyphens(url):
    return url.count('-')

def count_at_symbol(url):
    return url.count('@')

def count_question_mark(url):
    return url.count('?')

def count_ampersand(url):
    return url.count('&')

def count_equals(url):
    return url.count('=')

def count_slashes_in_path(url):
    try:
        parsed_url = urlparse(url)
        return parsed_url.path.count('/')
    except Exception:
        return 0

def count_digits(url):
    return sum(c.isdigit() for c in url)

def has_suspicious_keywords(url_lower):
    """Check for common phishing-related keywords (very basic)."""
    keywords = ['login', 'verify', 'account', 'secure', 'update', 'signin', 'banking', 'confirm']
    for kw in keywords:
        if kw in url_lower:
            return 1
    return 0

def extract_lexical_features(df, url_column_name='url'):
    """Extracts a set of lexical features from a DataFrame of URLs."""
    print("Extracting lexical features...")
    features_df = pd.DataFrame()
    
    df['url_lower'] = df[url_column_name].astype(str).str.lower() # Ensure string and lowercase

    features_df['url_len'] = df[url_column_name].apply(url_length)
    features_df['has_ip'] = df[url_column_name].apply(has_ip_address)
    features_df['num_dots'] = df[url_column_name].apply(count_dots)
    features_df['num_hyphens'] = df[url_column_name].apply(count_hyphens)
    features_df['has_at'] = df[url_column_name].apply(count_at_symbol)
    features_df['has_question'] = df[url_column_name].apply(count_question_mark)
    features_df['has_ampersand'] = df[url_column_name].apply(count_ampersand)
    features_df['has_equals'] = df[url_column_name].apply(count_equals)
    features_df['path_slashes'] = df[url_column_name].apply(count_slashes_in_path)
    features_df['num_digits'] = df[url_column_name].apply(count_digits)
    features_df['has_keywords'] = df['url_lower'].apply(has_suspicious_keywords)
    
    # Example using tldextract (if you have it installed and uncommented the import)
    # def get_domain_len(url):
    #     try:
    #         ext = tldextract.extract(url)
    #         return len(ext.domain)
    #     except Exception:
    #         return 0
    # features_df['domain_len'] = df[url_column_name].apply(get_domain_len)

    print("Lexical features extracted. Sample:\n", features_df.head())
    return features_df

# --- Main Script Logic ---
def load_data_and_train(file_path, target_column):
    print(f"Loading data from {file_path}...")
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: Data file '{file_path}' not found.")
        return

    print("Sample data head:\n", df.head())
    print(f"\nShape of data: {df.shape}")
    print(f"Value counts for target '{target_column}':\n{df[target_column].value_counts()}\n")

    # Extract features
    X_features = extract_lexical_features(df, 'url')
    
    # Encode target labels
    label_encoder = LabelEncoder()
    y_labels = label_encoder.fit_transform(df[target_column])
    print(f"\nTarget classes mapped by LabelEncoder: {dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))}")

    # Split data
    print("\nSplitting data into training and testing sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_features, y_labels, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y_labels
    )
    print(f"Training set shape: X_train={X_train.shape}, y_train={y_train.shape}")
    print(f"Testing set shape: X_test={X_test.shape}, y_test={y_test.shape}")

    # Train a simple model (Logistic Regression for this example)
    print("\nTraining a Logistic Regression model...")
    model = LogisticRegression(random_state=RANDOM_STATE, max_iter=1000, solver='liblinear')
    model.fit(X_train, y_train)
    print("Model training complete.")

    # Evaluate
    print("\nMaking predictions on the test set...")
    y_pred = model.predict(X_test)
    
    y_test_orig_labels = label_encoder.inverse_transform(y_test)
    y_pred_orig_labels = label_encoder.inverse_transform(y_pred)

    print("\nEvaluating the model...")
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test_orig_labels, y_pred_orig_labels, zero_division=0)

    print(f"Accuracy: {accuracy:.4f}")
    print("Classification Report:\n", report)

if __name__ == "__main__":
    print("--- Conceptual Phishing URL Detector ---")
    load_data_and_train(DATA_FILE, TARGET_COLUMN)
    print("\n--- End of Conceptual Phishing Detector Script ---") 