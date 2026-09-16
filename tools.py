import ast
import operator

ALLOWED_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}

def _safe_eval(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numeric constants allowed")
    elif isinstance(node, ast.BinOp):
        op_func = ALLOWED_OPS.get(type(node.op))
        if op_func is None:
            raise ValueError(f"Operator not allowed: {type(node.op).__name__}")
        return op_func(_safe_eval(node.left), _safe_eval(node.right))
    else:
        raise ValueError(f"Unsafe expression node: {type(node).__name__}")

def calculator(expression: str) -> float:
    tree = ast.parse(expression, mode="eval")
    return _safe_eval(tree.body)

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
