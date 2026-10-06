from pydantic import BaseModel
from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv
load_dotenv()

class Answer(BaseModel):
    summary: str
    confidence: float

@tool
def search(query: str) -> str:
    """Search for imformation"""
    return f"Results for: {query}"

agent = create_agent(
    model="openai:gpt-5.5",
    tools=[search],
    response_format=Answer,
    system_prompt="너는 학습 도우미야, 핵심과 간단구조만 알려줘",
)

result = agent.invoke({"messages": [{"role": "user", "content": "싱글 에이전트를 설명해줘"}]})
print(result["structured_response"])