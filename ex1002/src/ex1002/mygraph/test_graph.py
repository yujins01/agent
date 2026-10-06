# StateGraph 얘가 있어야 그래프를 그릴 수 있음
from langgraph.graph import StateGraph, MessagesState, START, END

def mock_llm(state: MessagesState):
    return {"messages": [{"role": "ai", "content": "hello world"}]}

graph = StateGraph(MessagesState)
#그래프를 만들고 nock_llm 노드를 추가함
graph.add_node(mock_llm)
#엣지는 노드를 연결하는 선으로 방향을 갖고 있음
graph.add_edge(START, "mock_llm")
graph.add_edge("mock_llm", END)
#다 했으면 컴파일 해야함
graph = graph.compile() #출력은 compile 뒤에 해야함

graph.invoke({"messages": [{"role": "user", "content": "hi!"}]})

#실행
#사용자가 hi 매새지를 날림 -> 또 다른 ai가 hello world 답을 날림
result = graph.invoke({"messages": [{"role": "user", "content": "hi!"}]})

#결과
print(result)
print(f"AIMessage: {result["messages"][-1].content}")

#머메이드로 그림
print(graph.get_graph().draw_mermaid())