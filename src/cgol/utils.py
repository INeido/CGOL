import csv
import sys
import os


def get_save_path():
    """Makes sure the 'cgol/images' folder exists and return its path.

    :return: The home directory of the user appended with '/cgol/images'.capitalize()
    :rtype: string
    """
    path = os.path.expanduser("~") + "/cgol/images/"
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def save_grid(grid, save_file):
    """Saves the Grid into a CSV file.
    """
    try:
        with open(save_file, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)

            for row in grid:
                writer.writerow(row)
        print("Last tick saved into:", save_file)
        return True
    except Exception as e:
        print("Couldn't save file.", e)
        return False


def load_grid(save_file):
    """Loads the Grid from a CSV file.

    :return: Rows of the CSV.
    :rtype: array
    """
    with open(save_file, "r") as csvfile:
        reader = csv.reader(csvfile)
        return [row for row in reader]


def shutdown(pygame):
    pygame.quit()
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
