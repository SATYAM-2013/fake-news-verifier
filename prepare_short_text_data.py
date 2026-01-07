import pandas as pd

df = pd.read_csv("news_dataset.csv")

# Word count
df["word_count"] = df["text"].astype(str).str.split().apply(len)

# Keep short texts (headlines / short news)
short_df = df[df["word_count"] <= 60]

print("Original samples:", len(df))
print("Short-text samples:", len(short_df))

# Keep only required columns
short_df = short_df[["text", "label"]]

short_df.to_csv("short_news_dataset.csv", index=False)
