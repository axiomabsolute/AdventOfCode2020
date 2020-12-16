from itertools import permutations
import sys

def parse_value(value_line):
    value_name, constraint_section = value_line.split(": ")
    raw_constraints = constraint_section.split(" or ")
    constraints = tuple(
        tuple(int(r) for r in c.split("-")) for c in raw_constraints
    )
    return value_name, constraints

def parse_values(values_section):
    return dict( 
        parse_value(value_line)
        for value_line in 
        values_section.split("\n")
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
    values_section, my_ticket_section, nearby_tickets_section = text.split("\n\n")
    values = parse_values(values_section)
    my_ticket = parse_my_ticket(my_ticket_section)
    nearby_tickets = parse_nearby_tickets(nearby_tickets_section)
    return values, my_ticket, nearby_tickets


def validate_ticket_numbers_not_in_any_range(ticket, values):
    for ticket_number in ticket:
        if not any(
            validate_field(ticket_number, constraint_set) for constraint_set in values.values()
        ):
            yield ticket_number

def validate_field(ticket_number, constraint_set):
    return any(lower <= ticket_number <= upper for lower, upper in constraint_set)
            

def validate_tickets(nearby_tickets, values, validator):
    """ Apply a validator to each nearby ticket and return the ticket with the
    results of the validator.
    
    Validator should return invalid ticket values, or None"""
    return [(ticket, list(validator(ticket, values))) for ticket in nearby_tickets]


if __name__ == "__main__":
    filename = sys.argv[1]

    with open(filename, "r") as inf:
        text = inf.read()

    values, my_ticket, nearby_tickets = parse(text)

    validation_results = validate_tickets(nearby_tickets, values, validate_ticket_numbers_not_in_any_range)
    invalid_results = [invalid_number for ticket, result in validation_results for invalid_number in result]
    print(sum(invalid_results))

    # valid_results = [ticket for ticket, result in validation_results if result]

