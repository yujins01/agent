from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# 1. State 정의
class State(TypedDict):
    message: str

# 2. 노드 함수 정의
def greeting_node(state: State) -> dict:
    original = state.get("message", "")
    return {"message": f"Hello! Processed message: '{original}'"}

# 3. Graph 구성 및 컴파일
builder = StateGraph(State)
builder.add_node("greeting", greeting_node)
builder.add_edge(START, "greeting")
builder.add_edge("greeting", END)

# langgraph dev가 인지할 그래프 변수 Export
graph = builder.compile()

# 실행: uv run langgraph dev
