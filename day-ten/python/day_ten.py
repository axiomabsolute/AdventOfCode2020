from collections import Counter
import sys

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