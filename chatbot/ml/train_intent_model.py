# chatbot/ml/train_intent_model.py
import joblib
import os
import re
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.utils import resample

from chatbot.ml.training_data import CHATBOT_TRAINING_DATA

# --- Preprocessing function ---
def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)  # remove punctuation
    return text.strip()

# --- Prepare data ---
X = [preprocess(text) for text, label in CHATBOT_TRAINING_DATA]
y = [label for text, label in CHATBOT_TRAINING_DATA]

# --- Balance dataset (oversample small classes) ---
data = list(zip(X, y))
labels_count = Counter(y)
max_count = max(labels_count.values())

balanced_data = []
for label in labels_count:
    items = [(x, l) for x, l in data if l == label]
    if len(items) < max_count:
        # oversample
        items_upsampled = resample(items, replace=True, n_samples=max_count, random_state=42)
    else:
        items_upsampled = items
    balanced_data.extend(items_upsampled)

X_balanced, y_balanced = zip(*balanced_data)

# --- Create pipeline ---
model = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1,2), min_df=1)),
    ("clf", MultinomialNB())
])

# --- Train ---
model.fit(X_balanced, y_balanced)

# --- Save model ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
file_path = os.path.join(BASE_DIR, "intent_model.joblib")
joblib.dump(model, file_path)
print(f"Model saved to {file_path}")
