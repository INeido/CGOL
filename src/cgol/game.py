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
from world import World
from utils import *
import pygame
import numpy


class Game:
    """Game
    ====

    Contains the functions needed to run the game.

    :param int res_height: Height of the Game.
    :param int res_width: Width of the Game.
    :param tuple color_alive: Colour for alive cells.
    :param tuple color_dead: Colour for dead cells.
    :param tuple color_background: Colour for background.
    :param int cell_size: Size of a cell in pixel.
    :param int tickrate: Number of times the game shall update in a second (FPS).
    :param str save_file: Path of the in-/output file.
    :param bool pause_stalemate: Game pauses on a stalemate.
    :param bool pause_oscillators: Game pauses when only oscillators remain.
    """

    def __init__(self, res_width: int, res_height: int, color_alive: tuple, color_dead: tuple, color_fade: tuple, color_background: tuple, cell_size: int, tickrate: int, save_file: str, pause_stalemate: bool, pause_oscillators: bool):
        self.res_width = res_width
        self.res_height = res_height
        self.color_alive = numpy.array(color_alive)
        self.color_dead = numpy.array(color_dead)
        self.color_fade = numpy.array(color_fade)
        self.color_background = numpy.array(color_background)
        self.cell_size = cell_size
        self.tickrate = tickrate
        self.save_file = save_file
        self.pause_stalemate = pause_stalemate
        self.pause_oscillators = pause_oscillators

    def setup_pygame(self):
        """Creates and configures pygame instance.
        """
        pygame.init()
        pygame.display.set_caption("CGOL", "hardware")
        self.dis = pygame.display.set_mode((self.res_width, self.res_height), 0, 8)
        self.clock = pygame.time.Clock()

    def get_borders(self):
        """Determines the visible edges of the grid based on the current viewport.

        This function updates the following instance variables with the calculated values:
            - vis_west: The x-coordinate of the leftmost visible column of cells.
            - vis_east: The x-coordinate of the rightmost visible column of cells.
            - vis_north: The y-coordinate of the topmost visible row of cells.
            - vis_south: The y-coordinate of the bottommost visible row of cells.
            - vis_width: The width of the visible region, in pixels.
            - vis_height: The height of the visible region, in pixels.
        """
        self.vis_west = max(0, int((-self.offset_y) / self.cell_size))
        self.vis_east = max(0, min(self.world.grid_height, self.world.grid_height - int(self.offset_y / self.cell_size) - self.world.grid_height - int(-self.res_height / self.cell_size) + 1))
        self.vis_north = max(0, int((-self.offset_x) / self.cell_size))
        self.vis_south = max(0, min(self.world.grid_width, self.world.grid_width - int(self.offset_x / self.cell_size) - self.world.grid_width - int(-self.res_width / self.cell_size) + 1))
        self.vis_width = (self.vis_south - self.vis_north) * self.cell_size
        self.vis_height = (self.vis_east - self.vis_west) * self.cell_size
        print((self.vis_west, self.vis_east))

        print((self.vis_north, self.vis_south))

        print((self.vis_width, self.vis_height))

        print((self.offset_x, self.offset_y))

    def draw(self):
        """Converts the 2D Numpy Array of floats to a 3D Numpy Array of integers.
        More specifically it creates a 3rd dimension with depth 3
        holding the RGB values.

        Before:                     After:

        Shape:      (2, 2)          (2, 2, 3)

        Example:    [[0.5  1.  ]    [[[127  72   0]  [255 144   0]]
                     [0.   0.49]]    [[  0   0   0]  [124  70   0]]]

        The colors in this example used were
        Color alive: [255, 144, 0]
        Color dead:  [  0,   0, 0]
        Color fade:  [  0,   0, 0]

        This 3D Array gets scaled up using numpy be the cell size like so:

        Before:
        [[[127  72   0]  [255 144   0]]
         [[  0   0   0]  [124  70   0]]]

        After:
        [[[127  72   0]  [127  72   0]  [255 144   0]  [255 144   0]]
         [[127  72   0]  [127  72   0]  [255 144   0]  [255 144   0]]
         [[  0   0   0]  [  0   0   0]  [124  70   0]  [124  70   0]]
         [[  0   0   0]  [  0   0   0]  [124  70   0]  [124  70   0]]]

        The cell size in this example is 2 pixels, thus the array got
        scaled by a factor of 2 in both axis.
        """
        # Reset the background color
        self.dis.fill(self.color_background)

        # Get the slice of self.world.grid that is actually visible and has to be rendered.
        colors = self.world.grid[self.vis_north:self.vis_south, self.vis_west:self.vis_east]

        # Set fade colors using interpolation TODO: Is it faster to not interpolate 0s and 1s?
        colors = (self.color_fade + (self.color_alive - self.color_fade) * colors[:, :, numpy.newaxis]).clip(0, 255).astype(int)

        # Scale the array in both axis
        colors = numpy.repeat(numpy.repeat(colors, self.cell_size, axis=1), self.cell_size, axis=0)

        # Create a surface from the array
        sur = pygame.surfarray.make_surface(colors)

        # If the left or top border is not visible, the offset needs to be adjusted.
        if self.vis_north > 0:
            off_x = 0
        else:
            off_x = self.offset_x
        if self.vis_west > 0:
            off_y = 0
        else:
            off_y = self.offset_y
        # Blit the surface to the display
        self.dis.blit(sur, (off_x, off_y))

        # Update display
        pygame.display.flip()

    def center(self):
        """Updates offsets so that grid is centered.
        """
        self.offset_x = (self.res_width / 2) - (self.world.grid_width / 2 * self.cell_size)
        self.offset_y = (self.res_height / 2) - (self.world.grid_height / 2 * self.cell_size)

    def create_world(self, grid_width: int, grid_height: int, seed: int, load: bool, fr, fd):
        """Creates a new World Object.

        Parameters:
        :param int grid_width: Height of the Grid.
        :param int grid_height: Width of the Grid.
        :param int seed: Seed for the array generation. Default is random (-1).
        :param bool load: Boolean indicating whether the last game should be loaded.
        """
        if load:
            try:
                self.world = World(grid_width, grid_height, seed, fr, fd, self.load_grid())
            except Exception as e:
                print("Couldn't load file.", e)
                shutdown(pygame)
        else:
            self.world = World(grid_width, grid_height, seed, fr, fd)

        # Gets correct offsets to center the grid
        self.center()

        # Create the pygame surface in the correct size
        self.get_borders()

    def calc_generation(self):
        """Calculates and renders the cells.
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
        """Interpolates between two points.

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
            x = (steps[:, 0]-self.offset_x)//self.cell_size
            y = (steps[:, 1]-self.offset_y)//self.cell_size

            return x.astype(int), y.astype(int)
        else:
            # Calculate coordinates of normal cells
            x = (point1[0]-self.offset_x)//self.cell_size
            y = (point1[1]-self.offset_y)//self.cell_size

            return int(x), int(y)

    def game_loop(self, pause=False):
        """The main loop that runs the game.
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
                self.get_borders()

            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    shutdown(pygame)
                # Key events
                elif event.type == pygame.KEYDOWN:
                    # RETURN pressed: Pause game
                    if event.key == pygame.K_RETURN:
                        running = not running
                    # ESCAPE pressed: Close game
                    if event.key == pygame.K_ESCAPE:
                        shutdown(pygame)
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
                        self.world.load_from_csv(load_grid(self.save_file))
                        self.get_borders()
                    # S pressed: Save current game
                    if event.key == pygame.K_s:
                        save_grid(self.world.grid, self.save_file)
                    # C pressed: Center view
                    if event.key == pygame.K_c:
                        self.center()
                        self.get_borders()
                    # P pressed: Save screenshot
                    if event.key == pygame.K_p:
                        pygame.image.save(self.sur, f"{self.get_save_path() + str(self.world.generations)}.png")
                    # + pressed: Extend grid
                    if event.key == pygame.K_PLUS:
                        self.world.extend()
                        self.get_borders()
                    # - pressed: Reduce grid
                    if event.key == pygame.K_MINUS:
                        self.world.reduce()
                        self.get_borders()

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
                    if event.y == 1:
                        self.cell_size *= 2
                        self.offset_x = curr_pos[0] + (self.offset_x - curr_pos[0]) * 2
                        self.offset_y = curr_pos[1] + (self.offset_y - curr_pos[1]) * 2
                        self.get_borders()
                    elif event.y == -1 and self.cell_size > 1:
                        self.cell_size /= 2
                        self.offset_x = curr_pos[0] + (self.offset_x - curr_pos[0]) / 2
                        self.offset_y = curr_pos[1] + (self.offset_y - curr_pos[1]) / 2
                        self.get_borders()

            # Interpolate to prevent dotted line
            if draw and prev_pos != None:
                x, y = self.interpolate(prev_pos, curr_pos)
                if isinstance(x, int) and isinstance(y, int):
                    if 0 <= x < self.world.grid_width and 0 <= y < self.world.grid_height:
                        self.world.grid[x, y] = draw_color or (0.5 if self.world.grid[x, y] == 1.0 and not draw_color else self.world.grid[x, y])
                elif min(x) >= 0 and max(x) < self.world.grid_width and min(y) >= 0 and max(y) < self.world.grid_height:
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

        shutdown(pygame)
