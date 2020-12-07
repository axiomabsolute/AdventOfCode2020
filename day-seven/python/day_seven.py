from collections import defaultdict
from itertools import chain
import re
import sys

CHILD_PATTERN = r"(?P<val>\d+) (?P<kind>.*?) bag"

def build_rules(lines):
    rules = {}

    for line in lines:
        parent, children_string = line.split(" bags contain ")
        child_matches = re.findall(CHILD_PATTERN, children_string)
        children = {v:int(k) for k,v in child_matches}
        rules[parent] = children

    return rules

def invert(rules):
    index = defaultdict(lambda : list())

    for parent, children in rules.items():
        for child in children:
            index[child].append(parent)

    return index

def collect_ancestors(index, root):
    return chain(index[root], *[collect_ancestors(index, a) for a in index[root]])

def count_children(rules, root):
    """Basically the same as count_self_and_children, but don't count the root bag itself."""
    direct_descendents = rules[root]
    return sum(v*count_self_and_children(rules, k) for k,v in direct_descendents.items())

def count_self_and_children(rules, root):
    if root not in rules:
        return 0
    return 1 + sum([ count * count_self_and_children(rules, bag) for bag, count in rules[root].items()])

if __name__ == "__main__":
    filename = sys.argv[1]
    TARGET_BAG = "shiny gold"

    with open(filename, "r") as inf:
        rules = build_rules(inf)
        index = invert(rules)
        ancestors = set(collect_ancestors(index, TARGET_BAG))
        print(f"{len(ancestors)} bags may eventually contain a '{TARGET_BAG}' bag.")

        child_bag_count = count_children(rules, TARGET_BAG)
        print(f"A {TARGET_BAG} contains {child_bag_count} children.")