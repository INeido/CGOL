"""
World
====
"""
import numpy


class World:
    """
    ### World

    Contains various functions to store and update a grid with Cells.

    Parameters:
    :param size_x: Height of the World.
    :param size_y: Width of the World.
    :param seed: Seed for the array generation. Default is random.
    :param rows: The 2D Array filled with random 0s and 1s with the last being settings.
    """

    def __init__(self, size_x: int, size_y: int, seed: int, rows=[]):
        self.size_x = size_x
        self.size_y = size_y
        self.seed = seed
        self.generations = 0

        # If 'rows' are empty, create new grid, else convert 'rows' to numpy array.
        self.create() if len(rows) == 0 else self.load_from_csv(rows)
        self.grid_backup_0 = numpy.copy(self.grid)
        self.backup()

    def create(self):
        """
        ### Create World

        Creates the World the game takes place in.
        """
        # If '-1' create a new random seed.
        if self.seed == -1:
            self.seed = numpy.random.randint(2**32 - 1)

        # Create a new BitGenerator with the seed.
        rng = numpy.random.default_rng(self.seed)

        self.grid = rng.choice([0, 1], size=(self.size_x, self.size_y))

    def load_from_csv(self, grid):
        """
        ### Load from CSV

        Loads data from CSV file.

        Parameters:
        :param grid: The 2D Array filled with random 0s and 1s with the last being settings.
        """
        self.grid = numpy.array(grid[:-2], dtype=int)
        self.seed = int(grid[-2][0])
        self.generations = int(grid[-1][0])

    def backup(self):
        """
        ### Backup

        Creates a shallow copy of the grid.
        """
        temp = numpy.copy(self.grid_backup_0)
        self.grid_backup_0 = numpy.copy(self.grid)
        self.grid_backup_1 = numpy.copy(temp)

    def check_stalemate(self):
        """
        ### Check Stalemate

        Compares the last backup with the current grid to see of it changed.

        Returns:
        Boolean: Is the backup the same as the current grid?
        """
        return numpy.array_equal(self.grid, self.grid_backup_0)

    def check_oscillators(self):
        """
        ### Compare Backup

        Compares the second last backup with the current grid to see of it changed. 

        Returns:
        Boolean: Is the second last backup the same as the current grid?
        """
        return numpy.array_equal(self.grid, self.grid_backup_1)

    def get_neighbours(self):
        """
        ### Get Neighbours in Toroidal Space

        Counts the number of alive neighbours of a cell inside a toroidal space. Neighbours off the edge will wrap around.

        Returns:
        2d Array: The number of neighbours of a cell.
        """
        # Create a new array the same size as 'grid'
        neighbours = numpy.zeros_like(self.grid)

        # Roll over every axis to get a new array with the number of neighbours
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if not dx and not dy:
                    continue
                neighbours += numpy.roll(numpy.roll(self.grid, dx, axis=0), dy, axis=1)

        return neighbours

    def apply_rules(self, neighbours):
        """
        ### Get State

        Determines the new state of each cell for the current tick.

        Parameters:
        :param neighbours: The number of neighbours for each cell.

        Returns:
        2d Array: New state of cells.
        """
        # Create a copy of the grid to store the next generation
        grid = numpy.copy(self.grid)

        # Find the indices of cells that are currently alive or dead
        alive = numpy.where(self.grid == 1)
        dead = numpy.where(self.grid == 0)

        # Apply the rules to all cells
        grid[alive] = numpy.where((neighbours[alive] == 2) | (neighbours[alive] == 3), 1, 0)
        grid[dead] = numpy.where(neighbours[dead] == 3, 1, 0)

        return grid

    def update(self):
        """
        ### Update World

        Updates the state of the cells in the world according to the rules of the Game of Life.
        """
        # Get neighbours
        neighbours = self.get_neighbours()

        # Apply rules
        self.grid = self.apply_rules(neighbours)
