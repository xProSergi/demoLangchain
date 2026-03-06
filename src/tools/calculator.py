def calculate(expression: str) -> str:
 
    allowed_chars = set("0123456789+-*/()., ")
    if any(ch not in allowed_chars for ch in expression):
        raise ValueError("Expression contains unsupported characters")

    expr = expression.replace(",", ".")

    try:
        result = eval(expr, {"__builtins__": {}}, {})
    except Exception as exc:
        raise ValueError(f"Invalid expression: {exc}") from exc

    return str(result)

