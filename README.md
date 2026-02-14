# LangGraph Studio ローカル環境（最小構成）

このリポジトリは、LangGraph をローカルで最小構成で動かすためのサンプルです。

- Graph ID: `sample`
- Node: `transform_text`
- Input: `user_input`
- Output: `result`（ノードで生成）

## 前提

- Python 3.11+
- `python3-venv` がインストール済み

## セットアップ

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install "langgraph-cli[inmem]"
cp .env.example .env
```

## 起動

```bash
langgraph dev --host 127.0.0.1 --port 2024
```

- API Docs: `http://127.0.0.1:2024/docs`
- Studio: `https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024`

## テスト方法（手動）

1. Studio で `sample` グラフを選ぶ
2. `User Input` に文字列を入れて `Submit`
3. `result` に `Processed: <入力文字列>` が返ることを確認

## SSHリモートで使う場合

ローカルPCで SSH ポートフォワードを張ります。

```bash
ssh -L 2024:127.0.0.1:2024 <user>@<remote-host>
```

その状態でリモート側で `langgraph dev --host 127.0.0.1 --port 2024` を起動し、
ローカルPCのブラウザで Studio URL を開きます。

## 注意

- Studio UI は `smith.langchain.com` 側の画面を利用するため、LangSmith ログインが必要です。
- `.env` は機密情報を含む可能性があるため、Git 管理しません（`.gitignore` で除外）。
- プロジェクトを別パスへ移動した場合は、`.venv` の再作成を推奨します。

## GitHub公開

```bash
git remote add origin https://github.com/<YOUR_ID>/<REPO>.git
git branch -M main
git push -u origin main
```
