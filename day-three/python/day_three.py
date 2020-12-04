import sys

SLOPES_TO_CHECK = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2)
]

def load_input_file(filepath):
    with open(filepath, "r") as inf:
        return [line.strip() for line in inf]

def count_trees_on_slope(scene, right = 3, down = 1):
    count = 0
    x_coord = 0
    y_coord = 0
    width = len(scene[0])
    while y_coord < len(scene):
        if scene[y_coord][x_coord] == "#":
            count += 1
        x_coord = (x_coord + right) % width
        y_coord += down
    return count

if __name__ == "__main__":
    filepath = sys.argv[1]

    scene = load_input_file(filepath)
    tree_count = count_trees_on_slope(scene)

    print(tree_count)

    tree_counts = [count_trees_on_slope(scene, *slope) for slope in SLOPES_TO_CHECK]
    product = 1
    for tc in tree_counts:
        product *= tc
    print(product)