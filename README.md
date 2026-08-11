# Music Recommender

楽曲の音響特徴量から「似た曲」を推薦するコンテンツベース推薦システム。

![demo](https://github.com/user-attachments/assets/111e406f-a94b-4842-be4a-86b81ebf9208)

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

特徴量に数値情報しか含まれないため、テンポやエネルギーが近ければジャンルや言語が大きく異なる楽曲も上位に来る。(例：「Insane」で実行した結果、上位はsoulやchillなど落ち着いた曲で揃った一方、5位にKodak Blackのhip-hop、9位にブラジル音楽（mpb）が混在した。
改善案として、ジャンル情報のone-hot化、popularityによるフィルタリングを検討中。)

## 改善：ジャンル情報の追加

数値特徴量のみでは音楽的に無関係な楽曲が上位に来る問題に対し、
track_genre をone-hot encodingして特徴量に追加した。

ただし113次元のジャンル情報をそのまま連結すると距離計算を支配し、
推薦結果が同一ジャンルのみになった（実質的にジャンルフィルタと同じ）。
そこでジャンル部分に重み係数を掛け、値を変えて検証した。

| 重み | 同ジャンル数（上位10曲） |
|---|---|
| 0.0 | 1 |
| 0.3 | 4 |
| 0.5 | 9 |
| 1.0 | 10 |

同一ジャンルを優先しつつ音楽的に近い他ジャンルも残る 0.3 を採用した。