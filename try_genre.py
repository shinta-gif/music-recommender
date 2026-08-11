import pandas as pd

df = pd.read_csv("dataset.csv")

df = df.drop(columns=["Unnamed: 0.1", "Unnamed: 0"])
df = df.drop_duplicates(subset=["track_name", "artists"]).reset_index(drop=True)

print("ジャンルの種類:", df["track_genre"].nunique())
print(df["track_genre"].unique()[:20])
genre_dummies = pd.get_dummies(df["track_genre"]).astype(int)
print(genre_dummies.shape)
print(genre_dummies.head())

features = ["danceability", "energy", "loudness", "speechiness",
            "acousticness", "instrumentalness", "liveness", "valence", "tempo"]

import numpy as np
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X = scaler.fit_transform(df[features])
X_new = np.hstack([X, genre_dummies.values])
print(X_new.shape)
print("重複除去前のジャンル数:", pd.read_csv("dataset.csv")["track_genre"].nunique())

before = set(pd.read_csv("dataset.csv")["track_genre"].unique())
after = set(df["track_genre"].unique())
print(before - after)