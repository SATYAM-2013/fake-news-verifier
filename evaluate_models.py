import pandas as pd
from transformers import pipeline

short_model = pipeline(
    "text-classification",
    model="fine_tuned_model",
    tokenizer="fine_tuned_model"
)

full_model = pipeline(
    "text-classification",
    model="full_text_model",
    tokenizer="full_text_model"
)

df = pd.read_csv("full_news.csv")

correct = 0
total = 200   # test on 200 samples

for i in range(total):
    text = df.iloc[i]["text"]
    label = df.iloc[i]["label"]

    pred = full_model(text)[0]["label"]
    true_label = "FAKE" if label == 0 else "REAL"

    if pred == true_label:
        correct += 1

accuracy = (correct / total) * 100
print(f"Model Accuracy: {accuracy:.2f}%")
