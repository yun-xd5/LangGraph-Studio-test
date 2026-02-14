import os
from functools import lru_cache
from typing import NotRequired, TypedDict

from langchain_ollama import ChatOllama
from langgraph.graph import END, START, StateGraph


class AppState(TypedDict):
    user_input: str
    result: NotRequired[str]


@lru_cache(maxsize=1)
def get_local_llm() -> ChatOllama:
    return ChatOllama(
        base_url=os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434"),
        model=os.getenv("OLLAMA_MODEL", "qwen2.5:7b"),
        temperature=0,
    )


def transform_text(state: AppState) -> AppState:
    text = state.get("user_input", "").strip()
    if not text:
        return {"result": "Input is empty."}

    try:
        response = get_local_llm().invoke(text)
        return {"result": str(response.content)}
    except Exception as e:
        return {"result": f"[local-llm error] {e}"}


builder = StateGraph(AppState)
builder.add_node("transform_text", transform_text)
builder.add_edge(START, "transform_text")
builder.add_edge("transform_text", END)

graph = builder.compile()
