import pandas as pd

df = pd.read_csv("dataset.csv")

print("曲数:", len(df))
print("\n列の一覧:")
print(df.columns.tolist())
print("\n最初の3曲:")
print(df[["track_name", "artists", "danceability", "energy", "tempo"]].head(3))