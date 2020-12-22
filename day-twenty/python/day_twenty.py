from collections import defaultdict
from math import sqrt
import sys

CARDINAL_TO_OPPOSITES = {
    "north": "south",
    "east": "west",
    "south": "north",
    "west": "east"
}

def parse_input(lines):
    tiles = {}
    tile_blocks = lines.read().split("\n\n")
    for tile_block in tile_blocks:
        tile_lines = tile_block.split("\n")
        tile_id = tile_lines[0].split(" ")[1][:-1]
        tile_rows = tuple(t.strip() for t in tile_lines[1:])
        tiles[tile_id] = tile_rows
    return tiles

def get_borders(tile_rows):
    north = tile_rows[0]
    south = tile_rows[-1]
    west = ''.join(t[0] for t in tile_rows)
    east = ''.join(t[:-1] for t in tile_rows)
    height = len(tile_rows)
    width = len(tile_rows[0])
    inner = tuple(''.join(tile_rows[i][1:width-1]) for i in range(1, height-1))
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


def get_candidate_cardinal_neighbors(border, cardinal_direction, by_borders):
    opposite = CARDINAL_TO_OPPOSITES[cardinal_direction] 
    return by_border[opposite][border]


def get_candidate_neighbors(tiles, borders, by_border):
    """Given a list of tiles and an index of borders, return a
    dictionary mapping tile_id->cardinal_direction->List[tile_id],
    where the leaf values are candidate neighbors whose opposite
    border matches the root key tile's border.
    """
    neighbor_candidates = {}
    for tile_id in tiles:
        north, east, south, west = borders[tile_id]
        northern_neighbors = get_candidate_cardinal_neighbors(
            north, "north", by_border
        )
        eastern_neighbors = get_candidate_cardinal_neighbors(
            east, "east", by_border
        )
        southern_neighbors = get_candidate_cardinal_neighbors(
            south, "south", by_border
        )
        western_neighbors = get_candidate_cardinal_neighbors(
            west, "west", by_border
        )
        neighbor_candidates[tile_id] = (
            northern_neighbors,
            eastern_neighbors,
            southern_neighbors,
            western_neighbors,
        )
        print(neighbor_candidates[tile_id])
    return neighbor_candidates


def expand_path(neighbors_by_tile, shape, x, y, path):
    if x == shape - 1 and y == shape - 1:
        yield path
    # Compute next indexes
    next_x = x + 1 % shape
    next_y = y + (1 if next_x == 0 else 0) % shape

    # Get next candidates for path
    cardinal_direction_of_neighbors = "south" if next_x == 0 else "east"
    # Order is NESW
    cardinal_index_of_neighbors = 2 if cardinal_direction_of_neighbors == "south" else 1
    previous = path[-shape] if next_x == 0 else path[-1]
    next_candidates = neighbors_by_tile[previous][cardinal_index_of_neighbors]

    # Recurse
    for c in next_candidates:
        yield from expand_path(shape, next_x, next_y, [*path, c])
    


def generate_candidates_for_root(shape, neighbors_by_tile):
    for root in neighbors_by_tile:
        yield from expand_path(neighbors_by_tile, shape, 1, 0, [root])


def get_candidate_layouts(neighbors_by_tile, shape):
    """Given a dictionary mapping from tile_id->List[List[neighbors]]
       return a List[List[tile_id]] of valid sequences of tiles.
    """
    candidate_layouts = []
    for tile_id, tile in neighbors_by_tile.items():
        candidates_for_root = generate_candidates_for_root(shape, neighbors_by_tile)
        candidate_layouts.extend(candidates_for_root)
    return candidate_layouts
        

if __name__ == "__main__":
    filename = sys.argv[1]

    with open(filename, "r") as inf:
        tiles = parse_input(inf)
        shape = sqrt(len(tiles))
        by_border, borders, inners = index_by_border(tiles)
        neighbors_by_tile = get_candidate_neighbors(tiles, borders, by_border)
        candidate_layouts = get_candidate_layouts(neighbors_by_tile, shape)
        for candidate_layout in candidate_layouts:
            print(candidate_layout)
        # print(f"Candidate layouts: {len(candidate_layouts)}")

