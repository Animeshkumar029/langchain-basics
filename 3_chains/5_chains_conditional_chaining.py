from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema.output_parser import StrOutputParser
from langchain_core.runnables import RunnableBranch
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

intialization_prompt=ChatPromptTemplate.from_messages([
    ("system","You are a feedback catcher."),
    ("human","Classify the given feedback as positive, negative, neutral or escalate feedback : {feedback}")
])

positive_feedback_prompt=ChatPromptTemplate.from_messages([
    ("system","You are a helpful assistant"),
    ("human","Generate a thanking note considering this provided feedback:{feedback}")
])

negative_feedback_prompt=ChatPromptTemplate.from_messages([
    ("system","You are a helpful assistant"),
    ("human","Generate a sincere response considering this negative feedback : {feedback}")
])

neutral_feedback_prompt=ChatPromptTemplate.from_messages([
    ("system","You are a helful assistant"),
    ("human","Generate a message requesting for more information considering the provided feedback : {feedback}")
])

escalate_feedback_prompt=ChatPromptTemplate.from_messages([
    ("system","You are a helpful assistant"),
    ("human","Generate a message to escalate this feedback to a human agent: {feedback}.")
])

branches=RunnableBranch(
    (
        lambda x: "positive" in x,
        positive_feedback_prompt | llm | StrOutputParser()
    ),
    (
        lambda x: "negative" in x,
        negative_feedback_prompt | llm | StrOutputParser()
    ),
    (
        lambda x:"neutral" in x,
        neutral_feedback_prompt | llm | StrOutputParser()
    ),
    escalate_feedback_prompt | llm | StrOutputParser()  # the fallback logic
)

chain=(intialization_prompt | llm | StrOutputParser() | branches )

feedback="The movie was pretty bad and the character development was very poor throughout the movie, specially of the protaganist."

result=chain.invoke({"feedback":feedback})

print(result)