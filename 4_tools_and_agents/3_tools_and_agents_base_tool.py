from langchain_community.tools import BaseTool
from pydantic import BaseModel
from pydantic import Field
from typing import Type

class AdditionInput(BaseModel):
    a: int=Field(...,description="First Argument")
    b: int=Field(...,description="Second Argument")

class AdditionTool(BaseTool):
    name: str="addition"
    description: str="Adds two numbers"
    args_schema: Type[BaseModel]=AdditionInput

    def _run(self, a: int,b: int)-> int:
        return a+b

addition_tool=AdditionTool()
result=addition_tool.invoke({"a":4,"b":5})
print(result)