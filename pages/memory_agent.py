import sys
import asyncio
import streamlit as st
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner
from dotenv import load_dotenv
from agents.mcp import MCPServerSse
import json
import os

load_dotenv()
# Windows 호환성
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# ✅ SSE URL 고정값 (하드코딩)
SSE_URL = os.getenv("MEMORY_MCP_URL")

# ✅ SSE 연결
def connect_sse():
    return MCPServerSse(params={"url": SSE_URL}, name="mcp.run")

# ✅ Agent 생성만 수행 (실행은 하지 않음)
async def setup_agent():
    mcp_server = connect_sse()
    await mcp_server.__aenter__() 

    agent = Agent(
        name="Assistant",
        instructions="너는 장기기억 에이전트야. 너는 사용자의 질문에 대해서 기억을 찾아서 답변이 필요한 경우 기업을 찾아보고, 기억을 저장할 필요가 있으면 기억을 저장해줘",
        model="gpt-4o",
        mcp_servers=[mcp_server],
    )
    return agent, [mcp_server]



# 메시지 처리
async def process_user_message():
    agent, mcp_servers = await setup_agent()
    messages = st.session_state.chat_history

    result = Runner.run_streamed(agent, input=messages)

    response_text = ""
    placeholder = st.empty()

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            response_text += event.data.delta or ""
            with placeholder.container():
                with st.chat_message("assistant"):
                    st.markdown(response_text)

        elif event.type == "run_item_stream_event":
            item = event.item

            if item.type == "tool_call_item":
                tool_name = getattr(item.raw_item, "name", "알 수 없음")
                raw_args = getattr(item.raw_item, "arguments", "{}")
                try:
                    args = json.loads(raw_args)
                    arg_str = ", ".join(f"{k}: {v}" for k, v in args.items())
                except Exception:
                    arg_str = raw_args  # 파싱 실패 시 원본 출력

                st.toast(f"🛠 도구 활용: `{tool_name}`\nArgs: {arg_str}", icon="🛠")

    # 최종 응답 저장
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": response_text
    })

    # MCP 서버 종료
    for server in mcp_servers:
        await server.__aexit__(None, None, None)

# Streamlit UI 메인
def main():
    st.set_page_config(page_title="장기기억 에이전트", page_icon="🎥")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.title("🎥 장기기억 에이전트")

    for m in st.session_state.chat_history:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    # 사용자 입력 처리
    user_input = st.chat_input("대화를 해주세요")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # 비동기 응답 처리
        asyncio.run(process_user_message())
        

if __name__ == "__main__":
    main()