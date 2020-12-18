import ast
import sys

MULT_NODE = ast.parse("1 * 1", mode="eval").body
MINUS_NODE = ast.parse("1 - 1", mode="eval").body
ADD_NODE = ast.parse("1 + 1", mode="eval").body

class MinusOpTransformer(ast.NodeTransformer):
    def visit_BinOp(self, node):
        if node.op == MINUS_NODE.op:
            node.op = MULT_NODE.op
        node.left = self.visit(node.left)
        node.right = self.visit(node.right)
        return node

class SwapAddMultTransformer(ast.NodeTransformer):
    pass

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
    