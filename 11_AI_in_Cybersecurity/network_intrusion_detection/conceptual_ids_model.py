import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
import numpy as np

# --- Configuration & Constants ---
DATA_FILE = 'sample_network_data.csv'
TARGET_COLUMN = 'label'
# For simplicity, we will use a few categorical and numerical features
# In a real scenario, feature selection and engineering would be extensive.
CATEGORICAL_FEATURES = ['protocol_type', 'service', 'flag']
NUMERICAL_FEATURES = ['duration', 'src_bytes', 'dst_bytes', 'land', 'wrong_fragment', 'urgent']
TEST_SIZE = 0.3 # 30% for testing
RANDOM_STATE = 42

def load_and_preprocess_data(file_path, target_column, cat_features, num_features):
    """Loads data, performs basic preprocessing (label encoding for categoricals)."""
    print(f"Loading data from {file_path}...")
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: Data file '{file_path}' not found.")
        return None, None

    print("Sample data head:\n", df.head())
    print(f"\nShape of data: {df.shape}")
    print(f"Value counts for target '{target_column}':\n{df[target_column].value_counts()}\n")

    # Separate features (X) and target (y)
    X = df.drop(columns=[target_column])
    y = df[target_column]

    # Basic preprocessing: Label encode categorical features
    # In a real NIDS, more sophisticated encoding (OneHotEncoder, target encoding, etc.) 
    # and scaling for numerical features would be applied.
    label_encoders = {}
    for col in cat_features:
        if col in X.columns:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col])
            label_encoders[col] = le # Store for potential inverse transform or new data
            print(f"Label encoded column: {col}")
        else:
            print(f"Warning: Categorical feature '{col}' not found in dataframe.")

    # Ensure all expected numerical features are present, fill missing with 0 if any (very basic imputation)
    for col in num_features:
        if col not in X.columns:
            print(f"Warning: Numerical feature '{col}' not found. Adding it with zeros.")
            X[col] = 0
    
    # Select only the defined features for the model
    selected_features = cat_features + num_features
    X = X[[col for col in selected_features if col in X.columns]]

    print("\nPreprocessed features head:\n", X.head())
    
    # Label encode the target variable
    target_encoder = LabelEncoder()
    y = target_encoder.fit_transform(y)
    print(f"\nTarget classes mapped by LabelEncoder: {dict(zip(target_encoder.classes_, target_encoder.transform(target_encoder.classes_)))}")

    return X, y, target_encoder

def train_evaluate_model(X, y, target_encoder):
    """Splits data, trains a Decision Tree, and evaluates it."""
    print("\nSplitting data into training and testing sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    print(f"Training set shape: X_train={X_train.shape}, y_train={y_train.shape}")
    print(f"Testing set shape: X_test={X_test.shape}, y_test={y_test.shape}")

    print("\nTraining a Decision Tree Classifier...")
    # Using a simple Decision Tree for this conceptual example.
    # Real NIDS might use more complex models like Random Forests, Gradient Boosting, or Neural Networks.
    model = DecisionTreeClassifier(random_state=RANDOM_STATE)
    model.fit(X_train, y_train)
    print("Model training complete.")

    print("\nMaking predictions on the test set...")
    y_pred = model.predict(X_test)

    # Convert numerical predictions back to original labels for report
    y_test_labels = target_encoder.inverse_transform(y_test)
    y_pred_labels = target_encoder.inverse_transform(y_pred)

    print("\nEvaluating the model...")
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test_labels, y_pred_labels, zero_division=0)

    print(f"Accuracy: {accuracy:.4f}")
    print("Classification Report:\n", report)
    
    # Feature importances (for tree-based models)
    if hasattr(model, 'feature_importances_'):
        importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
        print("\nFeature Importances:\n", importances)

if __name__ == "__main__":
    print("--- Conceptual Network Intrusion Detection Model ---")
    X_processed, y_processed, target_le = load_and_preprocess_data(
        DATA_FILE, TARGET_COLUMN, CATEGORICAL_FEATURES, NUMERICAL_FEATURES
    )

    if X_processed is not None and y_processed is not None:
        train_evaluate_model(X_processed, y_processed, target_le)
    else:
        print("Halting due to errors in data loading or preprocessing.")
    print("\n--- End of Conceptual NIDS Model Script ---") 