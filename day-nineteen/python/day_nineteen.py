import re
import sys

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
            subrules = [
                subrule.split(" ")
                for subrule in
                subrules_string.split(" | ")
            ]
            rules[rule_number] = subrules
        else:
            messages.append(line)
    return rules, messages

def _compile_patterns(literal_patterns, rules):
    if not len(rules):
        return literal_patterns
    satisfied_patterns = {k:v for k,v in rules.items() if all(t in literal_patterns for s in v for t in s)}
    new_literal_patterns = {}
    for pattern_name, subpatterns in satisfied_patterns.items():
        compiled_subpatterns = []
        for subpattern in subpatterns:
            compiled = ''.join(literal_patterns[c] for c in subpattern)
            compiled_subpatterns.append(compiled)
        full_pattern = f"({'|'.join(c for c in compiled_subpatterns)})"
        new_literal_patterns[pattern_name] = full_pattern
    unsatisfied_patterns = {k:v for k,v in rules.items() if k not in new_literal_patterns}
    return _compile_patterns({**literal_patterns, **new_literal_patterns}, unsatisfied_patterns)

def compile_patterns(rules):
    literal_patterns = {k:v[0][0][1] for k,v in rules.items() if len(v) == 1 and v[0][0].startswith("\"")}
    other_rules = {k:v for k,v in rules.items() if k not in literal_patterns}
    return _compile_patterns(literal_patterns, other_rules)

if __name__ == "__main__":
    filename = sys.argv[1]

    with open(filename, "r") as inf:
        rules, messages = parse_input(inf)

    compiled_patterns = compile_patterns(rules)
    print(f"Matching Rule 0: {sum(1 for message in messages if re.fullmatch(compiled_patterns['0'], message))}")
