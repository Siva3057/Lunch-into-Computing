"""
Spam classifier: Naive Bayes (from spam_classifier.py) vs keyword rule (from emailClassifier.js).

The training emails are exactly the 5 from the course script. The 20 test emails
are hand-written for this exercise (see spam_dataset.csv), so results are
illustrative only - this is NOT a public benchmark dataset.
"""

import json

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

df = pd.read_csv("spam_dataset.csv")
train, test = df[df.split == "train"], df[df.split == "test"]

# --- Model 1: Naive Bayes, same pipeline as the course script ---
model = Pipeline([("vectorizer", CountVectorizer()), ("classifier", MultinomialNB())])
model.fit(train.text, train.label)
nb_pred = model.predict(test.text)


# --- Model 2: keyword rule, a direct port of classifyEmail() from emailClassifier.js ---
SPAM_KEYWORDS = ["win", "free", "cash", "selected", "prize"]


def keyword_classify(email: str) -> int:
    lower = email.lower()
    return int(any(k in lower for k in SPAM_KEYWORDS))  # substring match, like JS includes()


kw_pred = test.text.map(keyword_classify)


def report(name, y_true, y_pred):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    m = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision_spam": precision_score(y_true, y_pred, zero_division=0),
        "recall_spam": recall_score(y_true, y_pred, zero_division=0),
        "TP": int(tp), "FP": int(fp), "FN": int(fn), "TN": int(tn),
    }
    print(f"{name}: " + ", ".join(f"{k}={v:.2f}" if isinstance(v, float) else f"{k}={v}" for k, v in m.items()))
    return m


print(f"Train: {len(train)} emails | Test: {len(test)} emails\n")
results = {
    "naive_bayes": report("Naive Bayes ", test.label, nb_pred),
    "keyword_rule": report("Keyword rule", test.label, kw_pred),
}

# Show every mistake
for name, pred in [("Naive Bayes", nb_pred), ("Keyword rule", kw_pred)]:
    print(f"\n{name} errors:")
    for text, true, p in zip(test.text, test.label, pred):
        if true != p:
            kind = "FALSE POSITIVE (ham flagged)" if p == 1 else "FALSE NEGATIVE (spam missed)"
            print(f"  {kind}: {text}")

with open("spam_metrics.json", "w") as f:
    json.dump(results, f, indent=2)
