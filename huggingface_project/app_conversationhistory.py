# Streamlit Chatbot with Persistent Chat History (LangChain + OpenAI GPT-4.1-nano)
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
from langchain_core.messages import messages_to_dict, messages_from_dict
import json
import os

load_dotenv()

st.set_page_config(page_title="GPT-4.1-nano Chatbot", layout="wide")
st.title("🤖 GPT-4.1-nano Chatbot (OpenAI + LangChain conversationelchain)")

# File-based storage example 
HISTORY_FILE = "chat_history.json"

def save_history(history):
    """Save chat history to a JSON file."""
    dicts = messages_to_dict(history.messages)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(dicts, f, ensure_ascii=False, indent=2)

def load_history():
    """Load chat history from a JSON file, if it exists."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            dicts = json.load(f)
        messages = messages_from_dict(dicts)
        return ChatMessageHistory(messages=messages)
    else:
        return ChatMessageHistory()

# Init chat history & memory
if "chat_history" not in st.session_state:
    # Load history from file, or create new
    st.session_state.chat_history = load_history()

if "conversation" not in st.session_state:
    llm = ChatOpenAI(
        model="gpt-4.1-nano",
        temperature=0
    )
    buffer = ConversationBufferMemory(chat_memory=st.session_state.chat_history)
    st.session_state.conversation = ConversationChain(
        llm=llm,
        memory=buffer,
        verbose=True
    )

# UI Input
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("You:", "")
    submit = st.form_submit_button("Send")
    if submit and user_input.strip():
        ai_response = st.session_state.conversation.predict(input=user_input)
        # History is already updated in ConversationBufferMemory via LangChain!
        # (No need to manually add to history list)
        save_history(st.session_state.chat_history)  # Save to file after each turn

# Display the conversation from memory
st.markdown("### Conversation")
for msg in st.session_state.chat_history.messages:
    if msg.type == "human":
        st.markdown(f"**🧑 You:** {msg.content}")
    elif msg.type == "ai":
        st.markdown(f"**🤖 AI:** {msg.content}")

# Reset conversation
if st.button("Reset conversation"):
    st.session_state.chat_history = ChatMessageHistory()
    st.session_state.conversation.memory.chat_memory = st.session_state.chat_history
    save_history(st.session_state.chat_history)  # Overwrite file with empty history
    st.experimental_rerun()

st.caption("Chat history is automatically saved and reloaded from 'chat_history.json'. You can implement multi-user or database persistence using the same approach.")
