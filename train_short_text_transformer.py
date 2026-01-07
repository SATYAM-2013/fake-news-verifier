import pandas as pd
import torch
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments
)

# -----------------------
# Paths
# -----------------------
BASE_MODEL_PATH = "fine_tuned_model" # Stage-1 model
SHORT_DATASET_PATH = "short_news_dataset.csv"
OUTPUT_DIR = "fine_tuned_model"          # Final model

# -----------------------
# Load dataset
# -----------------------
df = pd.read_csv(SHORT_DATASET_PATH)
dataset = Dataset.from_pandas(df)

# -----------------------
# Tokenizer & Model
# -----------------------
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(
    BASE_MODEL_PATH,
    num_labels=2
)

# -----------------------
# Tokenization (short-text optimized)
# -----------------------
def tokenize(batch):
    return tokenizer(
        batch["text"],
        padding="max_length",
        truncation=True,
        max_length=128      # IMPORTANT for short texts
    )

dataset = dataset.map(tokenize, batched=True)
dataset = dataset.train_test_split(test_size=0.1, seed=42)

dataset.set_format(
    type="torch",
    columns=["input_ids", "attention_mask", "label"]
)

# -----------------------
# Training arguments (anti-overfitting)
# -----------------------
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=1e-5,              # LOWER LR = safer
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,              # Small dataset → more epochs
    weight_decay=0.01,
    load_best_model_at_end=True,
    metric_for_best_model="loss",
    logging_steps=50,
    report_to="none",
    fp16=torch.cuda.is_available()
)

# -----------------------
# Trainer
# -----------------------
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    tokenizer=tokenizer
)

# -----------------------
# Train
# -----------------------
trainer.train()

# -----------------------
# Save final model
# -----------------------
trainer.save_model(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

print("✅ Short-text fine-tuning complete. Model saved.")
