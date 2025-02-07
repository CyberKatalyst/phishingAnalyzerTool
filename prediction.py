import pandas as pd
import re
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report


def anomaly_body_detection(body):

    df = pd.read_csv('body_email_detection.csv')

    # Preprocess the email text
    def preprocess_text(text):
        # Check if the text is a string before processing
        if isinstance(text, str):
            # Convert text to lowercase
            text = text.lower()
            # Remove URLs
            text = re.sub(r'http\S+', '', text)
            # Remove emails
            text = re.sub(r'\S+@\S+', '', text)
            # Remove special characters and digits
            text = re.sub(r'[^a-zA-Z\s]', '', text)
        else:
            # If the value is not a string, return an empty string or handle it as needed
            text = ''
        return text

    # Apply preprocessing to the email text
    df['cleaned_text'] = df['Email Text'].apply(preprocess_text)

    # Vectorize the text using TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
    X = vectorizer.fit_transform(df['cleaned_text'])

    # Prepare the target variable
    y = np.where(df['Email Type'] == 'Phishing Email', 1, 0)  # 1 for phishing, 0 for safe

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Train a Logistic Regression model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Preprocess the new email text
    new_body_cleaned = preprocess_text(body)

    # Convert the new email into the same vectorized format
    new_body_vectorized = vectorizer.transform([new_body_cleaned])

    # Predict whether the new email is suspicious or safe
    prediction = model.predict(new_body_vectorized)

    # Output the result
    if prediction[0] == 1:
        print(" 🔴 Based on anomaly detection, the body is suspicious")
    else:
        print(" ✅ Based on anomaly detection, the body is safe.")
