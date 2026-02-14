# LangGraph Studio ローカル環境

## 1. Python 仮想環境

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install "langgraph-cli[inmem]"
```

## 2. 環境変数ファイル

```bash
cp .env.example .env
```

## 3. LangGraph 開発サーバーを起動

```bash
langgraph dev
```

デフォルトのローカル API エンドポイント:

- `http://127.0.0.1:2024`

Studio が自動で開かない場合:

- `https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024`

## 同梱グラフ

- グラフ ID: `sample`
- 開始ノード: `transform_text`
- 入力ステートキー: `user_input`
- 出力ステートキー: `result`
