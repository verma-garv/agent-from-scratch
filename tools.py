tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Evaluates a basic math expression and returns the numeric result.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "A math expression to evaluate, e.g. '4 + 5 * 2'"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

def calculator(expression:str)-> float:
    return eval(expression)
