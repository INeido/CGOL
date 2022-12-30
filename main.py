"""
CGOL
====
A whack Conway's Game of Life implementation.

Rules of Conway's Game of Life:
1. Any live cell with two or three live neighbours survives.
2. Any dead cell with three live neighbours becomes a live cell.
3. All other live cells die in the next generation. Similarly, all other dead cells stay dead.

Github Repo:
https://github.com/INeido/CGOL
"""
from game import Game
import argparse


def main():
    # Gather arguments
    parser = argparse.ArgumentParser(prog="CGOL", description="Conway's Game of Life")
    parser.add_argument("--res-h", "-rh", dest="res_h", default=720, type=int, required=False, help="Height of the Game.")
    parser.add_argument("--res-w", "-rw", dest="res_w", default=1280, type=int, required=False, help="Width of the Game.")
    parser.add_argument("--colour-alive", "-ca", dest="c_a", default=(255, 255, 255), type=int, required=False, help="Colour for alive cells. 'R G B'", nargs='+')
    parser.add_argument("--colour-dead", "-cd", dest="c_d", default=(0, 0, 0), type=int, required=False, help="Colour for dead cells. 'R G B'", nargs='+')
    parser.add_argument("--colour-background", "-cb", dest="c_b", default=(125, 125, 125), type=int, required=False, help="Colour for dead cells. 'R G B'", nargs='+')
    parser.add_argument("--cell_size", "-cs", dest="cell_size", default=16, type=int, required=False, help="Size of a cell in pixel.")
    parser.add_argument("--size-x", "-sx", dest="size_x", default=45, type=int, required=False, help="Height of the World.")
    parser.add_argument("--size-y", "-sy", dest="size_y", default=80, type=int, required=False, help="Width of the World.")
    parser.add_argument("--tickrate", "-t", dest="tickrate", default=30, type=float, required=False, help="Number of times the game shall update in a second (FPS).")
    parser.add_argument("--seed", "-s", dest="seed", default=-1, type=int, required=False, help="Seed value used to create World.")
    parser.add_argument("--save-file", "-f", dest="save_file", default="./cgol.csv", type=str, required=False, help="Path of the in-/output file. (Should be .csv)")
    parser.add_argument("--load", "-l", dest="load", default=False, type=bool, required=False, help="Load revious save.")
    parser.add_argument("--pause-stalemate", "-ps", dest="pause_stalemate", default=False, type=bool, required=False, help="Game pauses on a stalemate.")
    parser.add_argument("--pause-oscillators", "-po", dest="pause_oscillators", default=False, type=bool, required=False, help="Game pauses when only oscillators remain.")
    args = parser.parse_args()

    # Create new Game
    game = Game(args.res_h, args.res_w, tuple(args.c_a), tuple(args.c_d), tuple(args.c_b), args.cell_size, args.tickrate, args.save_file, args.pause_stalemate, args.pause_oscillators)

    game.setup_pygame()

    # Let Game create the World
    game.create_world(args.size_x, args.size_y, args.seed, args.load)

    # Start Game
    game.game_loop()


if __name__ == "__main__":
    main()
