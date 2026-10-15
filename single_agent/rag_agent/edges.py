## edge는 다음에 어떤 노드를 실행할지 경정하거나, 노드 사이의 연결의 정의

##### (4) 관련성 평가 엣지 구현

from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-4o")

#평가 기준과 출력 형식 정의
#pydantic으로 llm 평가 결과의 구조를 정의
class Grade(BaseModel):
    """관련성 확인을 위한 점수 스키마"""

    binary_score: str = Field(description="문서가 질문과 관련이 있는지 여부, 'yes' 또는 'no'")


def decide_to_generate(state):
    """
    답변을 생성할지, 아니면 질문을 다시 생성할지 결정합니다.
    """

    print("----- ASSESS GRADED DOCUMENTS -----")
    if state.get("retry_num", 0) >= 3: #재시도 횟수가 3회 이상이면 generate로 보냄
        return "generate"

    # 구주화된 출력을 사용하는 평가 모델 생성
    #LLM의 결과를 Grade 스키마에 맞는 구조로 받도록 설정
    grader = llm.with_structured_output(Grade) 

    # 평가 프름프트 구성
    grader_prompt = ChatPromptTemplate.from_messages( # [ 3 ]
        [
            (
                "system",
                """
                당신은 검색된 문서가 사용자 질문과 관련이 있는지 평가하는 평가자입니다.
                문서가 사용자 질문과 관련된 키워드나 의미를 포함하고 있다면 관련성이 있다고 평가하세요.
                엄격한 테스트일 필요는 없습니다. 목표는 잘못된 검색 결과를 필터링하는 것입니다.
                문서가 질문과 관련이 있는지를 나타내는 'yes' 또는 'no'의 이진 점수를 제공하세요.
                """
            ),
            (
                "user",
                "검색된 문서: {context} \n\n 사용자 질문: {question} \n\n 관련성 점수:"
            ),
        ]
    )

    chain = grader_prompt | grader

    # 현재 상태에서 질문과 문서 가져오기
    question = state.get("question", "")
    context = state.get("context", "")

    if not context or not question:
        print("---ERROR: Missing context or question, defaulting to generate---")
        return "generate"

    #LLM이 질문과 문서의 관련성을 평가하고, 그 결과를 grade에 저장
    score = chain.invoke(
        {
            "question": question,
            "context": context
        }
    )
    grade = score.binary_score

    #평가 결과에 따라 다음 노드 결정
    if grade == "no":
        print(
            "---DECISION: RETRIEVED DOCUMENT ARE NOT RELEVANT TO QUESTION, TRANSFORM QUERY---"
        )
        return "transform_query" #검색 결과가 질문과 관련이 없으므로 질문을 다시 구성하는 노드로 이동
    else:
        print("---DECISION: GENERATE---")
        return "generate" #검색 결과가 관련 있으므로 답변 생성 노드로 이동


###### (7) 답변 환각 여부 평가 엣지 구
#답변의 환각 여부를 평가하는 라우팅 함수 만들기
class GradeHallucinations(BaseModel):
    """
    생성된 답변의 환각 여부를 판단하기 위한 점수 스키마
    """
    binary_score: str = Field(
        description="답변이 사실에 근거하고 있는지 여부, 'yes' or 'no'"
    )

def check_haalucinations(state):
    """
    생성된 답변이 문서에 근거하고 질문에 답하는지 판단합니다.
    """

    print("-----CHECK HALLUCINATION-----")
    question = state["question"]
    context = state["context"]
    answer = state["answer"]

    structured_llm = llm.with_structured_output(GradeHallucinations)

    system = """당신은 LLM이 생성한 답변이 검색된 사실들에 근거하고 있는지 평가하는 평가자입니다.
    'yes' 또는 'no'의 이진 점수를 제공하세요. 'yes'는 답변이 사실들에 근거하고 있음을 의미합니다."""

    hallucination_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("user", "질문: {question}\n\n 사실 집합: \n\n LLM 생성 답변: {generattion}"),

        ]
    )

    hallucination_grader = hallucination_prompt|structured_llm

    score = hallucination_grader.invoke(
        {"question":question, "context": context, "gernation": answer}
    )
    grade = score.binary_score
    if grade == "yes":
        print("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---")
        return "support"
    else:
        print("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, RE-TRY---")
        return "not supported"