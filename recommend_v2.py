import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

# データ読み込み
df = pd.read_csv("dataset.csv")

# 不要な列を削除、重複曲を除去
df = df.drop(columns=["Unnamed: 0.1", "Unnamed: 0"])
df = df.drop_duplicates(subset=["track_name", "artists"]).reset_index(drop=True)

# 推薦に使う特徴量
features = ["danceability", "energy", "loudness", "speechiness",
            "acousticness", "instrumentalness", "liveness", "valence", "tempo"]

genre_dummies = pd.get_dummies(df["track_genre"]).astype(int)
print(genre_dummies.shape)
print(genre_dummies.head())


# 標準化（単位がバラバラなので揃える）
scaler = StandardScaler()
X = scaler.fit_transform(df[features])
X_new = np.hstack([X, genre_dummies.values * 0.3])

def recommend(song_name, top_n=10):
    matches = df[df["track_name"].str.lower() == song_name.lower()]
    if matches.empty:
        print(f"「{song_name}」は見つかりませんでした")
        return

    idx = matches.index[0]
    sim = cosine_similarity([X_new[idx]], X_new)[0]

    df["_score"] = sim
    result = df.drop(index=idx).nlargest(top_n, "_score")

    print(f"\n▼「{df.loc[idx, 'track_name']}」に似た曲")
    print(result[["track_name", "artists", "track_genre", "_score"]].to_string(index=False))


recommend("insane")