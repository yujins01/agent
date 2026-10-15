### 2. 검색 도구 파일
"""
질문을 받아 관련 성이 높은 문서를 찾아주는 검색 인터페이스

1. 사용자가 질문 -> 같은 임베딩 모델로 벡터화
2. Chroma에 저장된 벡터들과 유사도 비교
"""

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.tools import create_retriever_tool
from dotenv import load_dotenv
load_dotenv()

#vector_retriever에서 만든 DB를 다시 연결해 검색에 활용
DB_PATH = "./rag_agent/chroma_db"

#이미 저장된 DB에 연결해 사용
vectorstore = Chroma(
    persist_directory=DB_PATH, #저장된 Chroma DB의 위치 지정
    embedding_function=OpenAIEmbeddings(model="text-embedding-3-small"),
    collection_name="korean_pdf" #연결할 컬렉션 지정
)

# 컬렉션에 저장된 레코드를 조회하는 기능
vectorstore.get()

# 질문과 유사한 문서를 검색
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# retriever를 agent가 사용할 수 있는 tool(도구)로 변환하는 코드
retriever_tool = create_retriever_tool(  # retriever를 agent용 tool로 만듬
    retriever, #질문과 관련된 문서 청크를 검색
    name = "pdf_search", #agent가 사용할 도구 이름
    #agent에게 이 도구 용도를 알려주는 설명
    description = "use this tool to search information from the Korean Spelling Rules PDF document",
)

if __name__ == "__main__":
    response = retriever_tool.invoke("부엌이 들어간 경우 어떻게 발음 하나요?")
    print(response)