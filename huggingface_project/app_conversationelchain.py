# OpenAI and LangChain Conversationelchain
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

st.set_page_config(page_title="GPT-4.1-nano Chatbot", layout="wide")

st.title("🤖 GPT-4.1-nano Chatbot (OpenAI + LangChain and Conversationelchain)")

if "conversation" not in st.session_state:
    llm = ChatOpenAI(
        model="gpt-4.1-nano",
        temperature=0
    )
    st.session_state.conversation = ConversationChain(
        llm=llm,
        memory=ConversationBufferMemory(),
        verbose=True
    )
if "history" not in st.session_state:
    st.session_state.history = []

# UI Input
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("You:", "")
    submit = st.form_submit_button("Send")
    if submit and user_input.strip():
        ai_response = st.session_state.conversation.predict(input=user_input)
        st.session_state.history.append({"role": "user", "text": user_input})
        st.session_state.history.append({"role": "ai", "text": ai_response})

st.markdown("### Conversation")
for msg in st.session_state.history:
    if msg["role"] == "user":
        st.markdown(f"**🧑 You:** {msg['text']}")
    else:
        st.markdown(f"**🤖 AI:** {msg['text']}")

if st.button("Reset conversation"):
    st.session_state.history = []
    st.session_state.conversation.memory.clear()
    st.experimental_rerun()
