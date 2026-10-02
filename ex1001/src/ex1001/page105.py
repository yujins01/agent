#랭그래프로 에이전트 설계하고 구현하기
from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI

#그래프의 입력 스키마와 출력 스키마 정의하기
class InputState(TypedDict):
    question: str

class OutputState(TypedDict):
    answer: str

class OverallState(TypedDict):
    messages: Annotated[list[str],add]
    question: str
    answer: str

#그래프 객체 생성하기
graph_builder = StateGraph(
    OverallState,
    input_schema=InputState,
    output_schema=OutputState
)

#llm 답변을 생성하는 노드 추가
llm = ChatOpenAI(
    temperature=0,
    model_name= "gpt-4o-mini"
)

def chatbot(state: InputState) -> OverallState:
    question = state["question"]
    response = llm.invoke(question)
    return {
        "answer":response.content,
        "messages": [question, response.content]
    }
graph_builder.add_node("chatbot", chatbot)

#챗봇 노드에 엣지를 연결하고 그래프 컴파일
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()

#그래프 시각화
from IPython.display import Image, display

try:
    display(Image(graph.get_graph().draw_mermaid_png()))
except Exception:
    pass

#그래프 실행하기
graph.invoke({"question": "대한민국의 수도는 어디인가요?"})