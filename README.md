# Music Recommender

楽曲の音響特徴量から「似た曲」を推薦するコンテンツベース推薦システム。

## 概要

Spotifyの楽曲データ（約11万曲）から、danceability・energy・valence など9つの音響特徴量を使い、コサイン類似度で類似楽曲を推薦します。

## 使い方

```bash
pip install pandas scikit-learn
python recommend.py
```

データセットは [Spotify Tracks Dataset](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset) から取得し、`dataset.csv` としてルートに配置してください。

実行結果の例：

```
▼「Insane」に似た曲
        track_name         artists  track_genre    _score
              Numb           Lithe         soul  0.988052
        I Believed  Skinny Atlas...        chill  0.981464
```

## 技術

- Python / pandas / scikit-learn
- 特徴量の標準化（StandardScaler）
- コサイン類似度による近傍探索

## 設計の経緯

当初はSpotify Web APIの audio-features エンドポイントから音響特徴量を直接取得する設計だった。しかし2024年11月の仕様変更で新規アプリからのアクセスが制限されており、加えて無料アカウントではアプリ登録自体に制約があったため、同等の特徴量を含む公開データセットを利用する構成に切り替えた。

## 現状の課題

特徴量に数値情報しか含まれないため、テンポやエネルギーが近ければジャンルや言語が大きく異なる楽曲も上位に来る。（例：[実際に出た結果を書く]）

改善案として、ジャンル情報のone-hot化、popularityによるフィルタリングを検討中。