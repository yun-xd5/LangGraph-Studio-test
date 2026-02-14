# LangGraph Studio ローカル環境（最小構成）

このリポジトリは、LangGraph + ローカルLLM（Ollama）を最小構成で動かすサンプルです。

- Graph ID: `sample`
- Node: `transform_text`
- Input: `user_input`
- Output: `result`

## 前提

- Python 3.11+
- `python3-venv` がインストール済み
- Ollama がインストール済み

## セットアップ

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install "langgraph-cli[inmem]"
cp .env.example .env
```

## ローカルLLM準備（Ollama）

```bash
ollama serve
ollama pull qwen2.5:7b
```

別モデルを使う場合は `.env` の `OLLAMA_MODEL` を変更します。

## 起動

```bash
langgraph dev --host 127.0.0.1 --port 2024
```

- API Docs: `http://127.0.0.1:2024/docs`
- Studio: `https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024`

## テスト方法（手動）

1. Studio で `sample` グラフを選ぶ
2. `User Input` に質問を入力して `Submit`
3. ローカルLLMの応答が `result` に返ることを確認

## 注意

- Studio UI は `smith.langchain.com` 側で提供されるため、表示・操作には LangSmith ログインが必要です。
- 理由: Studio は画面自体を LangSmith がホストし、`baseUrl` で指定したローカル `langgraph dev` に実行を転送する構成だからです。
- 未ログイン時は LangSmith のサインアップ/ログイン画面へリダイレクトされます。
- ログインなしで確認したい場合は、`http://127.0.0.1:2024/docs` から API を直接実行してください。
- `.env` は機密情報を含む可能性があるため、Git 管理しません（`.gitignore` で除外）。

## GitHub公開

```bash
git remote add origin https://github.com/<YOUR_ID>/<REPO>.git
git branch -M main
git push -u origin main
```

## スリープ復帰後の接続チェックリスト

PCスリープ後は、SSHトンネルやVS Codeのポートフォワードが見た目だけ残り、実体は切断されることがあります。
復帰後は次の順で確認してください。

1. リモート側で `langgraph dev` が稼働しているか確認（必要なら再起動）
2. VS Code の Forwarded Ports を一度解除して再作成
3. `http://127.0.0.1:<local-port>/docs` が開くことを確認
4. `https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:<local-port>` でStudioを開き直す
5. ブラウザはハードリロード（`Ctrl+Shift+R`）を実施

補足: `bind ... permission denied` が出る場合は、ローカル側ポートが他プロセスに占有されています。別ポートを使うか、占有プロセスを解放してください。
