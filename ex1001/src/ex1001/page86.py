from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

def page86_ai_msg():

    #load_dotenv()
    #llm = ChatOpenAI(model_name="gpt-4o-mini")

    message = [
        (
            "system",
            "당신은 사용자가 한 말을 영어로 변역"
        ),
        ("human", "안녕하세요"),
    ]
    
    #ai_msg = llm.invoke(message)

    ai_msg = "더미데이터"

    print(ai_msg + "여기는 Page86.py")

    return ai_msg