#create_agent 기반 에이전트 구축

#create_agent를 사용하여 에이전트 만들기
from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from tools import python_exec_tool, file_write_tool

tools = [python_exec_tool, file_write_tool]

llm = ChatOpenAI(model='gpt-4o')
graph = create_agent(
    model = llm, 
    tools = tools
)

#피보나치 수열 코드 작성 요청
if __name__ == "__main__":
    response = graph.stream(
        {
            "messages":[
                "첫번째 항이 1인 피보나치 수열을 출력하는 파이썬 코드를 작성해주세요. 정상적으로 실행되는 지 확인도 해주세요. ",
                "확인했다면 그 코드는 .py 파일로 저장하세요."
            ]
        }
    )

    for chunk in response:
        for node, value in chunk.items():
            if node:
                print("------", node, "------")
            if "messages" in value:
                print(value["messages"][0].content)
