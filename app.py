import pandas as pd
import numpy as np
import streamlit as st
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

st.title("Music Recommender")
st.caption("音響特徴量とジャンルから似た曲を推薦します")


@st.cache_data
def load_data():
    df = pd.read_csv("dataset.csv")
    df = df.drop(columns=["Unnamed: 0.1", "Unnamed: 0"])
    df = df.drop_duplicates(subset=["track_name", "artists"]).reset_index(drop=True)

    features = ["danceability", "energy", "loudness", "speechiness",
                "acousticness", "instrumentalness", "liveness", "valence", "tempo"]
    X = StandardScaler().fit_transform(df[features])
    genre = pd.get_dummies(df["track_genre"]).astype(int).values
    return df, X, genre


df, X, genre = load_data()

# 入力欄
song = st.text_input("曲名を入力", "Insane")
weight = st.slider("ジャンルの重み", 0.0, 1.0, 0.3, 0.1)

if st.button("推薦する"):
    matches = df[df["track_name"].str.lower() == song.lower()]

    if matches.empty:
        st.error(f"「{song}」は見つかりませんでした")
    else:
        idx = matches.index[0]
        X_new = np.hstack([X, genre * weight])
        sim = cosine_similarity([X_new[idx]], X_new)[0]

        df["_score"] = sim
        result = df.drop(index=idx).nlargest(10, "_score")

        st.subheader(f"「{df.loc[idx, 'track_name']}」に似た曲")
        st.dataframe(
            result[["track_name", "artists", "track_genre", "_score"]],
            hide_index=True,
        )