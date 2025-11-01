from langchain_core.messages import SystemMessage,HumanMessage,AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

chat_history=[]

system_message=SystemMessage(content="Your role here is of a chat assistant to answer all the queries")
chat_history.append(system_message)

while True:
    query=input("you:")
    if query=="exit":
        break
    chat_history.append(HumanMessage(content=query))
    result=llm.invoke(chat_history)
    response=result.content

    chat_history.append(AIMessage(content=response))

    print("AI::", response)

print("<--------------Chat History------------------------->")
print(chat_history)