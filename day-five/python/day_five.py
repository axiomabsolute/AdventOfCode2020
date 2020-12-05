from functools import reduce
import sys

TOTAL_ROWS = 128

def seat_coordinates_to_seat_id(row, column):
    return 8*row + column

def seat_id_to_coordinates(seat_id):
    row = seat_id // 8
    column = seat_id % 8
    return row, column

def to_binary_int(zero, entry):
    return int(''.join("0" if e == zero else "1" for e in entry), 2)

def bsp_to_seat_coordinates(bsp):
    row_bsp = bsp[:7]
    column_bsp = bsp[7:]
    
    row = to_binary_int("F", row_bsp)
    column = to_binary_int("L", column_bsp)

    return row, column

def generate_seats_in_range(start, end):
    return [x for x in range(start, end + 1) if x % 8 <= 7]

if __name__ == "__main__":
    filepath = sys.argv[1]

    with open(filepath, "r") as inf:
        seats = {seat_coordinates_to_seat_id(*bsp_to_seat_coordinates(line.strip())) for line in inf}

        min_seat = min(seats)
        max_seat = max(seats)

        print(f"Max seat: {max_seat}")

        seats_in_range = set(generate_seats_in_range(min_seat, max_seat))
        empty_seats = seats_in_range - seats

        print(empty_seats)

