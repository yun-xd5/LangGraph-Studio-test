# LangGraph Studio Local Environment

## 1. Python virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install "langgraph-cli[inmem]"
```

## 2. Environment file

```bash
cp .env.example .env
```

## 3. Start LangGraph dev server

```bash
langgraph dev
```

Default local API endpoint is:

- `http://127.0.0.1:2024`

If Studio does not open automatically, open:

- `https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024`

## Included graph

- Graph id: `sample`
- Entry node: `transform_text`
- Input state key: `user_input`
- Output state key: `result`
