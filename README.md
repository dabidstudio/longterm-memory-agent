


# 장기기억 AI Agent

## 메모리 작동방식
<img src="https://github.com/user-attachments/assets/7d0e3927-bf20-44fc-a9c9-0fb2c89c0ff2" width="500">


## 설치 방법

1. 필수 패키지 설치  
   ```bash
   uv add openai-agents openai streamlit python-dotenv 
   ```

2. 환경 변수 파일(.env)을 생성한 후, mem0와 OpenAI API 키를 입력하기
   ```env
   OPENAI_API_KEY=여기에_발급받은_키_입력
   MEM0_API_KEY=여기에_발급받은_키_입력
   ```

## 실행

   ```bash
   uv run streamlit run agent.py
   ```


