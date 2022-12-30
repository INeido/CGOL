"""
Game
====
"""
from world import World
import pygame
import math
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
    :param c_b: Colour for background.
    :param cell_size: Size of a cell in pixel.
    :param tickrate: Number of times the game shall update in a second (FPS).
    :param save_file: Path of the in-/output file.
    :param pause_stalemate: Game pauses on a stalemate.
    :param pause_oscillators: Game pauses when only oscillators remain.
    """

    def __init__(self, res_h: int, res_w: int, c_a: tuple, c_d: tuple, c_b: tuple, cell_size: int, tickrate: int, save_file: str, pause_stalemate: bool, pause_oscillators: bool):
        self.res_h = res_h
        self.res_w = res_w
        self.c_a = c_a
        self.c_d = c_d
        self.c_b = c_b
        self.cell_size = cell_size
        self.tickrate = tickrate
        self.save_file = save_file
        self.pause_stalemate = pause_stalemate
        self.pause_oscillators = pause_oscillators

    def setup_pygame(self):
        """
        ### Setup Pygame

        Creates and configures pygame instance.
        """
        try:
            os.system("cls" if os.name in ("nt", "dos") else "clear")
        except:
            pass
        pygame.init()

        self.dis = pygame.display.set_mode((self.res_w, self.res_h), 0, 8)
        pygame.display.set_caption("CGOL", "hardware")
        self.clock = pygame.time.Clock()

    def draw(self):
        """
        ### Draw Game

        Draws the current World.
        """
        # Reset background to background color
        self.dis.fill(self.c_b)
        self.sur.fill(self.c_d)

        # Calculate range of cells to draw
        start_x = max(0, int(-self.offset_x / self.cell_size))
        end_x = min(self.world.size_y, self.world.size_y - int(self.offset_x / self.cell_size) - self.world.size_y - int(-self.res_w / self.cell_size))
        start_y = max(0, int(-self.offset_y / self.cell_size))
        end_y = min(self.world.size_x, self.world.size_x - int(self.offset_y / self.cell_size) - self.world.size_x - int(-self.res_h / self.cell_size))

        # Update surface with changed pixels
        for x in range(start_y, end_y):
            for y in range(start_x, end_x):
                # If the cell has changed state, draw it FIXME
                # if self.world.grid[x][y] != self.world.grid_backup_0[x][y]:
                if self.world.grid[x][y]:
                    pygame.draw.rect(self.sur, self.c_a, pygame.Rect(y*self.cell_size, x*self.cell_size, self.cell_size, self.cell_size))
                #    else:
                #        pygame.draw.rect(self.sur, self.c_d, pygame.Rect(y*self.cell_size, x*self.cell_size, self.cell_size, self.cell_size))

        # Draw surface in display
        self.dis.blit(self.sur, (self.offset_x, self.offset_y))
        # Update display
        pygame.display.flip()

    def update_surface(self):
        self.sur = pygame.Surface((self.world.size_y*self.cell_size, self.world.size_x*self.cell_size))

    def center(self):
        """
        ### Center

        Updates offsets so that grid is centered.
        """
        self.offset_x = (self.res_w / 2) - (self.world.size_y / 2 * self.cell_size)
        self.offset_y = (self.res_h / 2) - (self.world.size_x / 2 * self.cell_size)

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

        # Gets correct offsets to center the grid
        self.center()

        # Create the pygame surface in the correct size
        self.update_surface()

    def save_grid(self):
        """
        ### Save Grid

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
        """
        ### Load Grid

        Loads the Grid from a CSV file.

        Returns:
        array: Rows of the CSV
        """
        with open(self.save_file, "r") as csvfile:
            reader = csv.reader(csvfile)
            return [row for row in reader]

    def calc_generation(self):
        """
        ### Calc Generation

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
            self.save_grid()
            self.game_loop(pause=True)

        # Catch if the World stopped developing because only oscillators remain
        if self.pause_oscillators and self.world.check_oscillators():
            print("\nGame stopped. Reason: Only Oscillators remaining.")
            self.save_grid()
            self.game_loop(pause=True)

    def game_loop(self, pause=False):
        """
        ### Game Loop

        The main loop that runs the game.
        """
        # Flags
        is_looping = True
        running = not pause
        exit = False
        m_down = False
        prev_pos = None
        first_pos = 0

        while True:
            # Draw before we start updating the cells
            self.draw()

            # Save mouse position
            curr_pos = pygame.mouse.get_pos()

            # Screen drag
            if first_pos != 0:
                self.offset_x, self.offset_y = self.world.calc_offset(curr_pos, first_pos, oldoffset_x, oldoffset_y)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_looping = False
                    print("\nGame stopped. Reason: Pygame closed.")
                    break

                # Key events
                elif event.type == pygame.KEYDOWN:
                    # RETURN pressed: Pause game
                    if event.key == pygame.K_RETURN:
                        running = not running
                    # ESCAPE pressed: Close game
                    if event.key == pygame.K_ESCAPE:
                        is_looping = False
                        print("\nGame stopped. Reason: Pygame closed.")
                        break
                    # Right Arrow pressed: Forward one generation
                    if event.key == pygame.K_RIGHT:
                        self.calc_generation()
                    # R pressed: Reset game
                    if event.key == pygame.K_r:
                        self.world.create()
                    # L pressed: Load last saved game
                    if event.key == pygame.K_l:
                        self.world.load_from_csv(self.load_grid())
                    # S pressed: Save current game
                    if event.key == pygame.K_s:
                        self.save_grid()
                    # C pressed: Center view
                    if event.key == pygame.K_c:
                        self.center()
                    # + pressed: Extend grid
                    if event.key == pygame.K_PLUS:
                        self.world.extend()
                        self.update_surface()
                        self.center()
                    # - pressed: Reduce grid
                    if event.key == pygame.K_MINUS:
                        self.world.reduce()
                        self.update_surface()
                        self.center()

                # Mouse events
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Left/Right Click: Draw
                    if event.button == 1 or event.button == 3:
                        m_down = True
                        prev_pos = curr_pos
                    if event.button == 1:
                        dragval = 1
                    if event.button == 3:
                        dragval = 0
                    # Middle Mouse: Drag screen
                    if event.button == 2:
                        oldoffset_x = self.offset_x
                        oldoffset_y = self.offset_y
                        first_pos = curr_pos
                elif event.type == pygame.MOUSEBUTTONUP:
                    # Left/Right Click: Draw
                    if event.button == 1 or event.button == 3:
                        m_down = False
                    # Middle Mouse: Drag screen
                    if event.button == 2:
                        first_pos = 0

                # Zoom TODO: Figure out the offset calculation
                elif event.type == pygame.MOUSEWHEEL:
                    if event.y == 1 and self.cell_size*8 < self.res_h and self.cell_size*8 < self.res_w:
                        # (((mPressed.X - (canvas.Width / 2)) * Fractal.GetPixelScaler() / 2) + double.Parse(Settings.TextBox_OffsetX.Text)).ToString();
                        # (self.res_h / 2) - (self.world.size_y / 2 * self.cell_size)
                        # self.offset_x = ((curr_pos[0] - (self.res_w / 2)) * self.cell_size / 2) + self.offset_x
                        # print((curr_pos[0] - (self.res_w / 2)) * self.world.size_y / 2 * self.cell_size * 2.0 / self.res_w / self.cell_size)
                        # self.offset_x += (curr_pos[0] - (self.world.size_y / 2 * self.cell_size)) / 2
                        self.cell_size *= 2
                        offset_x = curr_pos[0] + (self.offset_x - curr_pos[0]) * 2
                        offset_y = curr_pos[1] + (self.offset_y - curr_pos[1]) * 2
                        self.update_surface()

                        # self.offset_y += ((self.world.size_x / 2 * self.cell_size) - curr_pos[1]) / 2

                    elif event.y == -1 and self.cell_size > 1:
                        # ((((canvas.Height / 2) - mPressed.Y) * Fractal.GetPixelScaler() / 2) + double.Parse(Settings.TextBox_OffsetY.Text)).ToString();
                        # self.offset_y = (((self.res_h / 2) - curr_pos[1]) * self.cell_size / 2) + self.offset_y
                        # self.offset_x += (curr_pos[0] - (self.res_w / 2)) * 2
                        # self.offset_y += ((self.res_h / 2) - curr_pos[1]) * 2
                        self.cell_size /= 2
                        offset_x = curr_pos[0] + (self.offset_x - curr_pos[0]) * 2
                        offset_y = curr_pos[1] + (self.offset_y - curr_pos[1]) * 2
                        self.update_surface()
                # print("mouse : ", ((curr_pos[0] - (self.world.size_y / 2 * self.cell_size))))
                # print("old offset: ", self.offset_x)
                # print("new offset: ", self.offset_x + (curr_pos[0] - ((self.res_h / 2) - (self.world.size_y / 2 * self.cell_size))) / 2)
                # print("")

            # Interpolate to prevent dotted line
            if m_down:
                dx = curr_pos[0] - prev_pos[0]
                dy = curr_pos[1] - prev_pos[1]
                distance = math.sqrt(dx**2 + dy**2)
                # Prevent out of bounds error
                try:
                    # Prevent division by zero
                    if distance >= 2:
                        num_points = int(distance / 2)
                        x_step = dx / num_points
                        y_step = dy / num_points
                        for i in range(num_points):
                            x = prev_pos[0] + x_step * i
                            y = prev_pos[1] + y_step * i
                            self.world.grid[int((y-self.offset_y)//self.cell_size)][int((x-self.offset_x)//self.cell_size)] = dragval
                    else:
                        self.world.grid[int((curr_pos[1]-self.offset_y)//self.cell_size)][int((curr_pos[0]-self.offset_x)//self.cell_size)] = dragval
                    prev_pos = curr_pos
                except:
                    pass

            # Break out of main loop
            if not is_looping:
                break

            # Pause game
            if not running or m_down:
                continue

            try:
                self.calc_generation()
            except (KeyboardInterrupt):
                print("\nGame stopped. Reason: KeyboardInterrupt.")
                break

            self.clock.tick(self.tickrate)

        # Save current World
        self.save_grid()

        self.shutdown()

    def shutdown(self):
        pygame.quit()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
