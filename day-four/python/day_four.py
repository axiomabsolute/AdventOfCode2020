import re
import sys 

HEIGHT_PATTERN = r"^(?P<value>\d+)(?P<unit>cm|in)$"
PID_PATTERN = r"^\d{9}$"
HAIR_COLOR_PATTERN = r"^#[0-9a-f]{6}$"

def validate_height(entry):
    BOUNDS = {
        "cm": (150, 193),
        "in": (59, 76)
    }
    match = re.match(HEIGHT_PATTERN, entry)
    if not match:
        return match
    groups = match.groupdict()
    unit = groups["unit"]
    value = int(groups["value"])
    lower, upper = BOUNDS[unit]
    return lower <= value <= upper
     

REQUIRED_FIELDS = {
    'byr': lambda x: 1920 <= int(x) <= 2002,
    'iyr': lambda x: 2010 <= int(x) <= 2020,
    'eyr': lambda x: 2020 <= int(x) <= 2030,
    'hgt': validate_height,
    'hcl': lambda x: re.match(HAIR_COLOR_PATTERN, x),
    'ecl': lambda x: x in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'},
    'pid': lambda x: re.match(PID_PATTERN, x),
}

ALLOWED_FIELDS = {
    *REQUIRED_FIELDS,
    'cid',
}

def batch_to_records(batch):
    sections = batch.split("\n\n")
    records_kvs = [section.split() for section in sections]
    records = [dict([ kv.split(":") for kv in record ]) for record in records_kvs]
    return records

def validate_record(record):
    return all(k in record for k in REQUIRED_FIELDS)

def validate_record_strict(record):
    return all(k in record and REQUIRED_FIELDS[k](record[k]) for k in REQUIRED_FIELDS)

if __name__ == "__main__":
    filename = sys.argv[1]

    with open(filename, "r") as inf:
        batch = inf.read()
        records = batch_to_records(batch)
        valid_records = [r for r in records if validate_record(r)]
        print(f"Valid records: {len(valid_records)}")

        strict_valid_records = [r for r in records if validate_record_strict(r)]
        print(f"Strict valid records: {len(strict_valid_records)}")
    

