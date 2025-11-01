from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

messages=[
    ("system","You are a fact expert and your job is to present facts about {topic}"),
    ("human","Tell me {facts_count} about it")
]

prompt_template=ChatPromptTemplate.from_messages(messages)

# prompt=prompt_template.invoke({"topic":"Lion","facts_count":3})
# result=llm.invoke(prompt)

chain=prompt_template | llm | StrOutputParser()

result=chain.invoke({"topic":"Lion","facts_count":3})

print(result)