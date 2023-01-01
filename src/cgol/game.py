"""
CGOL
====
A Conway's Game of Life implementation using numpy and pygame.

Rules of Conway's Game of Life:
1. Any live cell with two or three live neighbors survives.
2. Any dead cell with three live neighbors becomes a live cell.
3. All other live cells die in the next generation. Similarly, all other dead cells stay dead.

Github Repo:
https://github.com/INeido/CGOL
"""
from .world import World
from pygame.locals import *
import pygame
import numpy
import csv
import sys
import os


class Game:
    """Game
    ====

    Contains the functions needed to run the game.

    :param int res_h: Height of the Game.
    :param int res_w: Width of the Game.
    :param tuple c_a: Colour for alive cells.
    :param tuple c_d: Colour for dead cells.
    :param tuple c_b: Colour for background.
    :param int cell_size: Size of a cell in pixel.
    :param int tickrate: Number of times the game shall update in a second (FPS).
    :param str save_file: Path of the in-/output file.
    :param bool pause_stalemate: Game pauses on a stalemate.
    :param bool pause_oscillators: Game pauses when only oscillators remain.
    """

    def __init__(self, res_h: int, res_w: int, c_a: tuple, c_d: tuple, c_f: tuple, c_b: tuple, cell_size: int, tickrate: int, save_file: str, pause_stalemate: bool, pause_oscillators: bool):
        self.res_h = res_h
        self.res_w = res_w
        self.c_a = c_a
        self.c_d = c_d
        self.c_f = c_f
        self.c_b = c_b
        self.cell_size = cell_size
        self.tickrate = tickrate
        self.save_file = save_file
        self.pause_stalemate = pause_stalemate
        self.pause_oscillators = pause_oscillators

    def setup_pygame(self):
        """Setup Pygame
        ====

        Creates and configures pygame instance.
        """
        pygame.init()
        pygame.display.set_caption("CGOL", "hardware")
        self.dis = pygame.display.set_mode((self.res_w, self.res_h), 0, 8)
        self.clock = pygame.time.Clock()

    def get_save_path(self):
        """Get Save Path
        ====

        Makes sure the 'cgol/images' folder exists and return its path.

        :return: The home directory of the user appended with '/cgol/images'.capitalize()
        :rtype: string
        """
        path = os.path.expanduser("~") + "/cgol/images/"
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def get_borders(self):
        """Get Borders
        ====

        Gets the visible edges of the grid.
        """
        self.vis_west = max(0, int((-self.offset_x) / self.cell_size))
        self.vis_east = min(self.world.size_y, self.world.size_y - int(self.offset_x / self.cell_size) - self.world.size_y - int(-self.res_w / self.cell_size) + 1)
        self.vis_north = max(0, int((-self.offset_y) / self.cell_size))
        self.vis_south = min(self.world.size_x, self.world.size_x - int(self.offset_y / self.cell_size) - self.world.size_x - int(-self.res_h / self.cell_size) + 1)

    def draw(self):
        """Draw Game
        ====

        Draws the current World.
        """
        # Reset background to background color
        self.dis.fill(self.c_b)
        self.sur.fill(self.c_d)

        # Update surface with changed pixels
        for x in range(self.vis_north, self.vis_south):
            for y in range(self.vis_west, self.vis_east):
                fade_value = self.world.grid[x][y]
                if fade_value > 0:
                    color = pygame.Color(self.c_f)
                    new_color = color.lerp(self.c_a, fade_value)
                    pygame.draw.rect(self.sur, new_color, pygame.Rect(y*self.cell_size, x*self.cell_size, self.cell_size, self.cell_size))

        # Draw surface in display
        self.dis.blit(self.sur, (self.offset_x, self.offset_y))
        # Update display
        pygame.display.flip()

    def update_surface(self):
        # Calculate range of cells to draw
        self.get_borders()

        self.sur = pygame.Surface((self.world.size_y*self.cell_size, self.world.size_x*self.cell_size))

    def center(self):
        """Center
        ====

        Updates offsets so that grid is centered.
        """
        self.offset_x = (self.res_w / 2) - (self.world.size_y / 2 * self.cell_size)
        self.offset_y = (self.res_h / 2) - (self.world.size_x / 2 * self.cell_size)

    def create_world(self, size_x: int, size_y: int, seed: int, load: bool, fr, fd):
        """Create World
        ====

        Creates a new World Object.

        Parameters:
        :param int size_x: Height of the Grid.
        :param int size_y: Width of the Grid.
        :param int seed: Seed for the array generation. Default is random (-1).
        :param bool load: Boolean indicating whether the last game should be loaded.
        """
        if load:
            try:
                self.world = World(size_x, size_y, seed, fr, fd, self.load_grid())
            except Exception as e:
                print("Couldn't load file.", e)
                self.shutdown()
        else:
            self.world = World(size_x, size_y, seed, fr, fd)

        # Gets correct offsets to center the grid
        self.center()

        # Create the pygame surface in the correct size
        self.update_surface()

    def save_grid(self):
        """Save Grid
        ====

        Saves the Grid into a CSV file.
        """
        try:
            with open(self.save_file, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)

                for row in self.world.grid:
                    writer.writerow(row)
                writer.writerow([self.world.seed])
                writer.writerow([self.world.generations])
            print("Last tick saved into:", self.save_file)

            print("")
            print("Seed used: ", self.world.seed)
            print("Generations: ", self.world.generations)
        except Exception as e:
            print("Couldn't save file.", e)

    def load_grid(self):
        """Load Grid
        ====

        Loads the Grid from a CSV file.

        :return: Rows of the CSV.
        :rtype: array
        """
        with open(self.save_file, "r") as csvfile:
            reader = csv.reader(csvfile)
            return [row for row in reader]

    def calc_generation(self):
        """Calc Generation
        ====

        Calculates and renders the cells.
        """
        # Iterate generations
        self.world.generations += 1

        # Copy is needed because we are updating 'world' in place and we want to save the last full World
        self.world.backup()

        # Update the state of the world
        self.world.update()

        # Catch if the World stopped developing because of a stalemate
        if self.pause_stalemate and self.world.check_stalemate():
            print("\nGame stopped. Reason: Stalemate.")
            self.game_loop(pause=True)

        # Catch if the World stopped developing because only oscillators remain
        if self.pause_oscillators and self.world.check_oscillators():
            print("\nGame stopped. Reason: Only Oscillators remaining.")
            self.game_loop(pause=True)

    def interpolate(self, point0, point1):
        """Interpolate
        ====

        Interpolates between two points.

        :return: Coordinates of interpolated cells.
        :rtype: tuple or int
        """
        # Calculate distance between previous and current position
        distance = numpy.linalg.norm(numpy.array(point1) - numpy.array(point0))

        # Prevent division by zero
        if distance >= 2:
            # Calculate steps in x and y directions
            steps = numpy.stack(numpy.linspace(point0, point1, int(distance / 2)))

            # Calculate coordinates of interpolated cells
            x = (steps[:, 1]-self.offset_y)//self.cell_size
            y = (steps[:, 0]-self.offset_x)//self.cell_size

            return x.astype(int), y.astype(int)
        else:
            # Calculate coordinates of normal cells
            x = (point1[1]-self.offset_y)//self.cell_size
            y = (point1[0]-self.offset_x)//self.cell_size

            return int(x), int(y)

    def game_loop(self, pause=False):
        """Game Loop
        ====

        The main loop that runs the game.
        """
        # Flags
        is_looping = True
        running = not pause
        draw = False
        drag = False
        prev_pos = None

        while True:
            self.clock.tick(self.tickrate)

            # Save mouse position
            curr_pos = pygame.mouse.get_pos()

            # Screen drag
            if drag and prev_pos != None:
                self.offset_x, self.offset_y = numpy.add(numpy.subtract(curr_pos, prev_pos), (oldoffset_x, oldoffset_y))
                self.update_surface()

            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.shutdown()
                # Key events
                elif event.type == pygame.KEYDOWN:
                    # RETURN pressed: Pause game
                    if event.key == pygame.K_RETURN:
                        running = not running
                    # ESCAPE pressed: Close game
                    if event.key == pygame.K_ESCAPE:
                        self.shutdown()
                    # Right Arrow pressed: Forward one generation
                    if event.key == pygame.K_RIGHT:
                        self.calc_generation()
                    # R pressed: Reset game
                    if event.key == pygame.K_r:
                        self.world.populate("seed")
                    # F pressed: Fill with random cells
                    if event.key == pygame.K_f:
                        self.world.populate("random")
                    # A pressed: Fill with alive cells
                    if event.key == pygame.K_a:
                        self.world.populate("alive")
                    # D pressed: Fill with dead cells
                    if event.key == pygame.K_d:
                        self.world.populate("dead")
                    # K pressed: Kill alive cells
                    if event.key == pygame.K_k:
                        self.world.populate("kill")
                    # L pressed: Load last saved game
                    if event.key == pygame.K_l:
                        self.world.load_from_csv(self.load_grid())
                        self.update_surface()
                    # S pressed: Save current game
                    if event.key == pygame.K_s:
                        self.save_grid()
                    # C pressed: Center view
                    if event.key == pygame.K_c:
                        self.center()
                        self.update_surface()
                    # P pressed: Save screenshot
                    if event.key == pygame.K_p:
                        pygame.image.save(self.sur, f"{self.get_save_path() + str(self.world.generations)}.png")
                    # + pressed: Extend grid
                    if event.key == pygame.K_PLUS:
                        self.world.extend()
                        self.update_surface()
                    # - pressed: Reduce grid
                    if event.key == pygame.K_MINUS:
                        self.world.reduce()
                        self.update_surface()

                # Mouse events
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Left/Right Click: Draw
                    if event.button == 1 or event.button == 3:
                        oldoffset_x, oldoffset_y = self.offset_x, self.offset_y
                        prev_pos = curr_pos
                        draw = True
                    if event.button == 1:
                        draw_color = 1
                    if event.button == 3:
                        draw_color = 0
                    # Middle Mouse: Drag screen
                    if event.button == 2:
                        oldoffset_x, oldoffset_y = self.offset_x, self.offset_y
                        prev_pos = curr_pos
                        drag = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    # Left/Right Click: Draw
                    if event.button == 1 or event.button == 3:
                        prev_pos = None
                        draw = False
                    # Middle Mouse: Drag screen
                    if event.button == 2:
                        prev_pos = None
                        drag = False

                # Zoom
                elif event.type == pygame.MOUSEWHEEL:
                    if event.y == 1 and self.cell_size < 128:
                        self.cell_size *= 2
                        self.offset_x = curr_pos[0] + (self.offset_x - curr_pos[0]) * 2
                        self.offset_y = curr_pos[1] + (self.offset_y - curr_pos[1]) * 2
                        self.update_surface()
                    elif event.y == -1 and self.cell_size > 1:
                        self.cell_size /= 2
                        self.offset_x = curr_pos[0] + (self.offset_x - curr_pos[0]) / 2
                        self.offset_y = curr_pos[1] + (self.offset_y - curr_pos[1]) / 2
                        self.update_surface()

            # Interpolate to prevent dotted line
            if draw and prev_pos != None:
                x, y = self.interpolate(prev_pos, curr_pos)
                if isinstance(x, int) and isinstance(y, int):
                    if 0 <= x < self.world.size_x and 0 <= y < self.world.size_y:
                        self.world.grid[x, y] = draw_color or (0.5 if self.world.grid[x, y] == 1.0 and not draw_color else self.world.grid[x, y])
                elif min(x) >= 0 and max(x) < self.world.size_x and min(y) >= 0 and max(y) < self.world.size_y:
                    for xc, yc in zip(x, y):
                        self.world.grid[xc, yc] = draw_color or (0.5 if self.world.grid[xc, yc] == 1.0 and not draw_color else self.world.grid[xc, yc])
                prev_pos = curr_pos

            # Break out of main loop
            if not is_looping:
                break

            # Draw before we start updating the cells
            self.draw()

            # Skip over generation to pause game
            if not running or draw:
                continue

            # Calculate the next generation
            self.calc_generation()

        self.shutdown()

    def shutdown(self):
        pygame.quit()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
