import ast
import sys

class MinusOpTransformer(ast.NodeTransformer):
    def visit_BinOp(self, node):
        if isinstance(node.op, ast.Sub):
            node.op = ast.Mult()
        node.left = self.visit(node.left)
        node.right = self.visit(node.right)
        return node

class SwapMinusDivTransformer(ast.NodeTransformer):
    def visit_BinOp(self, node):
        if isinstance(node.op, ast.Sub):
            node.op = ast.Mult()
        elif isinstance(node.op, ast.Div):
            node.op = ast.Add()
        node.left = self.visit(node.left)
        node.right = self.visit(node.right)
        return node

if __name__ == "__main__":
    filename = sys.argv[1]

    with open(filename, "r") as inf:
        # Replace * with - because they have the same precedence
        original_lines = [l for l in inf]
        lines = [l.replace("*", "-") for l in original_lines]

    # Parse the AST for the line
    asts = [ast.parse(l, mode="eval") for l in lines]

    # Change minus nodes to mult nodes
    xform = MinusOpTransformer()
    xformed = [xform.visit(a) for a in asts]

    # Print results
    values = [eval(compile(program, "<string>", "eval")) for program in xformed]
    part_one = sum(values)
    print(f"Part One: {part_one}")

    # Two part swap
    lines2 = [l.replace("*", "-").replace("+", "/") for l in original_lines]
    asts2 = [ast.parse(l, mode="eval") for l in lines2]
    xform2 = SwapMinusDivTransformer()
    xformed2 = [xform2.visit(a) for a in asts2]
    values2 = [eval(compile(program, "<string>", "eval")) for program in xformed2]
    part_two = sum(values2)
    print(f"Part Two: {part_two}")
    