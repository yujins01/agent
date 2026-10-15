#3. RAG를 위한 상태 정의

"""
3. agent가 사용할 데이터 항목과 데이터 구조를 정의

공용 데이터 보관함의 설계도

retry_num: 반복횟수를 세어, 일정 횟수를 초과하면 문서 재탐색을 포기하도록 구현하기 위해
관련성 평가에 통과하지 못해 문서를 반복적으로 다시 검색하는 무한 루트에 갇히는 것을 방지
"""

from langgraph.graph import MessagesState

class AgentState(MessagesState):
    question: str    #사용자 질문
    content: str     #검색된 문서 내용
    answer: str      #생성된 답변
    retry_num: int   #재시도 횟수