import argparse
import sys
import os


def get_save_path(subfolder: str) -> str:
    """Makes sure the subfolder folder exists and return its path.

    :return: The home directory of the user appended with subfolder.
    :rtype: string
    """
    path = os.path.expanduser("~") + subfolder
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def save_export(content: str, save_file: str) -> bool:
    """Saves string in file.
    """
    try:
        with open(save_file, "w") as file:
            file.write(content)
        print("Successfully saved into:", save_file)
        return True
    except Exception as e:
        print("Couldn't save file.", e)
        return False


def load_import(save_file) -> str:
    """Load the contents of a file.
    """
    try:
        with open(save_file, "r") as file:
            return file.read()
    except Exception as e:
        print("Couldn't load file.", e)
        return None


def shutdown(pygame) -> None:
    pygame.quit()
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)


def str2bool(value):
    if isinstance(value, bool):
        return value
    if value.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif value.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def parse_cli() -> argparse.Namespace:
    try:
        parser = argparse.ArgumentParser(
            prog="CGOL",
            description="Conway's Game of Life")
        parser.add_argument(
            "-rw",
            dest="rw",
            required=False,
            default=1280,
            type=int,
            help="Width of the Game.")
        parser.add_argument(
            "-rh",
            dest="rh",
            required=False,
            default=720,
            type=int,
            help="Height of the Game.")
        parser.add_argument(
            "-ca",
            dest="ca",
            required=False,
            default=(255, 144, 0),
            type=int,
            help="Color for alive cells. 'R G B'",
            nargs='+')
        parser.add_argument(
            "-cd",
            dest="cd",
            required=False,
            default=(0, 0, 0),
            type=int,
            help="Color for dead cells. 'R G B'",
            nargs='+')
        parser.add_argument(
            "-cf",
            dest="cf",
            required=False,
            default=(0, 0, 0),
            type=int,
            help="Color to fade dead cells to. 'R G B'",
            nargs='+')
        parser.add_argument(
            "-cb",
            dest="cb",
            required=False,
            default=(16, 16, 16),
            type=int,
            help="Color for dead cells. 'R G B'",
            nargs='+')
        parser.add_argument(
            "-cs",
            dest="cs",
            required=False,
            default=8,
            type=int,
            help="Size of a cell in pixel.")
        parser.add_argument(
            "-gw",
            dest="gw",
            required=False,
            default=160,
            type=int,
            help="Width of the World.")
        parser.add_argument(
            "-gh",
            dest="gh",
            required=False,
            default=90,
            type=int,
            help="Height of the World.")
        parser.add_argument(
            "-ti",
            dest="ti",
            required=False,
            default=60,
            type=float,
            help="Number of times the game shall update in a second (FPS).")
        parser.add_argument(
            "-se",
            dest="se",
            required=False,
            default=-1,
            type=int,
            help="Seed value used to create World.")
        parser.add_argument(
            "-ps",
            dest="ps",
            required=False,
            default=False,
            type=str2bool,
            nargs='?',
            const=True,
            help="Game pauses on a stalemate.")
        parser.add_argument(
            "-po",
            dest="po",
            required=False,
            default=False,
            type=str2bool,
            nargs='?',
            const=True,
            help="Game pauses when only oscillators remain.")
        parser.add_argument(
            "-fr",
            dest="fr",
            required=False,
            default=0.01,
            type=float,
            help="Value by which a cell should decrease every generation.")
        parser.add_argument(
            "-fd",
            dest="fd",
            required=False,
            default=0.5,
            type=float,
            help="Value a cell should have after death.")
        parser.add_argument(
            "-to",
            dest="to",
            required=False,
            default=True,
            type=str2bool,
            nargs='?',
            const=True,
            help="Enables toroidal space (Cells wrap around edges).")
        parser.add_argument(
            "-fa",
            dest="fa",
            required=False,
            default=True,
            type=str2bool,
            nargs='?',
            const=True,
            help="Enables fade effect.")
        args = parser.parse_args()
        return args
    except argparse.ArgumentError as err:
        sys.exit(2)


def get_configuration(args: argparse.Namespace) -> dict:
    return {
        "rw": args.rw,
        "rh": args.rh,
        "gw": args.gw,
        "gh": args.gh,
        "cs": args.cs,
        "ti": args.ti,
        "se": args.se,
        "ca": tuple(args.ca),
        "cd": tuple(args.cd),
        "cf": tuple(args.cf),
        "cb": tuple(args.cb),
        "fr": args.fr,
        "fd": args.fd,
        "ps": args.ps,
        "po": args.po,
        "to": args.to,
        "fa": args.fa,
    }
