from functools import reduce
import sys

TOTAL_ROWS = 128

def seat_coordinates_to_seat_id(row, column):
    return 8*row + column

def seat_id_to_coordinates(seat):
    row = seat // 8
    column = seat % 8
    return row, column

def interval_reducer_generator(first_half):
    """ Constructs an interval reducer using first_half as the character indicating that the
        result is in the first half of the previous interval
    """
    def interval_reducer(interval, coordinate):
        interval_start, interval_end = interval
        half_interval_width = (interval_end - interval_start) / 2
        if coordinate == first_half:
            return (interval_start, interval_start + half_interval_width)
        return (interval_start + half_interval_width, interval_end)
    return interval_reducer


def bsp_to_seat_coordinates(bsp):
    row_bsp = bsp[:7]
    column_bsp = bsp[7:]
    
    row = reduce(interval_reducer_generator("F"), row_bsp, (0, 128))[0]
    column = reduce(interval_reducer_generator("L"), column_bsp, (0, 8))[0]

    return row, column

def generate_seats_in_range(start, end):
    start_row, start_column = seat_id_to_coordinates(start)
    end_row, end_column = seat_id_to_coordinates(end)

    r, c = start_row, start_column
    current = start
    while current <= end:
        yield current
        c = (c + 1) % 8
        if c == 0:
            r = r + 1
        current = seat_coordinates_to_seat_id(r, c)

if __name__ == "__main__":
    filepath = sys.argv[1]

    with open(filepath, "r") as inf:
        seats = {seat_coordinates_to_seat_id(*bsp_to_seat_coordinates(line.strip())) for line in inf}

        min_seat = min(seats)
        max_seat = max(seats)

        print(f"Min seat: {min_seat}")
        print(f"Max seat: {max_seat}")

        seats_in_range = [x for x in generate_seats_in_range(min_seat, max_seat)]
        empty_seats = [x for x in seats_in_range if x not in seats]

        print(len(seats_in_range))

        print(empty_seats)

