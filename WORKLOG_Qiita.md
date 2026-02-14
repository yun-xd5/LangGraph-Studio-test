# LangGraph Studio のローカル開発環境を最小構成で立ち上げた記録

## はじめに
LangGraph を触り始めるときに、まず「ローカルで確実に動く最小構成」を作っておくと後の検証が楽になります。
この記事は、`langgraph dev` で Studio 連携まで確認できる環境を作った作業ログです。

- 作業日: 2026-02-14
- 直近コミット: `b8610f5` (`LangGraph Studio環境を初期構築`)

## ゴール
今回のゴールは次の3点です。

1. `langgraph dev` でローカルAPI (`http://127.0.0.1:2024`) を起動できること
2. Studio からグラフを確認できること
3. サンプルの1ノードグラフで入出力が確認できること

## プロジェクト構成

```text
.
├── agent.py
├── langgraph.json
├── pyproject.toml
├── README.md
└── .env.example
```

## 実施内容

### 1. 依存関係の最小化
`pyproject.toml` は `langgraph>=0.2.0` を基本依存として定義。
ローカル実行用に `langgraph-cli[inmem]` を追加インストールする前提にしました。

### 2. 最小グラフの実装
`agent.py` では `StateGraph` を使い、1ノードだけのシンプルなグラフを作成。

- State: `user_input`, `result`
- Node: `transform_text`
- 処理: `Processed: {user_input}` という文字列を `result` に格納
- Edge: `START -> transform_text -> END`

最小構成にしているので、ノード追加や分岐の土台として流用しやすいです。

### 3. 起動手順の明文化
`README.md` に以下の手順を整理。

1. venv作成・有効化
2. `pip install -e .`
3. `pip install "langgraph-cli[inmem]"`
4. `.env.example` を `.env` にコピー
5. `langgraph dev` を実行

Studio が自動起動しないケース向けに、接続URLも記載しました。

## 動作確認ポイント

- `langgraph dev` 実行後、`http://127.0.0.1:2024` が応答する
- Studio で graph id `sample` が見える
- `user_input` に値を入れて実行すると `result` に `Processed: ...` が返る

## ハマりどころメモ

- `.env` はサンプル段階では必須ではないが、運用を見据えて先に置いておくと安全
- 依存を増やしすぎると初期検証が重くなるため、最初は1ノードで通す方が切り分けしやすい

## 今後やること

1. ノードを2つ以上に増やしてステップ実行を検証
2. 条件分岐 (`add_conditional_edges`) を追加
3. 外部API呼び出しを入れた際のエラーハンドリング方針を決める

## まとめ
最小構成の LangGraph 環境を先に固めることで、以降の機能追加を「グラフ設計そのものの検証」に集中させやすくなりました。
まずは 1 ノードで確実に動かし、その後に段階的に複雑化していく進め方が有効でした。
