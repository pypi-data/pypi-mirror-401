variables = {}

def eval_expr(expr):
    if len(expr) == 1:
        token = expr[0]
        if token.isdigit():
            return int(token)
        return variables[token]

    left, op, right = expr
    if op == "+":
        return eval_expr([left]) + eval_expr([right])
    if op == "-":
        return eval_expr([left]) - eval_expr([right])
    if op == "*":
        return eval_expr([left]) * eval_expr([right])
    if op == "/":
        return eval_expr([left]) // eval_expr([right])

    raise RuntimeError("Invalid expression")

def run(ast):
    for node in ast:
        if node[0] == "let":
            _, name, value = node
            variables[name] = int(value)

        elif node[0] == "print":
            print(eval_expr(node[1]))