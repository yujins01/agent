from langchain.tools import tool
from langchain_openai import ChatOpenAI

@tool
def add(a: int, b: int) -> int:
    """Adds a and b.
    
    Args:
        a: first int
        b: second int
    """
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """Mutliply a and b.
    
    Arg:
        a: first int
        b: second int
    """

    return a * b

tools = [add, multiply]

llm = ChatOpenAI(
    model_name="gpt-4o-mini"
)
llm_with_tools = llm.bind_tools(tools)

# query = "3 곱하기 5는 뭔가요? 그리고 2더하기 4는?"

# response = llm_with_tools.invoke(query)
# print(response)
# print(response.tool_calls)

query = "안녕하세요"

response = llm_with_tools.invoke(query)
print(response)