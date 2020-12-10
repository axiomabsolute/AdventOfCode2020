from collections import Counter
import functools
import sys

@functools.lru_cache
def valid_combinations(entry, entries_set, final):
    if entry == final:
        return 1
    if entry not in entries_set:
        return 0
    return valid_combinations(entry + 1, entries_set, final) + valid_combinations(entry + 2, entries_set, final) + valid_combinations(entry + 3, entries_set, final)

if __name__ == "__main__":
    filename = sys.argv[1]

    with open(filename, "r") as inf:
        entries = [int(l.strip()) for l in inf]
        sorted_entries = sorted(entries)
        # Outlet
        sorted_entries.insert(0, 0)
        # Device
        sorted_entries.append(sorted_entries[-1] + 3)

    differences = []
    for i in range(len(sorted_entries) - 1):
        differences.append(sorted_entries[i+1] - sorted_entries[i])
    counter = Counter(differences)

    print(counter[3] * counter[1])

    print(f"Valid combinations: {valid_combinations(0, frozenset(sorted_entries), sorted_entries[-1])}")