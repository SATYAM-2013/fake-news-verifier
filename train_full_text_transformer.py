import pandas as pd
from datasets import Dataset
from transformers import (
    DistilBertTokenizerFast,
    DistilBertForSequenceClassification,
    Trainer,
    TrainingArguments
)

# =========================
# LOAD FULL NEWS DATASET
# =========================
df = pd.read_csv("full_news.csv")
df = df[["text", "label"]]

dataset = Dataset.from_pandas(df)
dataset = dataset.train_test_split(test_size=0.2)

tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")

def tokenize(batch):
    return tokenizer(
        batch["text"],
        padding=True,
        truncation=True,
        max_length=512   # IMPORTANT for long text
    )

dataset = dataset.map(tokenize, batched=True)
dataset = dataset.remove_columns(["text"])
dataset.set_format("torch")

model = DistilBertForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
    num_labels=2,
    id2label={0: "FAKE", 1: "REAL"},
    label2id={"FAKE": 0, "REAL": 1}
)

training_args = TrainingArguments(
    output_dir="./full_text_model",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    per_device_train_batch_size=8,   # lower because long text
    per_device_eval_batch_size=8,
    num_train_epochs=2,
    logging_steps=200,
    fp16=True,
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    tokenizer=tokenizer
)

trainer.train()

model.save_pretrained("full_text_model")
tokenizer.save_pretrained("full_text_model")

print("✅ Full-text model trained and saved")
