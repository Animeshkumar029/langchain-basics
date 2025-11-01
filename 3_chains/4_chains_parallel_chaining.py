from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema.runnable import RunnableLambda,RunnableParallel
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

initial_message_template=ChatPromptTemplate.from_messages([
    ("system","You are a movie critic and your task is to provide asked information about the mentioned movie."),
    ("human","Tell me about {movie}")
])

def plot_analyzer(plot):
    template_for_plot=ChatPromptTemplate.from_messages([
        ("system","You are a movie critic, analyze the plot."),
        ("human","here is the plot:{plot}. What are its strengths and weaknesses?")
    ])
    return template_for_plot.format_prompt(plot=plot)

def characters_analyzer(characters):
    template_for_characters=ChatPromptTemplate.from_messages([
        ("system","You are a movie critic"),
        ("human","Analyze the characters : {characters}. Mention the strength and weaknesses of each")
    ])
    return template_for_characters.format_prompt(characters=characters)

def combine_verdicts(plot_analysis,character_analysis):
    return f"Plot Analysis:\n{plot_analysis}\n\nCharacter Analysis:\n{character_analysis}"

plot_chain=(RunnableLambda(lambda x:plot_analyzer(x)) | llm | StrOutputParser())

character_chain=(RunnableLambda(lambda x:characters_analyzer(x)) | llm | StrOutputParser())

chain=(
    initial_message_template
    | llm
    | StrOutputParser()
    |RunnableParallel(branches={"plot":plot_chain,"characters":character_chain})
    |RunnableLambda(lambda x: combine_verdicts(x["branches"]["plot"],x["branches"]["characters"]))
)

result=chain.invoke({"movie":"Godfather"})

print(result)