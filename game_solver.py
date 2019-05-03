from copy import deepcopy
from pprint import pprint

from numpy.random import randint
from numpy.random import uniform as uni

number_of_spawns = 2
random_direction, down, right, up, left = 0, 1, 2, 3, 4


# game_duration is number of moves before end
def estimate_directions_win_probabilities(tiles, number_of_games=100, max_game_duration=25):
    global random_direction, down, right, up, left
    return {
        'left': estimate_win_probability(tiles, left, number_of_games, max_game_duration),
        'right': estimate_win_probability(tiles, right, number_of_games, max_game_duration),
        'up': estimate_win_probability(tiles, up, number_of_games, max_game_duration),
        'down': estimate_win_probability(tiles, down, number_of_games, max_game_duration)
    }


def estimate_win_probability(tiles, direction, number_of_games, max_game_duration):
    loses = 0
    total_moves = 0
    for game in range(number_of_games):
        temp_tiles = move(deepcopy(tiles), direction)
        if temp_tiles == tiles:
            continue
        for mv in range(max_game_duration):
            temp_tiles = spawn_random_tiles(temp_tiles)
            if not temp_tiles:  # game over
                loses += 1
                break
            total_moves += 1
            temp_tiles = move(temp_tiles)  # random move
    return 400 * total_moves / max_game_duration / number_of_games  # some formula


def spawn_random_tiles(tiles):
    dimension = len(tiles)
    empty_tiles = []
    for i in range(dimension):
        for j in range(dimension):
            if not tiles[i][j]:
                empty_tiles.append((i, j))
    if len(empty_tiles) == 0:
        return None

    global number_of_spawns

    for i in range(min(number_of_spawns, len(empty_tiles))):
        rand_index = randint(len(empty_tiles))
        i, j = empty_tiles.pop(rand_index)
        # set value 2 or 4
        tiles[i][j] = 2 if uni() < 0.9 else 4

    return tiles


# directions: random=0 down=1 right=2 up=3 left=4
def move(tiles, direction=0):
    if direction == 0:
        direction = randint(4) + 1

    dimension = len(tiles)

    vertical_move = direction == 1 or direction == 3
    if vertical_move:
        tiles_transposed = list(map(list, zip(*tiles)))  # columns
        positive_move_direction = direction == 1  # positive == up (1), not positive == down (3)
        for i in range(dimension):
            tiles_transposed[i] = move_in_line(tiles_transposed[i], move_right=positive_move_direction)
        # transpose back
        tiles = list(map(list, zip(*tiles_transposed)))
    else:  # horizontal move
        positive_move_direction = direction == 2  # positive == right (2), not positive == left (4)
        for i in range(dimension):
            tiles[i] = move_in_line(tiles[i], move_right=positive_move_direction)

    return tiles


# move to the left of line (list) with merges and stuff (time = o(n), memory = o(1)),  move_right=False is move left
def move_in_line(line, move_right=False):
    prev_tile_index = 0 if not move_right else len(line) - 1
    first_tile_index = 0 if not move_right else len(line) - 1
    last_index = len(line) if not move_right else -1
    step = 1 if not move_right else -1

    for i in range(prev_tile_index, last_index, step):
        if line[i] != 0:
            first_tile_index = i
            line[i], line[prev_tile_index] = 0, line[i]
            break
    pair_merged = False
    for i in range(first_tile_index + step, last_index, step):
        if not line[i]:
            continue
        if line[i] == line[prev_tile_index] and not pair_merged:
            # merge
            line[prev_tile_index] *= 2
            pair_merged = True
        else:
            prev_tile_index += step
            line[prev_tile_index] = line[i]
            pair_merged = False
        if prev_tile_index != i:
            line[i] = 0
    return line


def prnt(tiles):
    if not tiles:
        return print("NONO")
    for row in tiles:
        print(row)


if __name__ == '__main__':
    print('start script', __name__)
    test_tiles = [
        [4, 8, 32, 8],
        [0, 4, 8, 2],
        [0, 0, 4, 8],
        [0, 4, 2, 4]
    ]
    pprint(estimate_directions_win_probabilities(test_tiles))
