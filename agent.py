from typing import NotRequired, TypedDict

from langgraph.graph import END, START, StateGraph


class AppState(TypedDict):
    user_input: str
    result: NotRequired[str]


def transform_text(state: AppState) -> AppState:
    text = state.get("user_input", "")
    return {"result": f"Processed: {text}"}


builder = StateGraph(AppState)
builder.add_node("transform_text", transform_text)
builder.add_edge(START, "transform_text")
builder.add_edge("transform_text", END)

graph = builder.compile()
