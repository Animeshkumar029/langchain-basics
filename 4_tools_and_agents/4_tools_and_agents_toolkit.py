from langchain_core.tools import tool

@tool(description="Adds two numbers")
def addition_tool(a:int,b:int)->int: return a+b

@tool(description="Subtracts two numbers")
def subtraction_tool(a:int,b:int)->int: return a-b

class MathToolkit:
    def get_tools(self):
        return [addition_tool,subtraction_tool]
    
    def add(self,a:int,b:int)->int: return addition_tool.invoke({"a":a,"b":b})
    
toolkit=MathToolkit()

result=toolkit.add(5,6)
print(result)
