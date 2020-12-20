import re
import sys

RULE_REPLACEMENTS = [
    "8: 42 | 42 8",
    "11: 42 31 | 42 11 31",
]


def parse_input(lines):
    section_two = False
    rules = {}
    messages = []
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            section_two = True
            continue
        if not section_two:
            rule_number, subrules_string = line.split(": ")
            subrules = [subrule.split(" ") for subrule in subrules_string.split(" | ")]
            rules[rule_number] = subrules
        else:
            messages.append(line)
    return rules, messages


def pattern_to_regex(literal_patterns, variable_pattern):
    return "".join(literal_patterns[c] for c in variable_pattern)


def subpatterns_to_regex(literal_patterns, subpatterns):
    compiled_subpatterns = []
    for subpattern in subpatterns:
        compiled = pattern_to_regex(literal_patterns, subpattern)
        compiled_subpatterns.append(compiled)
    full_pattern = f"({'|'.join(c for c in compiled_subpatterns)})"
    return full_pattern


def patterns_to_regex(literal_patterns, variable_patterns):
    new_literal_patterns = {}
    for pattern_name, subpatterns in variable_patterns.items():
        full_pattern = subpatterns_to_regex(literal_patterns, subpatterns)
        new_literal_patterns[pattern_name] = full_pattern
    return new_literal_patterns


def find_satisfied_patterns(literal_patterns, rules):
    return {
        k: v
        for k, v in rules.items()
        if all(t in literal_patterns for s in v for t in s)
    }


def find_unsatisfied_patterns(literal_patterns, rules):
    return {k: v for k, v in rules.items() if k not in literal_patterns}


def compile_variable_patterns(literal_patterns, rules):
    if not len(rules):
        return literal_patterns, None
    satisfied_patterns = find_satisfied_patterns(literal_patterns, rules)
    if len(satisfied_patterns) == 0:
        return literal_patterns, rules
    new_literal_patterns = patterns_to_regex(literal_patterns, satisfied_patterns)
    unsatisfied_patterns = find_unsatisfied_patterns(new_literal_patterns, rules)
    return compile_variable_patterns(
        {**literal_patterns, **new_literal_patterns}, unsatisfied_patterns
    )


def compile_patterns(rules):
    literal_patterns = {
        k: v[0][0][1]
        for k, v in rules.items()
        if len(v) == 1 and v[0][0].startswith('"')
    }
    other_rules = {k: v for k, v in rules.items() if k not in literal_patterns}
    return compile_variable_patterns(literal_patterns, other_rules)


if __name__ == "__main__":
    filename = sys.argv[1]

    with open(filename, "r") as inf:
        rules, messages = parse_input(inf)

    compiled_patterns, _ = compile_patterns(rules)
    print(
        f"Matching Rule 0: {sum(1 for message in messages if re.fullmatch(compiled_patterns['0'], message))}"
    )
