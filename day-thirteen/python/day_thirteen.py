import sys

def parse_input(lines):
    earliest_departure_time = int(next(lines).strip())
    bus_ids = [int(x) if x != "x" else x for x in next(lines).strip().split(",")]
    return (earliest_departure_time, bus_ids)

def find_next_departure_after(departures, after):
    result = {}
    for d in departures:
        number_of_loops = (after // d) + 1
        at_time = number_of_loops * d
        result[d] = {
            "number_of_loops": number_of_loops,
            "at_time": at_time
        }
    return result

def part_one_answer(bus_id, first_departure_after, after):
    to_wait = first_departure_after["at_time"] - after
    return bus_id * to_wait

def find_biggest_bus_id(indexed_bus_ids):
    return max(indexed_bus_ids, key=lambda x: x[1])

def reframe(indexed_bus_ids, biggest_bus_id):
    """Find the largest of the bunch and adjust indexes"""
    return [(idx - biggest_bus_id[0], bus_id) for idx, bus_id in indexed_bus_ids]

def the_unstoppable_arrow_of_time(start, step):
    while True:
        yield start
        start += step

def bus_filter(times, unit, offset):
    return filter(lambda t: (t % unit) == (unit - offset), times)

if __name__ == "__main__":
    filename = sys.argv[1]

    with open(filename, "r") as inf:
        earliest_departure_time, bus_ids_raw = parse_input(inf)

    bus_ids = [x for x in bus_ids_raw if x != "x"]
    next_departures = find_next_departure_after(bus_ids, earliest_departure_time)

    first_departure_after = sorted(next_departures.items(), key = lambda p: p[1]["at_time"])[0]

    print(part_one_answer(first_departure_after[0], first_departure_after[1], earliest_departure_time))

    indexed_bus_ids = [ (idx, bus_id) for idx, bus_id in enumerate(bus_ids_raw) if bus_id != "x"]
    biggest_bus_id = find_biggest_bus_id(indexed_bus_ids)
    reframed = reframe(indexed_bus_ids, biggest_bus_id)

    times = the_unstoppable_arrow_of_time(0, indexed_bus_ids[0][1])
    for offset, bus_id in indexed_bus_ids[1:]:
        times = bus_filter(times, bus_id, offset)
    print(next(times))
