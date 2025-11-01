from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain.schema.output_parser import StrOutputParser

load_dotenv()
llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

messages=[
    ("system","You are a fact expert here for presenting facts on {animal}"),
    ("human","Provide me {facts_count} on the animal mentioned")
]

prompt_template=ChatPromptTemplate.from_messages(messages)

messages1=[
    ("system","You are a translator, your job is translate the provided text into {language}"),
    ("human","Translate the following text into {language}: {text}")
]

prompt_template1=ChatPromptTemplate.from_messages(messages1)

prepare_to_translate=RunnableLambda(lambda x:{"text":x,"language":"spanish"})

chain=prompt_template | llm | StrOutputParser() | prepare_to_translate | prompt_template1 | llm | StrOutputParser()

result=chain.invoke({"animal":"cheetah","facts_count":3})

print(result)
