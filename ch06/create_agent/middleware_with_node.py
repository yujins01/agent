#모델 호출 전 미들웨어와 프롬프트 선택 미들웨어 구현하기
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.agents import before_model, dynamic_prompt, AgentState, ModelRequst
from langgraph.runtime import Runtime

from tools import tools

#모델 정의
model = ChatOpenAI(model="gpt-40-mini")

#금지어 목록
BLOKED_WORDS = ["바보","멍청이","나쁜말"]

#=========1. 미들웨어 정의 (노드가 추가되는 방식)=======
@before_model
def content_filter_middleware(state: AgentState, runtime: Runtime):
    """
    금지어를 필터링하는 미드웨어
    - 그래프에 'content_filter_middleware' 노드가 추가됨
    - 금지어 감지 시 예외 발생으로 중단
    """

    #마지막 메시지 확인
    if state["messages"]:
        last_msg = state["messages"][-1]
        content = getattr(last_msg, 'content', str(last_msg))

        #금지어 검사
        for word in BLOKED_WORDS:
            if word in content:
                print(f"[before_model] 🚫 금지어 감지: '{word}'")
                raise ValueError(f"부적절한 표현이 감지되었습니다: '{word}'")

        print(f"[before_model] ✅ 입력 검증 통과")

    return None #정상 진행

# ===== 미들웨어 정의 2: @dynamic_prompt (동적 시스템 프롬프트) =====
@dynamic_prompt
def random_tone_prompt(request: ModelRequst) -> str:
    """
    랜덤하게 말투를 변경하는 미들웨어
    - 존댓말 또는 반말 프롬프트 랜덤 선택
    - @wrap_model_call 기반이므로 노드 추가 X
    """
    import random

    if random.choice([True, False]):
        print(f"[dynamic_prompt] 존댓말 모드")
        return "당신은 친절한 AI입니다. 항상 존댓말로 정중하게 답변하세요"
    else:
        print(f"[dynamic_prompt] 반말 모드")
        return "너는 친근한 AI야. 항상 반말로 편하게 답변해"


#에이전트 생성
agent = create_agent(
    model=model,
    tools=tools,
    middleware=[
        content_filter_middleware,
        random_tone_prompt,
    ]
)

if __name__ == "__main__":
    from pathlib import Path

    save_path = Path(__file__).parent / "middleware_with_node.png"
    graph_image = agent.get_graph().draw_mermaid_png()

    with open(save_path, "wb") as f:
        f.write(graph_image)

    #테스트 1: 정상입력
    print("=" * 50)
    response = agent.stream({"messages": ["15와 7을 더해주세요."]})
    for chunk in response:
        for node, value in chunk.items():
            if node:
                print