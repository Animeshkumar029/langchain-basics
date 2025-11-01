from langchain.tools import StructuredTool
from pydantic import BaseModel
from pydantic import Field

class AdditionInputs(BaseModel):
    a: int=Field(...,description="First argument to be passed")
    b: int=Field(...,description="Second argument to be passed")

def addition_function(a:int,b:int)->int:
    return a+b

addition_tool=StructuredTool.from_function(
    func=addition_function,
    name="addition",
    description="Adds two number",
    args_schema=AdditionInputs
)

result=addition_tool.invoke({"a":5,"b":6})
print(result)
