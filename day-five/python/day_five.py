from functools import reduce
import sys

TOTAL_ROWS = 128

def calculate_seat(row, column):
    return 8*row + column

def interval_reducer_generator(first_half):
    def interval_reducer(interval, coordinate):
        interval_start, interval_end = interval
        half_interval_width = (interval_end - interval_start) / 2
        if coordinate == first_half:
            return (interval_start, interval_start + half_interval_width)
        return (interval_start + half_interval_width, interval_end)
    return interval_reducer


def calculate_row_column(bsp):
    row_bsp = bsp[:7]
    column_bsp = bsp[7:]
    
    row = reduce(interval_reducer_generator("F"), row_bsp, (0, 128))[0]
    column = reduce(interval_reducer_generator("L"), column_bsp, (0, 8))[0]

    return row, column

def deconstruct_seat(seat):
    row = seat // 8
    column = seat % 8
    return row, column

def generate_seats_in_range(start, end):
    start_row, start_column = deconstruct_seat(start)
    end_row, end_column = deconstruct_seat(end)

    r, c = start_row, start_column
    current = start
    while current <= end:
        yield current
        c = (c + 1) % 8
        if c == 0:
            r = r + 1
        current = calculate_seat(r, c)

if __name__ == "__main__":
    filepath = sys.argv[1]

    with open(filepath, "r") as inf:
        seats = {calculate_seat(*calculate_row_column(line.strip())) for line in inf}

        min_seat = min(seats)
        max_seat = max(seats)

        print(f"Min seat: {min_seat}")
        print(f"Max seat: {max_seat}")

        seats_in_range = [x for x in generate_seats_in_range(min_seat, max_seat)]
        empty_seats = [x for x in seats_in_range if x not in seats]

        print(len(seats_in_range))

        print(empty_seats)

