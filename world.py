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
    :param toroidal: Boolean indicating whether the space is toroidal or not.
    :param grid: The 2D Array filled with random 0s and 1s.
    """

    def __init__(self, size_x: int, size_y: int, seed: int, toroidal: bool, rows=[]):
        self.size_x = size_x
        self.size_y = size_y
        self.seed = seed
        self.toroidal = toroidal
        self.generations = 0

        # If 'rows' are empty, create new grid, else convert 'rows' to numpy array.
        self.create() if len(rows) == 0 else self.load_from_csv(rows)
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
        """
        self.grid = numpy.array(grid[:-2], dtype=int)
        self.seed = int(grid[-2][0])
        self.generations = int(grid[-1][0])

    def backup(self):
        """
        ### Backup

        Creates a shallow copy of the grid.
        """
        self.grid_backup = numpy.copy(self.grid)

    def compare_backup(self):
        """
        ### Compare Backup

        Compares the last backup with the current grid.

        Returns:
        Boolean: Is the backup the same as the current grid?
        """
        return numpy.array_equal(self.grid, self.grid_backup)

    def get_neighbours(self, x: int, y: int):
        """
        ### Get Neighbours

        Counts the number of alive neighbours of a cell using a mask.

        Parameters:
        :param x: X-Coordinate of the cell.
        :param y: Y-Coordinate of the cell.

        Returns:
        Integer: The number of neighbours of the cell.
        """
        count, mask = 0, [[-1, 1],  [0, 1],  [1, 1],
                          [-1, 0],           [1, 0],
                          [-1, -1], [0, -1], [1, -1]]

        for i in mask:
            if (0 <= x + i[0] < len(self.grid)) and (0 <= y + i[1] < len(self.grid[0])):
                count += self.grid[x + i[0]][y + i[1]]
        return count

    def get_neighbours_toroidal(self, x: int, y: int):
        """
        ### Get Neighbours in Toroidal Space

        Counts the number of alive neighbours of a cell inside a toroidal space. Neighbours off the edge will wrap around.

        Parameters:
        :param x: X-Coordinate of the cell.
        :param y: Y-Coordinate of the cell.

        Returns:
        Integer: The number of neighbours of the cell.
        """
        count, mask = 0, [[-1, 1],  [0, 1],  [1, 1],
                          [-1, 0],           [1, 0],
                          [-1, -1], [0, -1], [1, -1]]

        for i in mask:
            # Check if X Coordinate is off the edge, if so wrap around.
            if x + i[0] > len(self.grid) - 1:
                x_coord = 0
            elif x + i[0] < 0:
                x_coord = len(self.grid) - 1
            else:
                x_coord = x + i[0]

            # Check if Y Coordinate is off the edge, if so wrap around.
            if y + i[1] > len(self.grid[0]) - 1:
                y_coord = 0
            elif y + i[1] < 0:
                y_coord = len(self.grid[0]) - 1
            else:
                y_coord = y + i[1]

            count += self.grid[x_coord][y_coord]
        return count

    def get_state(self, neighbours: int, x: int, y: int):
        """
        ### Get State

        Determines the new state of a cell for the current tick.

        Parameters:
        :param neighbours: The number of neighbours.
        :param x: X-Coordinate of the cell.
        :param y: Y-Coordinate of the cell.

        Returns:
        Integer: 0 for Dead, 1 for Alive.
        """
        if self.grid[x][y]:
            if neighbours in [2, 3]:
                return 1
            else:
                return 0
        else:
            if neighbours == 3:
                return 1
            else:
                return 0

    def update(self):
        """
        ### Update World

        Updates the state of the cells in the world according to the rules of the Game of Life.
        """
        if self.toroidal:
            get_neighbours_func = self.get_neighbours_toroidal
        else:
            get_neighbours_func = self.get_neighbours

        updated_world = numpy.empty_like(self.grid)

        # Loop through every cell to first get the count of the neighbours and then update the cell state.
        for x in range(len(self.grid)):
            for y in range(len(self.grid[0])):
                neighbours = get_neighbours_func(x, y)
                updated_world[x][y] = self.get_state(neighbours, x, y)

        self.grid = updated_world
