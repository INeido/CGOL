from .game import Game
import argparse


def main():
    # Gather arguments
    parser = argparse.ArgumentParser(prog="CGOL", description="Conway's Game of Life")
    parser.add_argument("--res-h", "-rh", dest="rh", default=720, type=int, required=False, help="Height of the Game.")
    parser.add_argument("--res-w", "-rw", dest="rw", default=1280, type=int, required=False, help="Width of the Game.")
    parser.add_argument("--color-alive", "-ca", dest="ca", default=(255, 144, 0), type=int, required=False, help="Colour for alive cells. 'R G B'", nargs='+')
    parser.add_argument("--color-dead", "-cd", dest="cd", default=(0, 0, 0), type=int, required=False, help="Colour for dead cells. 'R G B'", nargs='+')
    parser.add_argument("--color-fade", "-cf", dest="cf", default=(0, 0, 0), type=int, required=False, help="Colour to fade dead cells to. 'R G B'", nargs='+')
    parser.add_argument("--color-background", "-cb", dest="cb", default=(16, 16, 16), type=int, required=False, help="Colour for dead cells. 'R G B'", nargs='+')
    parser.add_argument("--cell_size", "-cs", dest="cs", default=16, type=int, required=False, help="Size of a cell in pixel.")
    parser.add_argument("--size-x", "-sx", dest="sx", default=45, type=int, required=False, help="Height of the World.")
    parser.add_argument("--size-y", "-sy", dest="sy", default=80, type=int, required=False, help="Width of the World.")
    parser.add_argument("--tickrate", "-t", dest="t", default=30, type=float, required=False, help="Number of times the game shall update in a second (FPS).")
    parser.add_argument("--seed", "-s", dest="s", default=-1, type=int, required=False, help="Seed value used to create World.")
    parser.add_argument("--save-file", "-f", dest="f", default="./cgol.csv", type=str, required=False, help="Path of the in-/output file. (Should be .csv)")
    parser.add_argument("--load", "-l", dest="l", default=False, type=bool, required=False, help="Load revious save.")
    parser.add_argument("--pause-stalemate", "-ps", dest="ps", default=False, type=bool, required=False, help="Game pauses on a stalemate.")
    parser.add_argument("--pause-oscillators", "-po", dest="po", default=False, type=bool, required=False, help="Game pauses when only oscillators remain.")
    parser.add_argument("--fade-rate", "-fr", dest="fr", default=0.01, type=float, required=False, help="Value by which a cell should decrease every generation.")
    parser.add_argument("--fade-death-value", "-fd", dest="fd", default=0.5, type=float, required=False, help="Value a cell should have after death.")
    args = parser.parse_args()

    # Create new Game
    game = Game(args.rh, args.rw, tuple(args.ca), tuple(args.cd), tuple(args.cf), tuple(args.cb), args.cs, args.t, args.f, args.ps, args.po)

    game.setup_pygame()

    # Let Game create the World
    game.create_world(args.sx, args.sy, args.s, args.l, args.fr, args.fd)

    # Start Game
    game.game_loop()


if __name__ == "__main__":
    main()
