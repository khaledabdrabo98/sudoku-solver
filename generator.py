"""
Freely inspired by :
https://stackoverflow.com/questions/45471152/how-to-create-a-sudoku-puzzle-in-python

Adapted by Jonathan RAYBAUD--SERDA for the needs of this project, especially
regarding the output format of the generated grids.
"""

from argparse import ArgumentParser
from random import sample
from math import sqrt

def generate(size):
    nn = size * size

    def pattern(r, c):
        # Generate a list of offsets to shift each line.
        return(size * (r % size) + r // size + c) % nn

    def shuffle(s):
        return sample(s, len(s)) 

    # Block numbers (0, ..., size)
    rBase = range(size)
    rows  = [g * size + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols  = [g * size + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums = shuffle(range(1, nn + 1))

    # 2D array of grid rows.
    board = [[nums[pattern(r, c)] for c in cols] for r in rows]

    # Suppression of 3/4 of the numbers in the generated board
    nb_cells = nn * nn
    to_empty = nb_cells * 3 // 4
    #to_empty = nb_cells - 101
    for p in sample(range(nb_cells), to_empty):
        board[p // nn][p % nn] = 0

    return board

# Takes a grid as a 2D array of lines, and transforms it in a single string
# encoding the given numbers ('.' if empty cell, 1-9 or A-Z if number ≥ 10)
def transform(board):
    res = ''
    for line in board:
        for item in line:
            if item == 0:
                res += '.'
            elif item >= 10:
                res += chr(item + ord('A') - 10)
            else:
                res += str(item)
    return res

# Takes a single string and formats it so that it is presentable.
def parse(grid, file):
    dim = int(sqrt(len(grid)))

    count = 0
    for i in range(dim):
        line = ''
        for _ in range(dim):
            line += grid[count]
            count += 1

        if i == (dim - 1):
            file.write(f"\"{line}\",\n")
        else:
            file.write(f"\"{line}\"\n")
    file.write('\n')

def argument_parser():
    parser = ArgumentParser()

    parser.add_argument('-s', '--size', type=int, required=True,\
        help="The size of the grids to generate (n * n)")
    parser.add_argument('-n', '--number', type=int, required=True,\
        help="The number of grids to generate.")
    parser.add_argument('-f', '--file', type=str, required=True,\
        help="The file in which to generate the grids")

    return parser.parse_args()

def main():
    args = argument_parser()

    try:
        file = open(args.file, 'a')
    except:
        file = open(args.file, 'x')

    for _ in range(args.number):
        grid = generate(args.size)
        grid_str = transform(grid)
        parse(grid_str, file)
    file.close()

if __name__ == '__main__':
    main()

"""
Avec 3/4 des cases vidées, une grille n'a pas une unique solution. Il va falloir
définir le nombre minimal d'indices requis pour une solution unique...

Il semblerait que ce nombre soit 101.
"""