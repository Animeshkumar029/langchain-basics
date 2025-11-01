from langchain.agents import create_react_agent, AgentExecutor
from langchain_community.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain import hub
from dotenv import load_dotenv
import os, requests, json

load_dotenv()
CURRENCY_API_KEY = os.getenv("CURRENCY_API_KEY")

@tool
def fetch_conversion_rate(input_str: str) -> float:
    """Gets the conversion rate using the API. 
    Expects a JSON string like: {"base_currency": "INR", "target_currency": "USD"}.
    """
    try:
        data = json.loads(input_str)
        base_currency = data["base_currency"]
        target_currency = data["target_currency"]
    except (json.JSONDecodeError, KeyError) as e:
        raise ValueError(f"Invalid input for fetch_conversion_rate: {input_str}") from e

    url = f'https://v6.exchangerate-api.com/v6/{CURRENCY_API_KEY}/pair/{base_currency}/{target_currency}'
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"API call failed: {response.text}")
    return response.json()["conversion_rate"]

@tool
def convert(input_str: str) -> float:
    """Converts the mentioned amount using the conversion rate. 
    Expects a JSON string like: {"amount": 10, "conversion_rate": 0.012}.
    """
    try:
        data = json.loads(input_str)
        amount = data["amount"]
        conversion_rate = data["conversion_rate"]
    except (json.JSONDecodeError, KeyError) as e:
        raise ValueError(f"Invalid input for convert: {input_str}") from e

    return amount * conversion_rate

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
prompt = hub.pull("hwchase17/react")

agent = create_react_agent(
    llm=llm,
    tools=[fetch_conversion_rate, convert],
    prompt=prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=[fetch_conversion_rate, convert],
    verbose=True
)
response = agent_executor.invoke({
    "input": "What is the conversion factor between INR and USD, and based on that can you convert 10 usd to inr?"
})

print("\nFinal Response:\n", response)
