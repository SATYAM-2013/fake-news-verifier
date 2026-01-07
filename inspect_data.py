import pandas as pd

df = pd.read_csv("news_dataset.csv")

print(df.columns)
print(df['label'].value_counts())
