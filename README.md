


# 장기기억 AI Agent

## 작동방식


## 설치 방법

1. 필수 패키지 설치  
   ```bash
   uv add openai-agents openai streamlit python-dotenv 
   ```

2. 환경 변수 파일(.env)을 생성한 후, OpenAI API 키를 입력하기
 - https://mcp.supermemory.ai 에서 MCP URL 입력
   ```env
   OPENAI_API_KEY=여기에_발급받은_키_입력
   MEMORY_MCP_URL=내 URL 입력
   ```

## 실행

Streamlit 앱 실행  
   ```bash
   uv run streamlit run agent.py
   ```


