import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
import os.path


def check_keyword_existance():
    file_path = 'C:\\Phishing Analysis\\suspicious_keywords.csv'
    # If the file exists, then load it as DataFrame
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        return file_path
    else:
        return None


def predication(email_body_text):
    # Get the path of the CSV file
    path = check_keyword_existance()
    # Load the DataFrame
    df = pd.read_csv(path)

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(df['Suspicious Keywords'], df['Label'], test_size=0.2, random_state=42)

    # Convert text data to TF-IDF feature vectors
    vectorizer = TfidfVectorizer()
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # Train a Naive Bayes classifier
    model = MultinomialNB()
    model.fit(X_train_tfidf, y_train)

    # Make predictions on the test set
    y_pred = model.predict(X_test_tfidf)

    # Transform the new email text to the same TF-IDF format
    new_email_tfidf = vectorizer.transform([email_body_text])

    # Predict the class of the new email
    predicted_class = model.predict(new_email_tfidf)
    classification = predicted_class[0]

    # Strip whitespace and check again
    classification = classification.strip()

    if classification.lower() == 'scam':
        result = "possible scam"
        return result
    else:
        return None

