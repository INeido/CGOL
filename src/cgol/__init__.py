from .game import *
from .utils import *


def main():
    args = parse_cli()
    config = get_configuration(args)
    game = Game(**config)
    game.run()


if __name__ == "__main__":
    main()
