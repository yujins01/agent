#그래프 상태에서 리듀서 함수 추가 -> 상태의 업데이트 방식을 지정

#기존 메세지에 추가 메세지를 병합하기 위해 리듀서 함수 'add'사용

from typing import TypedDict, Annotated
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph.message import add_messages

def add(left, right):
    return left + right

class State(TypedDict):
    messages: Annotated[list[Annotated], add]

msgs1 = [HumanMessage(content="Hello", id="1")]
msgs2 = [AIMessage(content="Hi there!", id="2")]

result = add_messages(msgs1, msgs2)
print(result)