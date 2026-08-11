# Music Recommender

楽曲の音響特徴量とジャンル情報から「似た曲」を推薦するコンテンツベース推薦システム。

![demo](https://github.com/user-attachments/assets/111e406f-a94b-4842-be4a-86b81ebf9208)

## 概要

Spotifyの楽曲データ（約11万曲）から、danceability・energy・valence など9つの音響特徴量と、ジャンル情報を組み合わせ、コサイン類似度で類似楽曲を推薦します。Webアプリ上でジャンルの重み係数を変更し、推薦結果の変化を確認できます。

## 使い方

```bash
pip install pandas scikit-learn streamlit
streamlit run app.py
```

データセットは [Spotify Tracks Dataset](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset) から取得し、`dataset.csv` としてルートに配置してください。

CLIで実行する場合は `python recommend.py`。

## 技術

- Python / pandas / scikit-learn / Streamlit
- 特徴量の標準化（StandardScaler）
- ジャンルのone-hot encoding + 重み付け
- コサイン類似度による近傍探索

## 設計の経緯

当初はSpotify Web APIの audio-features エンドポイントから音響特徴量を直接取得する設計だった。しかし2024年11月の仕様変更で新規アプリからのアクセスが制限されており、加えて無料アカウントではアプリ登録自体に制約があったため、同等の特徴量を含む公開データセットを利用する構成に切り替えた。

## 改善の過程

### 課題：数値特徴量のみでは音楽的に無関係な曲が混在する

「Insane」で実行した結果、上位はsoulやchillなど落ち着いた曲で揃った一方、5位にKodak Blackのhip-hop、9位にブラジル音楽（mpb）が入った。テンポやエネルギーが近ければ、ジャンルや言語が大きく異なる楽曲も上位に来てしまう。

### 対応：ジャンル情報のone-hot encoding

track_genre をone-hot化して特徴量に追加した。ただし113次元のジャンル情報をそのまま連結すると距離計算を支配し、推薦結果が同一ジャンルのみになった（実質的にジャンルフィルタと同じ）。

そこでジャンル部分に重み係数を掛け、値を変えて検証した。

| 重み | 上位10曲中の同ジャンル数 |
|---|---|
| 0.0 | 1 |
| 0.3 | 4 |
| 0.5 | 9 |
| 1.0 | 10 |

同一ジャンルを優先しつつ、音楽的に近い他ジャンルも残る 0.3 を採用した。

## 残っている課題

- 重みの選定が目視による判断にとどまっており、定量的な評価指標を用いていない
- 重複除去（曲名+アーティスト）の副作用で、ジャンルが1つ消失している
- 曲名が完全一致でしか検索できない
- 特徴量に歌詞・言語・年代の情報が含まれていない