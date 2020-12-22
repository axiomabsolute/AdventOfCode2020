from collections import defaultdict
import sys

def parse_input(lines):
    tiles = {}
    tile_blocks = lines.read().split("\n\n")
    for tile_block in tile_blocks:
        tile_lines = tile_block.split("\n")
        tile_id = tuple(tile_lines[0].split(" ")[:-1])
        tile_rows = tuple(t.strip() for t in tile_lines[1:])
        tiles[tile_id] = tile_rows
    return tiles

def get_borders(tile_rows):
    north = tuple(tile_rows[0])
    south = tuple(tile_rows[-1])
    west = tuple(t[0] for t in tile_rows)
    east = tuple(t[:-1] for t in tile_rows)
    height = len(tile_rows)
    width = len(tile_rows[0])
    inner = tuple(tuple(tile_rows[i][1:width-1]) for i in range(1, height-1))
    return north, east, south, west, inner

def index_by_border(tiles):
    """Given a dictionary of tile_id->rows, return a dictionary mapping       cardinal_direction->border_string->List[tile_id]
    """
    by_border = {
        "north": defaultdict(lambda: []),
        "east": defaultdict(lambda: []),
        "south": defaultdict(lambda: []),
        "west": defaultdict(lambda: []),
    }
    borders = {}
    inners = {}
    for tile_id, tile_rows in tiles.items():
        north, east, south, west, inner = get_borders(tile_rows)
        by_border["north"][north].append(tile_id)
        by_border["east"][east].append(tile_id)
        by_border["south"][south].append(tile_id)
        by_border["west"][west].append(tile_id)
        inners[tile_id] = inner
        borders[tile_id] = (north, east, south, west)
    return by_border, borders, inners


def get_candidate_neighbors(tiles, borders, by_border):
    """Given a list of tiles and an index of borders, return a
    dictionary mapping tile_id->cardinal_direction->List[tile_id],
    where the leaf values are candidate neighbors whose opposite
    border matches the root key tile's border.
    """
    for tile_id in tiles:
        north, east, south, west = borders[tile_id]
        # For each, look up candidate neighbors in by_border 
        # ??? Profit?

if __name__ == "__main__":
    filename = sys.argv[1]

    with open(filename, "r") as inf:
        tiles = parse_input(inf)
        by_border, borders, inners = index_by_border(tiles)
        print(by_border.keys())

