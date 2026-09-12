import json
import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

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

messages=[
    {"role": "user", "content": "what is the capital of france?"}
]

def calculator(expression:str)-> float:
    return eval(expression)

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=messages,
    tools=tools
)

while True:
    assistant_message = response.choices[0].message
    if assistant_message.tool_calls:
        messages.append(assistant_message) # record the model's own tool-call request

        tool_call = response.choices[0].message.tool_calls[0]
        args = json.loads(tool_call.function.arguments)
        expression = args["expression"]
        result = calculator(expression)

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(result)
        }) #record the tool's result,linked to that specific request

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages, #same list - now has all 3 entries
            tools=tools
        )
        print(response)
    else:
        print(response.choices[0].message.content)
        break
