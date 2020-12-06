import sys

if __name__ == "__main__":
    filename = sys.argv[1]

    with open(filename) as inf:
        groups = inf.read().split("\n\n")
        responses_by_group = [g.split("\n") for g in groups]

        any_yes_by_group = [len(set.union(*map(set, rg))) for rg in responses_by_group]
        print(f"Each by Group: {sum(any_yes_by_group)}")

        all_yes_by_group = [
            len(set.intersection(*map(set, rg))) for rg in responses_by_group
        ]
        print(f"Every by Group: {sum(all_yes_by_group)}")