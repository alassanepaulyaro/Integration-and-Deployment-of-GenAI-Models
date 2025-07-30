import os
import streamlit as st
from dotenv import load_dotenv
import json

from langchain_openai import OpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain_experimental.plan_and_execute import (
    PlanAndExecute, load_agent_executor, load_chat_planner
)
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langchain.chains.llm_math.base import LLMMathChain
from langchain.tools import Tool

# Load environment variables
load_dotenv()

# Streamlit page config
st.set_page_config(
    page_title="OpenAI Plan&Execute Agent Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent_temperature" not in st.session_state:
    st.session_state.agent_temperature = 0.0

if "agent_max_tokens" not in st.session_state:
    st.session_state.agent_max_tokens = 512

# --- Agent Factory ---
@st.cache_resource(show_spinner=False)
def get_agent(temperature=0.0, max_tokens=512):
    llm = OpenAI(model="gpt-4.1-nano", temperature=temperature, max_tokens=max_tokens)
    llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=False)
    search = TavilySearchResults()
    wikipedia = WikipediaAPIWrapper()
    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="useful for when you need to answer questions about current events"
        ),
        Tool(
            name="Wikipedia",
            func=wikipedia.run,
            description="useful for when you need to look up facts and statistics"
        ),
        Tool(
            name="Calculator",
            func=llm_math_chain.run,
            description="useful for when you need to answer questions about math"
        ),
    ]
    model = ChatOpenAI(model="gpt-4.1-nano", temperature=temperature, max_tokens=max_tokens)
    planner = load_chat_planner(model)
    executor = load_agent_executor(model, tools, verbose=False)
    agent = PlanAndExecute(planner=planner, executor=executor, verbose=False)
    return agent

if "agent" not in st.session_state:
    st.session_state.agent = get_agent(
        temperature=st.session_state.agent_temperature,
        max_tokens=st.session_state.agent_max_tokens
    )

# Sidebar: Model parameters & about
with st.sidebar:
    st.title("🤖 OpenAI Plan&Execute Agent")
    st.markdown("### Settings")
    max_tokens = st.slider("Max Tokens", min_value=64, max_value=2048, value=st.session_state.agent_max_tokens)
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=st.session_state.agent_temperature, step=0.05)
    st.markdown("### About")
    st.info(
        "This assistant leverages OpenAI GPT-4.1-nano, Tavily Search, Wikipedia, and Calculator tools via LangChain's Plan & Execute agent.\n"
        "Ideal for research, code, and math queries."
    )
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# If the settings changed, update agent
if (
    temperature != st.session_state.agent_temperature or 
    max_tokens != st.session_state.agent_max_tokens
):
    st.session_state.agent = get_agent(temperature=temperature, max_tokens=max_tokens)
    st.session_state.agent_temperature = temperature
    st.session_state.agent_max_tokens = max_tokens

# Display chat history
st.title("🤖 OpenAI Plan&Execute Agent")
st.markdown("Ask me anything! I can reason, search, calculate, and cite Wikipedia.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Auto-reply if needed (for example button/quick test) ---
if (
    st.session_state.messages and
    st.session_state.messages[-1]["role"] == "user" and
    (len(st.session_state.messages) == 1 or st.session_state.messages[-2]["role"] == "assistant")
):
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                agent = st.session_state.agent
                prompt = st.session_state.messages[-1]["content"]
                response = agent.run(prompt)
                # --- Clean up JSON action_input ---
                try:
                    resp_json = response.replace("'", '"')
                    parsed = json.loads(resp_json)
                    if isinstance(parsed, dict) and "action_input" in parsed:
                        response = parsed["action_input"]
                except Exception:
                    pass
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Chat input
if prompt := st.chat_input("Ask a question or give a research task..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                agent = st.session_state.agent
                response = agent.run(prompt)
                # --- Clean up JSON action_input ---
                try:
                    resp_json = response.replace("'", '"')
                    parsed = json.loads(resp_json)
                    if isinstance(parsed, dict) and "action_input" in parsed:
                        response = parsed["action_input"]
                except Exception:
                    pass
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Example prompts
if not st.session_state.messages:
    st.markdown("### 💡 Example Prompts")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🏟️ Next Olympics location and stats"):
            st.session_state.messages.append({"role": "user", "content":
                "Where are the next summer olympics going to be hosted? What is the population of that country raised to the 0.43 power?"
            })
            st.rerun()
    with col2:
        if st.button("🌍 Who won the 2020 Nobel Peace Prize?"):
            st.session_state.messages.append({"role": "user", "content":
                "Who won the 2020 Nobel Peace Prize and what did they do?"
            })
            st.rerun()
    with col3:
        if st.button("🧮 What is (2^30) - 1?"):
            st.session_state.messages.append({"role": "user", "content":
                "What is (2^30) - 1? Give the full calculation."
            })
            st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Powered by LangChain, OpenAI GPT-4.1-nano, and Tavily Search"
    "</div>", 
    unsafe_allow_html=True
)
