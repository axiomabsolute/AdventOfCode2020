import sys

def parse_input(lines):
    tiles = {}
    tile_blocks = lines.read().split("\n\n")
    for tile_block in tile_blocks:
        tile_lines = tile_block.split("\n")
        tile_id = next(tile_lines).split(" ")[:-1]
        tile_rows = list(tile_lines)
        tiles[tile_id] = tile_rows
    return tiles
            

if __name__ == "__main__":
    filename = sys.argv[1]

    with open(filename, "r") as inf:
        tiles = parse_input(inf)