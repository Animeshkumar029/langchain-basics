from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

messages=[
    ("system","You are a helpful learning ai here to increase knowledge on {subject}"),
    ("human","What is the capital of {country}")
]

prompt_template=ChatPromptTemplate.from_messages(messages)
country=input("Give the country name whose capital you want to know:")
prompt=prompt_template.invoke({"subject":"General Knowledge", "country":country})

response=llm.invoke(prompt).content

print(response)