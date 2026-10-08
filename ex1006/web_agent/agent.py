import os
from langchain_tavily import TavilySearch
from langchain_openai import ChatOpenAI

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START ,END
from langgraph.graph.message import add_messages

from dotenv import load_dotenv
load_dotenv()

#타빌리 서피 도구를 사용하는 LLM 설정
tool = TavilySearch(max_results=3)
tools = [tool]

llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools) #llm에게 tool 사용 가능하다고 알려줌

#메시지 목록을 관리하는 그래프 상태 정의
class State(TypedDict):
    messages: Annotated[list, add_messages]

#상태 그래프 만들기
graph_builder = StateGraph(State)

#노드 생성하기 (LLM의 답변을 생성하는 노드)
def chatbot(state: State):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

graph_builder.add_node("chatbot", chatbot)

#도구 노드 생성하기 (LLM이 호출한 도구를 실행하는 노드 만들기)
import json
from langchain.messages import ToolMessage

#llm이 tool을 사용해! 요청하면 실제 tool을 찾아서 실행
class BasicToolNode:
    """
    마지막 AIMessage에서 요청 된 도구를 실행하는 노드
    """
    #사용할 tool들을 받아서 이름별로 저장
    def __init__(self, tools: list) -> None:
        #tool의 이름을 key로 해서 tool 객체를 저장
        self.tools_by_name = {
            tool.name: tool 
            for tool in tools
        }
    #LangGraph에서 이 노드가 실행될 때 호출되는 함수
    def __call__(self, inputs: dict):
        #State에서 messages를 가져옴
        if messages := inputs.get("messages",[]):
            message = messages[-1]
        else: #메세지가 없으면 오류 발생
            raise ValueError("ERROR:입력에 메시지가 없습니다.")

        #tool 실행 결과를 저장할 리스트
        outputs = []

        #LLM이 호출하라고 요청한 tool들을 하나씩 실행** 핵심
        for tool_call in message.tool_calls:
            #tool 이름으로 실제 tool을 찾아서 실행
            tool_result = self.tools_by_name[
                tool_call["name"]
                ].invoke(
                tool_call["args"] #llm이 전달한 입력값
            )
            #tool 실행 결과를 toolmessage로 변환
            outputs.append(
                ToolMessage(
                    content=json.dumps(tool_result, ensure_ascii=False),
                    name=tool_call["name"], #어떤 tool을 실행했는지
                    tool_call_id=tool_call["id"], #호출한 tool의 ID
                )
            )
        return {"messages": outputs}

#tool node 생성
tool_node = BasicToolNode(tools=[tool])
#langgraph에 tools라는 이름의 노드 추가
graph_builder.add_node("tools",tool_node)


#LLM의 도구호출 결과에 따라 처리하는 조건부 엣지 만들기
def route_tools(
        state: State,
):
    """
    마지막 메시지에 도구호출이 있는 경우, ToolNode로 라우팅하고 그렇지 않으면 END로 라우팅
    """
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages",[]):
        ai_message = messages[-1]
    else:
        raise ValueError(f"ERROR: 입력에 메시지가 없습니다. 상태 {state}")

    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return END

graph_builder.add_conditional_edges(
    "chatbot",
    route_tools,
    {"tools": "tools", END: END},
)


#엣지 연결하고 그래프 컴파일하기
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")
graph = graph_builder.compile()



#그래프를 시각화 하여 저장하고 실행
# def run_agent():
#     # 1. LangGraph 구조를 PNG 이미지로 생성
#     try:
#         image = graph.get_graph().draw_mermaid_png()

#         with open("web_agent/graph.png", "wb") as f:
#             f.write(image)

#         print("그래프 이미지 생성 완료")

#     except Exception as e:
#         print(f"그래프 이미지 생성 실패: {e}")

#     # 2. Agent 실행
#     response = graph.invoke(
#         {
#             "messages": ["LangGraph가 무엇인가요?"]
#         }
#     )

#     print(response)

#####최신정보 검색하고 답변 받아보기

#1. invoke 사용
#그래프를 시각화하여 저장하고 실행
if __name__ == "__main__":

    try:
        image = graph.get_graph().draw_mermaid_png()

        with open("web_agent/graph.png", "wb") as f:
            f.write(image)

        print("그래프 이미지 생성 완료")

    except Exception as e:
        print(f"그래프 이미지 생성 실패: {e}")

    response = graph.invoke(
        {
            "messages": ["Langgraph가 무엇인가요?"]
        }
    )

    #print(response)

#pretty_print() 사용해 메시지 목록 출력
def invoke():
    response = graph.invoke(
        {
            "messages":["Langgraph가 무엇인가요?"]
        }
    )
    for msg in response["messages"]:
        msg.pretty_print()

if __name__ == "__main__":
    invoke()


#2. ainvoke 사용
async def ainvoke():
    response = await graph.ainvoke(
        {
            "messages":["Langgraph가 무엇인가요?"]
        }
    )

    for msg in response["messages"]:
        msg.pretty_print()

if __name__ == "__main__":
    import asyncio
    asyncio.run(ainvoke())

#3. stream: udates 모드 사용하기
#각 노드의 상태 업데이트만 출력되는 방식
def stream():
    response = graph.stream(
        {
            "messages":["Langgraph가 무엇인가요?"]
        }
    )
    for chunk in response:
        for node, state in chunk.items():
            print("---", node, "---")
            print(state)
            print("="*60)

if __name__ == "__main__":
    stream()


#4. stream: values 모드 사용하기
#노드의 이름은 출력되지않고 상태 정보만 출력
#그래프의 메시지 목록이 어떻게 쌓여가는지 파악 가능
def stream_values():
    response = graph.stream(
        {
            "messages":["Langgraph가 무엇인가요?"]
        },
        stream_mode="values"
    )

    for chunk in response:
        for state_key, state_value in chunk.items():
            print("---현재상태---")
            for msg in state_value:
                print(f"{type(msg).__name__}: {msg.content[:50]}")
            if state_key == "messages":
                state_value[-1].pretty_print()
            print("="*60)

if __name__ == "__name__":
    stream_values()

#5. stream: messages 모드 사용
#토큰 단위로 순차적으로 실시간으로 생성되는 즉시 화면에 전달

def stream_messages():
    response = graph.stream(
        {
            "messages":["Langgraph가 무엇인가요?"]
        },
        stream_mode="values"
    )

    for token, metadata in response:
        print(token.content)
        #print(metadata["langgraph_node"])


if __name__ == "__main__":
    stream_messages()


#6.astream()을 활용해 실행 결과 확인
async def astream():
    response = graph.astream(
        {
            "messages":["Langgraph가 무엇인가요?"]
        }
    )
    async for chunk in response:
        for node, state in chunk.items():
            print('---',node,'---')
            print(state)
            print("="*60)

if __name__ == "__main__":
    import asyncio
    asyncio.run(astream())


####langgrapgh dev할때 set PYTHONUTF8=1먼저 실행 후 동작
####LangGraph API가 파일을 읽을 때 CP949 대신 UTF-8 방식으로 처리하도록 유도