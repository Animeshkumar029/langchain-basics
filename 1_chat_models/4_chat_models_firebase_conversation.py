from langchain_core.messages import SystemMessage,HumanMessage,AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_google_firestore import FirestoreChatMessageHistory
from google.cloud import firestore

load_dotenv()

PROJECT_ID="langchain-tut-b19ad"
SESSION_ID="new_session_langchain"
COLLECTION_NAME="chat_history"

client=firestore.Client(project=PROJECT_ID)

chat_history=FirestoreChatMessageHistory(
    session_id=SESSION_ID,
    collection=COLLECTION_NAME,
    client=client
)

llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

while True:
    query=input("You:")
    if query=="exit":
        break
    chat_history.add_user_message(query)
    response=llm.invoke(chat_history).content
    chat_history.add_ai_message(response)

    print("AI::",response)