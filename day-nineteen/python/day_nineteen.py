from itertools import product
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


def pattern_to_literal(literal_patterns, variable_pattern):
    alternates = []
    for c in variable_pattern:
        subpattern = literal_patterns[c]
        if not isinstance(subpattern, list):
            alternates.append([subpattern])
        else:
            alternates.append(subpattern)
    return [''.join(p) for p in list(product(*alternates))]


def subpatterns_to_regex(literal_patterns, subpatterns):
    compiled_subpatterns = []
    for subpattern in subpatterns:
        compiled = pattern_to_regex(literal_patterns, subpattern)
        compiled_subpatterns.append(compiled)
    full_pattern = f"({'|'.join(c for c in compiled_subpatterns)})"
    return full_pattern


def subpatterns_to_literals(literal_patterns, subpatterns):
    compiled_subpatterns = []
    for subpattern in subpatterns:
        compiled = pattern_to_literal(literal_patterns, subpattern)
        compiled_subpatterns.extend(compiled)
    return compiled_subpatterns


def patterns_to_target(literal_patterns, variable_patterns, target):
    new_literal_patterns = {}
    for pattern_name, subpatterns in variable_patterns.items():
        full_pattern = target(literal_patterns, subpatterns)
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


def compile_variable_patterns(literal_patterns, rules, compilation_target):
    if not len(rules):
        return literal_patterns, None
    satisfied_patterns = find_satisfied_patterns(literal_patterns, rules)
    if len(satisfied_patterns) == 0:
        return literal_patterns, rules
    new_literal_patterns = patterns_to_target(literal_patterns, satisfied_patterns, compilation_target)
    unsatisfied_patterns = find_unsatisfied_patterns(new_literal_patterns, rules)
    return compile_variable_patterns(
        {**literal_patterns, **new_literal_patterns}, unsatisfied_patterns, compilation_target
    )


def compile_patterns(rules, compilation_target=subpatterns_to_regex):
    literal_patterns = {
        k: v[0][0][1]
        for k, v in rules.items()
        if len(v) == 1 and v[0][0].startswith('"')
    }
    other_rules = {k: v for k, v in rules.items() if k not in literal_patterns}
    return compile_variable_patterns(literal_patterns, other_rules, compilation_target)


def count_suffix(patterns, message, count = 0):
    ends_with_any = any(message.endswith(p) for p in patterns)
    if not ends_with_any:
        return count, message
    return count_suffix(patterns, message[:-1 * len(patterns[0])], count + 1)


def count_prefix(patterns, message, count = 0):
    starts_with_any = any(message.startswith(p) for p in patterns)
    if not starts_with_any:
        return count, message
    return count_prefix(patterns, message[len(patterns[0]):], count + 1)


if __name__ == "__main__":
    filename = sys.argv[1]

    with open(filename, "r") as inf:
        rules, messages = parse_input(inf)

    compiled_patterns, _ = compile_patterns(rules)
    print(
        f"Matching Rule 0: {sum(1 for message in messages if re.fullmatch(compiled_patterns['0'], message))}"
    )

    rule_updates, _ = parse_input(RULE_REPLACEMENTS)
    updated_rules = {**rules, **rule_updates}
    updated_compiled_patterns = compile_patterns(updated_rules, subpatterns_to_literals)[0]

    prefix_counts_and_messages = [count_prefix(updated_compiled_patterns["42"], m) for m in messages]
    prefix_counts = [p[0] for p in prefix_counts_and_messages]
    suffix_counts_and_messages = [count_suffix(updated_compiled_patterns["31"], m) for _,m in prefix_counts_and_messages]
    suffix_counts = [s[0] for s in suffix_counts_and_messages]
    residuals = [s[1] for s in suffix_counts_and_messages]
    print(sum(
        1 for p,s,r in zip(prefix_counts, suffix_counts, residuals)
        if p != 0 and s != 0 and len(r) == 0 and p > s
    ))
    