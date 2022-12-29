from world import World
import time
import csv
import sys
import os


class Game:
    """
    ### Game

    Contains the functions needed to run the game.
    """

    def __init__(self, tickrate: int, save_file: str, load: bool):
        """
        ### Game Constructor

        Initiates the Game Class.

        Parameters:
        :param tickrate: Number of times the game shall update in a second (FPS).
        :param save_file: Path of the in-/output file.
        """
        self.tickrate = tickrate
        self.save_file = save_file
        self.load = load
        self.world = None

    def create_world(self, size_x: int, size_y: int, seed: int, toroidal: bool):
        """
        ### Create World

        Creates a new World Object.

        Parameters:
        :param size_x: Height of the Grid.
        :param size_y: Width of the Grid.
        :param seed: Seed for the array generation. Default is random (-1).
        :param toroidal: Boolean indicating whether the space is toroidal or not.
        """
        # Get the World
        if self.load:
            try:
                self.world = World(size_x, size_y, seed, toroidal, self.load_grid())
            except Exception as e:
                print("Couldn't load file.", e)
                self.shutdown()
        else:
            # Create new World
            self.world = World(size_x, size_y, seed, toroidal)

    def display(self, clear: bool = True):
        """
        ### Display

        Displays the Grid.

        Parameters:
        :param clear: Defines if console should be cleared before outputting.
        """
        if clear:
            try:
                os.system("cls" if os.name in ("nt", "dos") else "clear")
            except:
                pass

        for row in self.world.grid:
            for cell in row:
                if cell == 0:
                    print(" ", end=" ")
                else:
                    print("■", end=" ")
            print()

    def save_grid(self):
        """
        ### Save Grid

        Saves the Grid into a CSV file.
        """
        with open(self.save_file, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)

            for row in self.world.grid:
                writer.writerow(row)
            writer.writerow([self.world.seed])
            writer.writerow([self.world.generations])

    def load_grid(self):
        """
        ### Load Grid

        Loads the Grid from a CSV file.

        Returns:
        array: Rows of the CSV
        int: Seed value used to create Grid.
        """
        with open(self.save_file, "r") as csvfile:
            reader = csv.reader(csvfile)
            return [row for row in reader]

    def game_loop(self):
        """
        ### Game Loop

        The engine that runs the game indefinetly until Keyboardinterrupt.
        """
        while True:
            try:
                self.world.generations += 1
                # Copy is needed because we are updating 'world' in place and we want to save the last full World.
                self.world.backup()

                # Display before we start updating the cells.
                self.display()

                # Convert tickrate to seconds for sleep.
                time.sleep(1 / self.tickrate)

                # Loop through every cell to first get the count of the neighbours and then update the cell state.
                self.world.update()

                # Catch if the World stopped developing because of a stalemate.
                if self.world.compare_backup():
                    print("\nGame stopped. Reason: Stalemate.")
                    break

            except (KeyboardInterrupt):
                print("\nGame stopped. Reason: KeyboardInterrupt.")
                break

        try:
            self.save_grid()
            print("Last tick saved into:", self.save_file)
        except Exception as e:
            print("Couldn't save file.", e)

        print("")
        print("Seed used: ", self.world.seed)
        print("Generations: ", self.world.generations)

        self.shutdown()

    def shutdown(self):
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
