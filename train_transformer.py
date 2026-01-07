import pandas as pd
import torch
from datasets import Dataset
from transformers import (
    DistilBertTokenizerFast,
    DistilBertForSequenceClassification,
    Trainer,
    TrainingArguments
)

# Load dataset
df = pd.read_csv("full_news.csv")

# Keep only needed columns
df = df[["text", "label"]]

# Convert to HuggingFace Dataset
dataset = Dataset.from_pandas(df)

# Train-test split
dataset = dataset.train_test_split(test_size=0.2)

# Load tokenizer
tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")

# Tokenization function
def tokenize(batch):
    return tokenizer(
        batch["text"],
        padding=True,
        truncation=True,
        max_length=256
    )

dataset = dataset.map(tokenize, batched=True)
dataset = dataset.remove_columns(["text"])
dataset.set_format("torch")

# Load model
model = DistilBertForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
    num_labels=2,
    id2label={0: "FAKE", 1: "REAL"},
    label2id={"FAKE": 0, "REAL": 1}
)

# Training settings
training_args = TrainingArguments(
    output_dir="./model",
evaluation_strategy="no",

    save_strategy="epoch",

    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,

    num_train_epochs=1,
    fp16=True,
    no_cuda=False,

    logging_steps=200,
    report_to="none"
)



# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    tokenizer=tokenizer
)

# Train
trainer.train()

# Save model
model.save_pretrained("model")
tokenizer.save_pretrained("model")


print("✅ Training complete. Model saved.")
