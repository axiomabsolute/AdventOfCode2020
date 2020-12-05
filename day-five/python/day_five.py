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

if __name__ == "__main__":
    filepath = sys.argv[1]

    with open(filepath, "r") as inf:
        seats = [calculate_seat(*calculate_row_column(line.strip())) for line in inf]
        print(max(seats))
