import sys

if __name__ == "__main__":
    filename = sys.argv[1]

    with open(filename) as inf:
        groups = inf.read().split("\n\n")
        responses_by_group = [set(g for g in group if g != '\n') for group in groups]

        print(f"Total: {sum(map(len, responses_by_group))}")