from langchain.agents import create_react_agent, AgentExecutor
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain import hub
from dotenv import load_dotenv
import requests
import os

load_dotenv()

WEATHER_API_KEY=os.getenv("WEATHER_API_KEY")

llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

tool_for_searching=DuckDuckGoSearchRun()
@tool
def weather_tool(city:str)->str:
    """Function for finding the weather data of specified city"""
    url=f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}"
    response=requests.get(url)
    return response.json()

prompt=hub.pull("hwchase17/react")

agent=create_react_agent(
    llm=llm,
    tools=[tool_for_searching,weather_tool],
    prompt=prompt
)

execution_agent=AgentExecutor(
    agent=agent,
    tools=[tool_for_searching,weather_tool],
    verbose=True
)

response=execution_agent.invoke({"input":"What is the capital of spain , also find the weather details of that city?"})
print(response)
