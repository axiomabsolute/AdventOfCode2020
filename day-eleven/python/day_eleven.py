from collections import Counter
from itertools import chain
import sys

def get_neighbors(n_row, n_col, row, col):
    return [
        (r, c)
        for r in range(max(row - 1, 0), min(row + 2, n_row))
        for c in range(max(col - 1, 0), min(col + 2, n_col))
        if not (r == row and c == col)
    ]

def get_adjacent_seats(layout, row, col):
    return [
        layout[r][c] for r,c in get_neighbors(len(layout), len(layout[0]), row, col)
    ]

def get_next_visible_seat(layout, row, col, rise, run):
    nrow = row + rise
    ncol = col + run
    upper_row = len(layout)
    upper_col = len(layout[row])
    while 0 <= nrow < upper_row and 0 <= ncol < upper_col:
        sight = layout[nrow][ncol]
        if sight  == "L" or sight == "#":
            return sight
        nrow += rise
        ncol += run
    return "."
    

def get_visible_seats(layout, row, col):
    return [
        get_next_visible_seat(layout, row, col, -1, 0), # down
        get_next_visible_seat(layout, row, col, 1, 0),   # up
        get_next_visible_seat(layout, row, col, 0, -1),  # left
        get_next_visible_seat(layout, row, col, 0, 1),   # right
        get_next_visible_seat(layout, row, col, -1, -1), # down-left
        get_next_visible_seat(layout, row, col, -1, 1),  # down-right
        get_next_visible_seat(layout, row, col, 1, -1),  # up-left
        get_next_visible_seat(layout, row, col, 1, 1),   # up-right
    ]

def find_seats(layout, get_adjacent_seats_fn = get_adjacent_seats, threshold = 4):
    new_layout = [[column for column in row] for row in layout]
    for row in range(len(layout)):
        for col in range(len(layout[row])):
            adjacent_seats = get_adjacent_seats_fn(layout, row, col)
            # If the seat is L and no adjacent seat is #, it becomes #
            if layout[row][col] == "L" and "#" not in adjacent_seats:
                new_layout[row][col] = "#"
            # If the seat is # and threshold or more adjacent seats are # then it becomes L
            elif layout[row][col] == "#" and Counter(adjacent_seats)["#"] >= threshold:
                new_layout[row][col] = "L"
    if new_layout == layout:
        return layout

    return find_seats(new_layout, get_adjacent_seats_fn, threshold)

if __name__ == "__main__":
    filename = sys.argv[1]

    with open(filename, "r") as inf:
        layout = [line.strip() for line in inf]

        seats = find_seats(layout)
        occupied = Counter(chain(*seats))["#"]
        print(f"Occupied: {occupied}")

        seats2 = find_seats(layout, get_visible_seats, 5)
        occupied2 = Counter(chain(*seats2))["#"]
        print(f"Occupied2: {occupied2}")
