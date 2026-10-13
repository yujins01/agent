#RAG를 위한 상태 정의

from langgraph.graph import MessagesState

class AgentState(MessagesState):
    question: str
    content: str
    answer: str
    retry_num: int