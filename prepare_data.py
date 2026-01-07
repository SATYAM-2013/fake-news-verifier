import pandas as pd

# Load datasets
fake = pd.read_csv("fake_news.csv")
true = pd.read_csv("True.csv")

# Add labels
fake["label"] = 0   # Fake
true["label"] = 1   # Real

# Keep only text column
fake = fake[["text", "label"]]
true = true[["text", "label"]]

# Combine datasets
data = pd.concat([fake, true], axis=0)

# Shuffle data
data = data.sample(frac=1).reset_index(drop=True)

# Basic cleaning
data["text"] = data["text"].astype(str)
data = data[data["text"].str.len() > 20]  # remove very short junk

# Save final dataset
data.to_csv("news_dataset.csv", index=False)

print("✅ Dataset prepared successfully!")
print(data.head())
print("Total samples:", len(data))
