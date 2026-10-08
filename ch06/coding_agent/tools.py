##### 코드를 실행하는 도구 생성

from pydantic import Field
from langchain.tools import tool

#python_exec_tool라는 도구 제작
@tool
def python_exec_tool(
    imports: str = Field(description="임포트 구문"),
    code: str = Field(description="임포트 구문을 제외한 코드 블록"),
) -> str:
    # 독스트링
    """
    파이썬 코드를 실행하는 도구입니다.
    만약 코드 실행에 실패하면 에러 메시지를 반환합니다.
    실핼결과를 확인하고 싶으면 'priint(...)'를 사용하여 출력해야합니다.
    
    Args:
        imports:임포트 구문
        code:임포트 구문을 제외한 코드 블록

    Returns:
        실행결과 또는 에러 메시지
    """

    #check imports
    #먼저 import구문이 작성된 코드를 실행하여 모듈을 실행할 준비가 되어있는지 확인
    #코드 실행은 exec()로 동작
    try:
        exec(imports)
    except Exception as e:
        return f"모듈을 임포트하는 데 실패했습니다. ERROR: {repr(e)}"

    #check execution
    #import 구문이 정상적이면 그외 코드를 합쳐 정상적으로 실행하는지 확인
    try:
        exec(imports +"\n" +code)
    except Exception as e:
        return f"코드 실행에 실패했습니다. ERROR: {repr(e)}"

    result_str = f"성공적으로 코드가 실행되었습니다. :\n'''python\n{code}\n'''"

    return result_str

##### 파일을 저장하는 도구 생성
@tool
def file_write_tool(
    file_path: str = Field(description="생성/수정할 파일의 경로"),
    content: str = Field(description="파일에 작성할 내용")
) -> str:
    """
    파일을 생성하거나 내용을 작성하는 도구입니다.
    
    Args:
        file_path: 생성/수정할 파일의 경로
        content: 파일에 작성할 내용
    
    Returns:
        성공/실패 메시지
    """

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"파일 '{file_path}'에 성공적으로 작성했습니다."
    except Exception as e:
        return f"파일 작성 실패: {repr(e)}"


# if __name__ == "__main__":
#     result = python_exec_tool.invoke({
#         "imports": "import math",
#         "code": "print(math.sqrt(16))"
#     })

#     print(result)