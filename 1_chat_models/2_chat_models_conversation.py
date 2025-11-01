from langchain_core.messages import SystemMessage,HumanMessage,AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

messages=[
    SystemMessage("You are a social media adviser"),
    HumanMessage("Give me 5 tips for using Instagram"),
    # AIMessage(),
    HumanMessage("Now give 5 tips for using facebook")
]

result=llm.invoke(messages)
print(result.content)