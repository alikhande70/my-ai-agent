from langchain_core.tools import tool
import math


@tool
def calculator(expression: str) -> str:
    """Evaluate mathematical expressions safely."""
    try:
        allowed_names = {"math": math}
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"