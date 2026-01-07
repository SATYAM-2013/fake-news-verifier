import pandas as pd

df = pd.read_csv("news_dataset.csv")

# Clean text
df["text"] = df["text"].astype(str)
df["word_count"] = df["text"].str.split().apply(len)

# Short headlines
short_df = df[df["word_count"] <= 40][["text", "label"]]

# Full articles
full_df = df[df["word_count"] > 25][["text", "label"]]

short_df.to_csv("short_news.csv", index=False)
full_df.to_csv("full_news.csv", index=False)

print("Short news samples:", len(short_df))
print("Full news samples:", len(full_df))

print("\nShort news label distribution:")
print(short_df["label"].value_counts())

print("\nFull news label distribution:")
print(full_df["label"].value_counts())
