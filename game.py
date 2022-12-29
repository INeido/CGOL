"""
Game
====
"""
from world import World
import pygame
import time
import csv
import sys
import os


class Game:
    """
    ### Game

    Contains the functions needed to run the game.

    Parameters:
    :param res_h: Height of the Game.
    :param res_w: Width of the Game.
    :param c_a: Colour for alive cells.
    :param c_d: Colour for dead cells.
    :param cell_size: Size of a cell in pixel.
    :param tickrate: Number of times the game shall update in a second (FPS).
    :param save_file: Path of the in-/output file.
    """

    def __init__(self, res_h: int, res_w: int, c_a, c_d, cell_size: int, tickrate: int, save_file: str):
        self.res_h = res_h
        self.res_w = res_w
        self.c_a = c_a
        self.c_d = c_d
        self.cell_size = cell_size
        self.tickrate = tickrate
        self.save_file = save_file

    def setup_pygame(self):
        """
        ### Setup Pygame

        Creates and configures pygame instance.
        """
        pygame.init()

        self.dis = pygame.display.set_mode((self.res_h, self.res_w))
        pygame.display.set_caption("CGOL")

    def draw(self):
        """
        ### Draw Game

        Draws the current World.
        """
        self.dis.fill(self.c_d)
        for x in range(len(self.world.grid)):
            for y in range(len(self.world.grid[0])):
                if self.world.grid[x][y]:
                    pygame.draw.rect(self.dis, self.c_a, pygame.Rect(y*self.cell_size, x*self.cell_size, self.cell_size, self.cell_size))

    def create_world(self, size_x: int, size_y: int, seed: int, load: bool):
        """
        ### Create World

        Creates a new World Object.

        Parameters:
        :param size_x: Height of the Grid.
        :param size_y: Width of the Grid.
        :param seed: Seed for the array generation. Default is random (-1).
        :param load: Boolean indicating whether the last game should be loaded.
        """
        if load:
            try:
                self.world = World(size_x, size_y, seed, self.load_grid())
            except Exception as e:
                print("Couldn't load file.", e)
                self.shutdown()
        else:
            self.world = World(size_x, size_y, seed)

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
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.shutdown()

            try:
                self.world.generations += 1
                # Copy is needed because we are updating 'world' in place and we want to save the last full World.
                self.world.backup()

                # Draw before we start updating the cells.
                self.draw()
                pygame.display.update()

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
        pygame.quit()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
