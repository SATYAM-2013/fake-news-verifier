# Fake News Detection Project (Proper Version)

import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

nltk.download('stopwords', quiet=True)


stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = text.split()
    words = [stemmer.stem(word) for word in words if word not in stop_words]
    return " ".join(words)


# Load datasets
fake = pd.read_csv("fake_news.csv")
true = pd.read_csv("True.csv")

# Add labels
fake['label'] = 0   # Fake
true['label'] = 1   # Real

# Combine datasets
data = pd.concat([fake, true], axis=0)

# Shuffle data
data = data.sample(frac=1).reset_index(drop=True)

# Features and labels
X = data['text']
y = data['label']

# Convert text to numbers
vectorizer = TfidfVectorizer(
    stop_words='english',
    ngram_range=(1, 2),   # VERY IMPORTANT for short text
    max_df=0.9,
    min_df=3
)

X_vectorized = vectorizer.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized, y, test_size=0.2, random_state=42
)

# Train model
from sklearn.svm import LinearSVC
model = LinearSVC()

model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Model Accuracy:", accuracy)

# User input
news = input("Enter a news sentence: ")
news_vector = vectorizer.transform([news])
prediction = model.predict(news_vector)
score = model.decision_function(news_vector)
confidence = abs(score[0])
confidence = min(confidence, 1.0) * 100

if prediction[0] == 0:
    print("❌ Fake News")
else:
    print("✅ Real News")

print(f"Confidence: {confidence:.2f}%")
