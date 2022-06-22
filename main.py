import argparse
import curses
import time


from itertools import product
from random import uniform
from curses import window


UPDATE_RATE = 0.15


Cell = bool
Board = list[list[Cell]]
NeighborCount = tuple[Cell, int]
NeighborCountBoard = list[list[NeighborCount]]
Index = tuple[int, int]


def create_board(n: int, m: int, p: float = 0.35) -> Board:
    return [[uniform(0, 1) <= p for _ in range(m)] for _ in range(n)]


def update_cell(cell: Cell, neighbors: int) -> Cell:
    if not cell and neighbors == 3:
        return True

    if cell and neighbors in [2, 3]:
        return True

    return False


def valid_neighbors(i: int, j: int, n: int, m: int) -> set[Index]:
    di, dj = {-1, 0, 1}, {-1, 0, 1}

    if i == 0:
        di.remove(-1)

    elif i == n - 1:
        di.remove(1)

    if j == 0:
        dj.remove(-1)

    elif j == m - 1:
        dj.remove(1)

    deltas = set(product(di, dj))
    deltas.remove((0, 0))

    return deltas


def count_neighbors(board: Board, i: int, j: int) -> NeighborCount:
    n, m = len(board), len(board[0])
    cell = board[i][j]
    output = 0

    deltas = valid_neighbors(i, j, n, m)
    for di, dj in deltas:
        output += int(board[i + di][j + dj])

    return cell, output


def count(board: Board) -> NeighborCountBoard:
    n, m = len(board), len(board[0])
    return [[count_neighbors(board, i, j) for j in range(m)] for i in range(n)]


def update(board: Board) -> Board:
    n, m = len(board), len(board[0])
    neighbor_count = count(board)
    return [[update_cell(*neighbor_count[i][j]) for j in range(m)] for i in range(n)]


def render(stdscr: window, board: Board) -> None:
    n, m = len(board), len(board[0])
    print_dict = {False: ('-', curses.A_DIM), True: ('+', curses.A_BOLD)}

    stdscr.clear()
    for i in range(n):
        for j in range(m):
            t, b = print_dict[board[i][j]]
            stdscr.addstr(i, j, t, b)
    stdscr.refresh()

    time.sleep(UPDATE_RATE)


def parse_args() -> tuple[int, int, int, float]:
    parser = argparse.ArgumentParser(description='The game of life')
    parser.add_argument('-n', type=int, default=20, help='number of rows')
    parser.add_argument('-m', type=int, default=100, help="number of columns")
    parser.add_argument('-t', type=int, default=50, help="number of iterations")
    parser.add_argument('-p', type=float, default=0.35, help="initial probability of being alive")

    args = parser.parse_args()

    return args.n, args.m, args.t, args.p


def main() -> None:
    stdscr = curses.initscr()
    n, m, t, p = parse_args()

    board = create_board(n, m, p)
    render(stdscr, board)

    i = 0
    while i < t:
        board = update(board)
        render(stdscr, board)
        i += 1

    stdscr.clear()


if __name__ == '__main__':
    main()
