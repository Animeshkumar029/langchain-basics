from langchain_core.messages import HumanMessage,AIMessage,SystemMessage
from langchain_core.tools import tool
from dotenv import load_dotenv
import requests
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import InjectedToolArg
from typing import Annotated
import json
import os

load_dotenv()
CURRENCY_API_KEY=os.getenv("CURRENCY_API_KEY")

@tool
def fetch_conversion_rate(base_currency:str,target_currency:str)->float:
    """to fetch the conversion rate of mentioned currency with respect to USD"""
    url=f'https://v6.exchangerate-api.com/v6/{CURRENCY_API_KEY}/pair/{base_currency}/{target_currency}'
    response=requests.get(url)
    return response.json()


@tool
def convert(amount:float,conversion_rate: Annotated[float, InjectedToolArg])->float:
    """this function multiply the stated amount using with the conversion_rate fetched"""
    return amount*conversion_rate

llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

llm_with_tools=llm.bind_tools([fetch_conversion_rate,convert])

messages=[
    SystemMessage(content="you are a currency converter app you task is to use the binded tools and fetch and convert the stated amount into stated target currency"),
    HumanMessage(content="What is the conversion factor between INR and USD, and based on that can you convert 10 inr to usd")
]

ai_message=llm_with_tools.invoke(messages)
messages.append(ai_message)

for tool_call in ai_message.tool_calls:
    if tool_call['name']=="fetch_conversion_rate":
        tool_message1=fetch_conversion_rate.invoke(tool_call)
        conversion_rate=json.loads(tool_message1.content)['conversion_rate']
        messages.append(tool_message1)

    if tool_call['name']=="convert":
        tool_call['args']['converstion_rate']=conversion_rate
        tool_message2=convert.invoke(tool_call)
        messages.append(tool_message2)

print(llm_with_tools.invoke(messages).content)

