from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

def main():
	st.set_page_config(layout="wide")
	st.title("AI 챗봇")
	if "messages" not in st.session_state:
		st.session_state.messages = []

	for message in st.session_state.messages:
		with st.chat_message(message["role"]):
			st.write(message["content"])

	client = OpenAI()
	user_input = st.chat_input("무엇이 궁금한가요?")
	if user_input:
		st.session_state.messages.append({"role": "user", "content": user_input})
		with st.chat_message("user"):
			st.write(user_input)
		with st.chat_message("assistant"):
			stream = client.chat.completions.create(
				model="gpt-4o-mini",
				messages=st.session_state.messages,
				stream=True,
			)
			response = st.write_stream(stream)
		st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
	main()