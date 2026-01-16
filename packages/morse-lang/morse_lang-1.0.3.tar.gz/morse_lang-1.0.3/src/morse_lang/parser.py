def parse(program: str):
    ast = []

    for line in program.splitlines():
        tokens = line.split()
        if not tokens:
            continue

        if tokens[0] == "let":
            ast.append(("let", tokens[1], tokens[3]))

        elif tokens[0] == "print":
            ast.append(("print", tokens[1:]))

        else:
            raise SyntaxError(f"Unknown statement: {tokens[0]}")

    return ast