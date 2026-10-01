#그래프의 실행 단위, 노드 추가하기
#메세지 입력을 받으면 어떻게 처리 할지 정의하는 단계의 코드

#노드 사이에 엣지추가한 함수

from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END

# 1. State 정의
#State = 그래프가 들고 다니는 데이터
#그래프 안에서 작업들이 공유할 데이터의 형태를 정의
class State(TypedDict):
    #각 노드가 messages를 반환하면 기존 messages에 이어 붙임
    messages: Annotated[list[str], add] 

# 2. Graph 생성
#그래프 만듬, 아직 아무것도 없음
graph = StateGraph(State)

# 3. Node에서 실행할 함수 정의
#노드로 사용할 함수
def chatbot(state: State):
    question = state["messages"][-1]

    print("chatbot 실행")

    return {
        "messages": [f"질문을 받았습니다: {question}"]
    }


def simple_answer(state: State):
    print("simple_answer 실행")

    return {
        "messages": ["간단한 질문이므로 바로 답변합니다."]
    }


def summary(state: State):
    print("summary 실행")

    return {
        "messages": ["긴 질문이므로 내용을 요약해서 답변합니다."]
    }

# 4. Node 추가
graph.add_node("chatbot", chatbot)
graph.add_node("simple_answer", simple_answer)
graph.add_node("summary", summary)


# 5. 기본 Edge 연결
#node_a -> node_b로 향하는 엣지
# START → node_a
# graph.add_edge(START, "node_a")

# # node_a → node_b
# graph.add_edge("node_a", "node_b")

# # node_b → END
# graph.add_edge("node_b", END)

# 5. 시작점 → chatbot
graph.add_edge(START, "chatbot")

# 6. 조건 판단 함수
def routing_function(state: State):

    question = state["messages"][0]

    if len(question) > 10:
        return "summary"
    else:
        return "simple_answer"


# 7. 조건부 Edge
graph.add_conditional_edges(
    "chatbot",
    routing_function,
    {
        "simple_answer": "simple_answer",
        "summary": "summary"
    }
)

# 8. 각각의 노드 → END
graph.add_edge("simple_answer", END)
graph.add_edge("summary", END)


# 9. 그래프 컴파일
app = graph.compile()


# 10. 실행
result = app.invoke({
    "messages": ["LangGraph를 사용해서 RAG 시스템을 구축하는 방법을 알려주세요."]
})


print(result)
