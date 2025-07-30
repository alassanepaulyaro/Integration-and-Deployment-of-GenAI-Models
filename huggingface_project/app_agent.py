# OpenAI + Wikipedia Agent
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain import hub

# Disable LangChain tracing/logging
os.environ["LANGCHAIN_TRACING_V2"] = "false"

# Load .env for OPENAI_API_KEY
load_dotenv()

# --- Streamlit Page Config ---
st.set_page_config(
    page_title="OpenAI Wikipedia Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Sidebar ---
with st.sidebar:
    st.title("🤖 OpenAI + Wikipedia Agent")
    st.markdown("### Settings")
    st.info(
        "This app uses an OpenAI LLM agent with access to Wikipedia for factual and reasoning questions."
    )
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent_executor" not in st.session_state:
    st.session_state.agent_executor = None

# --- Agent Loading and Caching ---
@st.cache_resource(show_spinner="Loading AI agent (first run may take up to 1 minute)...")
def load_agent():
    # Choose your model ("gpt-4.1-nano", "gpt-4", etc.)
    llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0)
    tools = [WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())]
    prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True,
        handle_parsing_errors=True
    )
    return agent_executor

try:
    if st.session_state.agent_executor is None:
        agent_executor = load_agent()
        st.session_state.agent_executor = agent_executor
    else:
        agent_executor = st.session_state.agent_executor
except Exception as e:
    st.error(f"Error loading agent: {e}")
    st.stop()

# --- Main Content ---
st.title("🤖 OpenAI + Wikipedia Agent")
st.markdown("Ask me anything! I can search Wikipedia and reason step by step.")

# Render chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input and agent call
if user_input := st.chat_input("Ask a factual or reasoning question..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking and searching Wikipedia..."):
            try:
                # Run the agent
                result = agent_executor.invoke({"input": user_input})
                response = result["output"]
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {e}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Example questions if chat is empty
if not st.session_state.messages:
    st.markdown("### 💡 Example Questions")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Who was the first president of the United States?"):
            st.session_state.messages.append({"role": "user", "content": "Who was the first president of the United States?"})
            st.rerun()
    with col2:
        if st.button("When was the 3rd president of the US born?"):
            st.session_state.messages.append({"role": "user", "content": "When was the 3rd president of the United States born? What is that year raised to the power of 3?"})
            st.rerun()
    with col3:
        if st.button("What is the capital of Australia?"):
            st.session_state.messages.append({"role": "user", "content": "What is the capital of Australia?"})
            st.rerun()

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Powered by OpenAI, LangChain, and Wikipedia"
    "</div>",
    unsafe_allow_html=True
)
