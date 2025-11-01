from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema.runnable import RunnableLambda,RunnableSequence
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate

load_dotenv()

llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

messages=[
    ("system","You are an animal expert tell me about {animal}"),
    ("human","Tell me {facts_count} facts about specified animal")
]

prompt_template=ChatPromptTemplate.from_messages(messages)
prompt=RunnableLambda(lambda x: prompt_template.invoke(x))
invoke_llm=RunnableLambda(lambda x: llm.invoke(x.to_messages()))
parse_output=RunnableLambda(lambda x: x.content)

chain=RunnableSequence(first=prompt,middle=[invoke_llm],last=parse_output)

response=chain.invoke({"animal":"cat","facts_count":3})

print(response)