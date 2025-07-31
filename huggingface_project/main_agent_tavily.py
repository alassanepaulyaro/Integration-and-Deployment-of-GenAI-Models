import os
from dotenv import load_dotenv

from langchain_openai import OpenAI  
from langchain_community.chat_models import ChatOpenAI
from langchain_experimental.plan_and_execute import (
    PlanAndExecute, load_agent_executor, load_chat_planner
)
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langchain.chains.llm_math.base import LLMMathChain   
from langchain.tools import Tool

# --- Load environment variables ---
load_dotenv()

# --- Model and Chains ---
llm = OpenAI(temperature=0, model="gpt-4.1-nano")
llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)
search = TavilySearchResults()  # Tavily web search tool
wikipedia = WikipediaAPIWrapper()  # Use directly, no QueryRun wrapper needed

# --- Tool Definitions ---
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

# --- Plan and Execute Agent Setup ---
model = ChatOpenAI(temperature=0)
planner = load_chat_planner(model)
executor = load_agent_executor(model, tools, verbose=True)
agent = PlanAndExecute(planner=planner, executor=executor, verbose=True)

# --- Example Prompt ---
prompt = (
    "Where are the next summer olympics going to be hosted? "
    "What is the population of that country raised to the 0.43 power?"
)

# --- Agent Execution ---
result = agent.run(prompt)
print(result)