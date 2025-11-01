from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool

# built_in_tools
ddgsr=DuckDuckGoSearchRun()
result1=ddgsr.invoke("Who won the ipl 2025?")
print(result1)

# custom_tools
@tool
def addition(a: int,b: int)->int:
    """This tool is made to get the summation of two numbers"""
    return a+b

add=addition.invoke({"a":5,"b":6})
print(add)


print(addition.name)
print(addition.description)
print(addition.batch)
print(addition.args)



