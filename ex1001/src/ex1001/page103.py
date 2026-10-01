#노드 사이에 엣지 추가할 경우에는 라우팅 함수가 필요없음
#이 코드는 라우팅 함수를 사용하는 코드로 구현

from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END


# 1. State 정의
# 그래프가 들고 다니는 데이터
class State(TypedDict):
    messages: Annotated[list[str], add]


# 2. Graph 생성
graph = StateGraph(State)


# 3. chatbot Node에서 실행할 함수
def chatbot(state: State):
    question = state["messages"][-1]

    answer = f"사용자 입력을 그대로 반환하는 챗봇입니다. {question}라는 질문을 받았습니다."

    return {
        "messages": [answer]
    }


# 4. summary Node에서 실행할 함수
def summary(state: State):
    return {
        "messages": ["질문이 길어서 요약을 진행합니다."]
    }


# 5. Node 추가
graph.add_node("chatbot", chatbot)
graph.add_node("summary", summary)


# 6. START → chatbot
graph.add_edge(START, "chatbot")


# 7. Routing 함수
def routing_function(state: State):

    # 실제 State의 마지막 메시지를 가져옴
    message = state["messages"][-1]

    if len(message) > 1000:
        return True

    return False


# 8. 조건부 Edge
graph.add_conditional_edges(
    "chatbot",
    routing_function,
    {
        True: "summary",
        False: END
    }
)


# 9. summary → END
graph.add_edge("summary", END)


# 10. Graph Compile
app = graph.compile()


# 11. 실제 입력
result = app.invoke({
    "messages": ["안녕하세요"]
})


# 12. 결과 출력
print(result)