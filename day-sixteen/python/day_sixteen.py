from itertools import chain, product
import sys

def parse_field(field_line):
    field_name, constraint_section = field_line.split(": ")
    raw_constraints = constraint_section.split(" or ")
    constraints = tuple(
        tuple(int(r) for r in c.split("-")) for c in raw_constraints
    )
    return field_name, constraints

def parse_fields(fields_section):
    return dict( 
        parse_field(field_line)
        for field_line in 
        fields_section.split("\n")
  )

def parse_ticket(ticket_line):
    return tuple( 
        int(x) for x in ticket_line.strip().split(",")
  )

def parse_my_ticket(my_ticket_section):
    return parse_ticket(my_ticket_section.split("\n")[1])

def parse_nearby_tickets(nearby_tickets_section):
    return tuple( parse_ticket(l) for l in nearby_tickets_section.split("\n")[1:] )

def parse(text):
    fields_section, my_ticket_section, nearby_tickets_section = text.split("\n\n")
    fields = parse_fields(fields_section)
    my_ticket = parse_my_ticket(my_ticket_section)
    nearby_tickets = parse_nearby_tickets(nearby_tickets_section)
    return fields, my_ticket, nearby_tickets


def check_ticket_number_in_range(ticket_number, constraint):
    lower, upper = constraint
    return lower <= ticket_number <= upper


def valid_ranges_for_ticket_number(ticket_number, constraints):
    return [c for c in constraints if check_ticket_number_in_range(ticket_number, c)]


def valid_constraint_sets_for_ticket_number(ticket_number, fields):
    return [field_name for field_name, cs in fields.items() if any(check_ticket_number_in_range(ticket_number, c) for c in cs)]

def get_valid_constraint_sets_positions_for_field_position(field_values, fields):
    valid_constraint_sets = [valid_constraint_sets_for_ticket_number(t, fields) for t in field_values]
    result = set(valid_constraint_sets[0])
    for vcs in valid_constraint_sets[1:]:
        result &= set(vcs)
    return result


def get_field_positions(valid_constraint_sets_by_field_position):
    result = [None for _ in valid_constraint_sets_by_field_position]
    already_picked = set()
    while any(len(s) == 1 for s in valid_constraint_sets_by_field_position):
        position, cs = next((i,cs) for i,cs in enumerate(valid_constraint_sets_by_field_position) if len(cs) == 1)
        result[position] = cs
        already_picked |= cs
        valid_constraint_sets_by_field_position = [v - already_picked for v in valid_constraint_sets_by_field_position]
    for position, cs in enumerate(valid_constraint_sets_by_field_position):
        if len(cs) != 0:
            result[position] = cs
    for field_order in product(*result):
        if len(field_order) != len(set(field_order)):
            continue
        return result


if __name__ == "__main__":
    filename = sys.argv[1]

    with open(filename, "r") as inf:
        text = inf.read()

    fields, my_ticket, nearby_tickets = parse(text)

    all_constraints = [ constraint for constraint_set in fields.values() for constraint in constraint_set ]
    invalid_ticket_numbers = [ticket_number for ticket in nearby_tickets for ticket_number in ticket if len(valid_ranges_for_ticket_number(ticket_number, all_constraints)) > 0]
    print(f"Sum of invalid ticket numbers: {sum(invalid_ticket_numbers)}")

    valid_nearby_tickets = [ticket for ticket in nearby_tickets if all(len(valid_constraint_sets_for_ticket_number(t, fields)) > 0 for t in ticket)]

    valid_constraint_set_positions_by_field_position = [get_valid_constraint_sets_positions_for_field_position((ticket[i] for ticket in valid_nearby_tickets), fields) for i in range(len(my_ticket))]

    # print(valid_constraint_set_positions_by_field_position)

    field_order = get_field_positions(valid_constraint_set_positions_by_field_position)
    print(field_order)
    departure_field_values = [x for i,x in enumerate(my_ticket) if field_order[i].pop().startswith("departure")]
    result = 1
    for d in departure_field_values:
        result *= d
    print(result)
