# -*- coding: utf8 -*-
import sys
from collections import deque
from os import system

BLANK = "O"

def width(board):
    return len(board[0])

def height(board):
    return len(board)

def x(coord):
    return coord[0]

def y(coord):
    return coord[1]

def offset(coord, rel):
    return x(coord) + x(rel), y(coord) + y(rel)

def set_item(board, coord, value):
    board[y(coord) - 1][x(coord) - 1] = value

def get_item(board, coord):
    return board[y(coord)- 1][x(coord) - 1]

def set_many(board, coords, value):
    for c in coords:
        set_item(board, c, value)

def get_many(board, coords):
    for c in coords:
        yield get_item(board, c)

def coords_of(board):
    yield from region(1, 1, width(board), height(board))

def region(col_start, row_start, col_end, row_end):
    for row in range(row_start, row_end + 1):
        for col in range(col_start, col_end + 1):
            yield col, row

def items(board):
    for coord in coords_of(board):
        yield coord, get_item(board, coord)

def contains(board, coord):
    """Check if a cmd is out of list range."""
    return 1 <= x(coord) <= width(board) and 1 <= y(coord) <= height(board)

def string(board):
    return "\n".join(("".join(row) for row in board))

# def flood(coord, inside, key, strategy=((-1, 0), (1, 0), (0, -1), (0, 1))):  # type: ignore
#     if not inside(coord):
#         return coord

#     yield coord

#     neighbor = (offset(coord, rel) for rel in strategy)

#     for n in neighbor:
#         if inside(n) and key(n):
#             yield from flood(n, inside, key)

def flood(original, inside, key, strategy=((-1, 0), (1, 0), (0, -1), (0, 1))):
    visited = set()
    pending = deque((original,))

    while pending:
        coord = pending.pop()
        visited.add(coord)

        yield coord

        neighbors = (offset(coord, rel) for rel in strategy)

        for n in neighbors:
            if (n not in visited
                    and inside(n)
                    and key(n)):
                pending.append(n)

def create_array(board, w, h, value=BLANK):
    """Create a array - 'I' Command."""
    board[:] = [[value] * w for _ in range(h)]

def clean_array(board, value=BLANK):
    """Clean a array - 'C' Command."""
    set_many(board, coords_of(board), value)

def color_pixel(board, col, row, color):
    """Change the old_color of one pixel - 'L' Command."""
    set_item(board, (col, row), color)

def ver_pixel(board, col, row_start, row_end, old_color):
    """ "Change the old_color of a columm - 'V' Command."""
    set_many(board, region(col, row_start, col, row_end), old_color)

def hor_pixel(board, col_start, col_end, row, old_color):
    """Change the old_color of a row - 'H' Command."""
    set_many(board, region(col_start, row, col_end, row), old_color)

def block_pixel(board, col_start, row_start, col_end, row_end, old_color):
    """Change old_color of an entire block - 'K' Command."""
    set_many(board, region(col_start, row_start, col_end, row_end), old_color)

def fill_pixel(board, col, row, new_color):
    """Fill a continuous region 'F' Command."""
    coord = (col, row)
    old_color = get_item(board, coord)

    def bound(coord):
        return contains(board, coord)

    def same_color(neighbor):
        return get_item(board, neighbor) == old_color
    
    set_many(board, flood(coord, inside=bound, key=same_color), new_color)

def save_array(board, filename):
    """Save the array with the 'S' Command."""
    with open(filename, "w") as f:
        f.write(string(board))

def prompt(convert):
    while True:
        value = input("> ")
        value = value.strip()

        try:
            value = convert(value)
        except ValueError as e:
            print(e)
        else:
            break

    return value

def parse(text, options="ICLVHKFSX"):
    '''Parse and validate a command string.'''
    tokens = text.upper().split()

    if not tokens or tokens[0] not in options:
        raise ValueError("Comando inv??lido.")

    for i, t in enumerate(tokens):
        if t.isdigit():
            tokens[i] = int(t)

    return tokens

def invoke(board, tokens):
    commands = {
            'X': sys.exit,
            'I': create_array,
            'L': color_pixel,
            'V': ver_pixel,
            'H': hor_pixel,
            'K': block_pixel,
            'F': fill_pixel,
            'S': save_array,
            'C': clean_array,
    }

    cmd, *args = tokens
    f = commands[cmd]
    f(board, *args)

def main():
    board = []
    while True:
        try:
            system('clear')
            print(string(board))
            cmd = prompt(parse)
            invoke(board, cmd)
        except TypeError:
            print("\nArgumentos inv??lidos!\n")
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
