# LangGraph Studio のローカル開発環境を最小構成で立ち上げた記録

## はじめに
LangGraph を触り始めるときに、まず「ローカルで確実に動く最小構成」を作っておくと後の検証が楽になります。
この記事は、`langgraph dev` で Studio 連携まで確認できる環境を作った作業ログです。

- 作業日: 2026-02-14
- 初回コミット: `b8610f5` (`LangGraph Studio環境を初期構築`)

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

## Codexで構築した経緯

今回の環境は、Codexと対話しながら次の順序で構築しました。

1. 空ディレクトリに最小ファイル群（`agent.py`, `langgraph.json`, `pyproject.toml`, `README.md`, `.env.example`）を一括作成
2. `python3 -m venv .venv` 実行時に `ensurepip is not available` で失敗
3. `python3-venv` 未導入が原因と判明し、ユーザー側で `apt` 導入
4. `.venv` 作成と `pip install -e .` / `pip install "langgraph-cli[inmem]"` を実施
5. `langgraph dev` を短時間起動して、`sample` グラフの読み込みと `http://127.0.0.1:2024` 起動を確認
6. 実行時生成物（`*.egg-info/`, `.langgraph_api/`）を `.gitignore` に追加して管理ノイズを除去

この進め方により、環境依存エラーの切り分けと、最小構成の起動確認を短いサイクルで実施できました。

## 動作確認ポイント

- `langgraph dev` 実行後、`http://127.0.0.1:2024` が応答する
- Studio で graph id `sample` が見える
- `user_input` に値を入れて実行すると `result` に `Processed: ...` が返る

## ハマりどころメモ

- `.env` はサンプル段階では必須ではないが、運用を見据えて先に置いておくと安全
- 依存を増やしすぎると初期検証が重くなるため、最初は1ノードで通す方が切り分けしやすい
- Ubuntu系環境では `python3-venv` が未導入だと venv が作れない
- プロジェクトを別パスに移動すると、既存 `.venv` の shebang / パス参照が合わず `langgraph: コマンドが見つかりません` が出る場合がある


## 今後やること
## ディレクトリ移動時の対応ログ

`/home/yun/dev/test/ai/LangGraph/構築テスト/01.構築テスト` から  
`/home/yun/dev/test/ai/LangGraph/01.構築テスト` へ移動した後、仮想環境を再作成しました。

1. `deactivate` で既存 venv から抜ける
2. `rm -rf .venv`
3. `python3 -m venv .venv`
4. `source .venv/bin/activate`
5. `python -m pip install -e .`
6. `python -m pip install "langgraph-cli[inmem]"`

移動後は「同じ名前のフォルダでも絶対パスが変わる」ため、venv は作り直す前提で運用するのが安全です。

1. ノードを2つ以上に増やしてステップ実行を検証
2. 条件分岐 (`add_conditional_edges`) を追加
3. 外部API呼び出しを入れた際のエラーハンドリング方針を決める

## まとめ
最小構成の LangGraph 環境を先に固めることで、以降の機能追加を「グラフ設計そのものの検証」に集中させやすくなりました。
まずは 1 ノードで確実に動かし、その後に段階的に複雑化していく進め方が有効でした。
