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
    parser.add_argument("--size-x", "-x", dest="size_x", default=10, type=int, required=False, help="Height of the World.")
    parser.add_argument("--size-y", "-y", dest="size_y", default=10, type=int, required=False, help="Width of the World.")
    parser.add_argument("--tickrate", "-t", dest="tickrate", default=1, type=float, required=False, help="Number of times the game shall update in a second (FPS).")
    parser.add_argument("--seed", "-s", dest="seed", default=-1, type=int, required=False, help="Seed value used to create World.")
    parser.add_argument("--toroidal", "-o", dest="toroidal", default=False, type=bool, required=False, help="Boolean indicating whether the space is toroidal or not.")
    parser.add_argument("--save-file", "-f", dest="save_file", default="./cgol.csv", type=str, required=False, help="Path of the in-/output file. (Should be .csv)")
    parser.add_argument("--load", "-l", dest="load", default=False, type=bool, required=False, help="Boolean determining if a previous save should be loaded.")
    args = parser.parse_args()

    # Create new Game
    game = Game(args.tickrate, args.save_file)

    # Let Game create the World
    game.create_world(args.size_x, args.size_y, args.seed, args.toroidal, args.load)

    # Start Game
    game.game_loop()


if __name__ == "__main__":
    main()
