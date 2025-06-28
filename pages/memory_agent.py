import sys
import asyncio
import streamlit as st
import os
from mem0 import AsyncMemoryClient
from agents import Agent, Runner, function_tool
from dotenv import load_dotenv
from openai.types.responses import ResponseTextDeltaEvent, ResponseOutputItemDoneEvent, ResponseFunctionToolCall
import json
load_dotenv()
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

client = AsyncMemoryClient(api_key=os.getenv("MEM0_API_KEY"))

user_id = "dabid"

# --- Tool 정의 ---
@function_tool
async def add_to_memory(content: str) -> str:
    """Add a message to Mem0"""
    messages = [{"role": "user", "content": content}]
    await client.add(messages, user_id=user_id,output_format="v1.1")
    return f"Stored message: {content}"

@function_tool
async def search_memory(query: str) -> str:
    """Search for memories in Mem0"""
    memories = await client.search(query, user_id=user_id, output_format="v1.1")
    results = '\n'.join([result["memory"] for result in memories["results"]])
    return str(results)


agent = Agent(
    name="Memory Assistant",
    instructions="""
    You are a helpful assistant with memory capabilities. You can:
    1. Store new information using add_to_memory
    2. Search existing information using search_memory
    When users ask questions:
    - If they want to store information, use add_to_memory
    - If they're searching for specific information, use search_memory
    - even if the user did not explicitly ask for retrieval, if the user's question is related to personal information, use search_memory
    """,
    model="gpt-4.1-mini",
    tools=[add_to_memory, search_memory],
)


    
async def process_user_message():
    messages = st.session_state.longterm_messages
    result = Runner.run_streamed(agent, input=messages)
    response_text = ""
    placeholder = st.empty()

    async for event in result.stream_events():
        if event.type == "raw_response_event":
            if isinstance(event.data, ResponseTextDeltaEvent):
                response_text += event.data.delta or ""
                with placeholder.container():
                    with st.chat_message("assistant"):
                        st.markdown(response_text)

            # 도구사용 결과를 toast로 반환
            if (
                event.type == "raw_response_event"
                and isinstance(event.data, ResponseOutputItemDoneEvent)
                and isinstance(event.data.item, ResponseFunctionToolCall)
            ):
                print(event.data)
                tool_name = getattr(event.data.item, "name", "알 수 없음")
                raw_args = getattr(event.data.item, "arguments", "{}")
                try:
                    args = json.loads(raw_args)
                    arg_str = ", ".join(f"{k}: {v}" for k, v in args.items())
                except Exception:
                    arg_str = raw_args
                st.toast(f"🛠 도구 활용: `{tool_name}`\nArgs: {arg_str}", icon="🛠")

    # 대화 내역에 오직 assistant 응답만 저장
    st.session_state.longterm_messages.append({
        "role": "assistant",
        "content": response_text
    })

def main():
    st.title("장기기억 Agent")
    if "longterm_messages" not in st.session_state:
        st.session_state.longterm_messages = []

    # 기존 메시지 출력
    for message in st.session_state.longterm_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 입력 처리
    user_input = st.chat_input("메시지를 입력하세요")
    if user_input:
        st.session_state.longterm_messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        asyncio.run(process_user_message())

if __name__ == "__main__":
    main()
