#from 같은 경로의 app파일
#import app파일 안에 있는 main()
from .app import main

__all__ =["main"]

# uv init은 프로젝트를 초기화 해줌 
print("프로젝트 초기화 init")