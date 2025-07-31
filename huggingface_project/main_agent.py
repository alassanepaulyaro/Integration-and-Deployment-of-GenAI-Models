# OpenAi Agent with Wikipedia
import os
os.environ["LANGCHAIN_TRACING_V2"] = "false"
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain import hub

load_dotenv()

llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0)

# Better tools - Wikipedia instead of human input
tools = [WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())]

prompt = hub.pull("hwchase17/react")
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True,
    handle_parsing_errors=True
)

#prompt = "Who was the first president of the United States?"
prompt = "When was the 3rd president of the united states born? What is that year raised to the power of 3?"

# Simple factual question
result = agent_executor.invoke({"input": prompt })
print(result["output"])