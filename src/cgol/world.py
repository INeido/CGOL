"""
World
====
"""
import numpy


class World:
    """World
    ====

    Contains various functions to store and update a grid with Cells.

    :param int size_x: Height of the World.
    :param int size_y: Width of the World.
    :param int seed: Seed for the array generation. Default is random.
    :param array rows: The 2D Array filled with random 0s and 1s with the last being settings.
    """

    def __init__(self, size_x: int, size_y: int, seed: int, fade_rate: float, fade_dead: float, rows=[]):
        self.size_x = size_x
        self.size_y = size_y
        self.fade_rate = fade_rate
        self.fade_dead = fade_dead
        self.seed = numpy.random.randint(2**32 - 1) if seed == -1 else seed
        self.generations = 0

        # If 'rows' are empty, create new grid, else convert 'rows' to numpy array.
        self.populate("seed") if len(rows) == 0 else self.load_from_csv(rows)
        self.grid_backup_0 = numpy.zeros_like(self.grid)
        self.grid_backup_1 = numpy.zeros_like(self.grid)

    def populate(self, mode: str, ):
        """Populate
        ====

        Fill 'grid' with different values.

        :param bool mode: The mode based on which the array should be filled.
        """
        if mode == "seed":
            self.grid = numpy.random.default_rng(self.seed).choice([0.0, 1.0], size=(self.size_x, self.size_y), p=[0.75, 0.25])
        if mode == "random":
            self.grid = numpy.random.choice([0.0, 1.0], size=(self.size_x, self.size_y), p=[0.75, 0.25])
        elif mode == "alive":
            self.grid = numpy.ones((self.size_x, self.size_y), dtype=float)
        elif mode == "dead":
            self.grid = numpy.zeros((self.size_x, self.size_y), dtype=float)
        elif mode == "kill":
            self.grid[self.grid == 1.0] = self.fade_dead
        else:
            return False

    def load_from_csv(self, grid):
        """Load from CSV
        ====

        Loads data from CSV file.

        :param array grid: The 2D Array filled with random 0s and 1s with the last being settings.
        """
        self.grid = numpy.array(grid[:-2], dtype=float)
        self.seed = int(grid[-2][0])
        self.generations = int(grid[-1][0])

    def backup(self):
        """Backup
        ====

        Creates a shallow copy of the grid.
        """
        temp = numpy.copy(self.grid_backup_0)
        self.grid_backup_0 = numpy.copy(self.grid)
        self.grid_backup_1 = numpy.copy(temp)

    def check_stalemate(self):
        """Check Stalemate
        ====

        Compares the last backup with the current grid to see of it changed.

        :return: Is the backup the same as the current grid?
        :rtype: bool
        """
        return numpy.array_equal(self.grid, self.grid_backup_0)

    def check_oscillators(self):
        """Compare Backup
        ====

        Compares the second last backup with the current grid to see of it changed.

        :return: Is the second last backup the same as the current grid?
        :rtype: bool
        """
        return numpy.array_equal(self.grid, self.grid_backup_1)

    def extend(self):
        """Extend
        ====

        Extends grid in every direction by one row/column.
        """
        self.grid = numpy.pad(self.grid, pad_width=1, mode='constant', constant_values=0)
        self.size_x += 2
        self.size_y += 2

    def reduce(self):
        """Reduce
        ====

        Reduces grid in every direction by one row/column.
        """
        if len(self.grid) < 3 or len(self.grid[0]) < 3:
            return
        self.grid = self.grid[1:-1, 1:-1]
        self.size_x -= 2
        self.size_y -= 2

    def get_neighbors(self):
        """Get Neighbours in Toroidal Space
        ====

        Counts the number of alive neighbors of a cell inside a toroidal space. Neighbours off the edge will wrap around.

        :return: The number of neighbors of a cell.
        :rtype: np.array int
        """
        # Create a new array the same size as 'grid'
        neighbors = numpy.zeros_like(self.grid)

        # Convert faded values to zeros
        clipped_grid = numpy.where(self.grid < 1, 0, 1)

        # Roll over every axis to get a new array with the number of neighbors
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if not dx and not dy:
                    continue
                neighbors += numpy.roll(numpy.roll(clipped_grid, dx, axis=0), dy, axis=1)

        return neighbors

        '''
        Potentially faster to bit shift? 1kx1k grid takes 0.01-0.02, just like numpy.roll

        # Shift grid left and right, and add to neighbors
        neighbors += numpy.bitwise_or(numpy.left_shift(clipped_grid, 1), numpy.right_shift(clipped_grid, 1))
        # Shift grid up and down, and add to neighbors
        neighbors += numpy.bitwise_or(numpy.left_shift(clipped_grid, self.grid.shape[0]), numpy.right_shift(clipped_grid, self.grid.shape[0]))
        # Shift grid diagonally and add to neighbors
        neighbors += numpy.bitwise_or(numpy.left_shift(clipped_grid, self.grid.shape[0]+1), numpy.right_shift(clipped_grid, self.grid.shape[0]+1))
        neighbors += numpy.bitwise_or(numpy.left_shift(clipped_grid, self.grid.shape[0]-1), numpy.right_shift(clipped_grid, self.grid.shape[0]-1))

        return neighbors
        '''

    def apply_rules_fade(self, neighbors):
        """Apply Rules
        ====

        Determines the new state of each cell for the current tick.

        Because of the fade implementation, the values are stored as floats.
        1.0 = alive
        < 1.0 || > 0.0 = dead and fading
        0.0 == dead

        :param np.array neighbors: The number of neighbors for each cell.

        :return: New state of cells.
        :rtype: np.array float
        """
        # Create a copy of the grid to store the next generation
        next_generation = numpy.copy(self.grid)

        # Find the indices of cells that are currently alive
        alive = numpy.where(self.grid == 1)

        # Find the indices of cells that are currently dead
        dead = numpy.where(self.grid < 1)

        # Apply the rules to cells that are currently alive
        next_generation[alive] = numpy.where((neighbors[alive] == 2) | (neighbors[alive] == 3), 1.0, self.fade_dead)

        # Apply the rule to cells that are currently dead
        next_generation[dead] = numpy.where(neighbors[dead] == 3, 1.0, self.grid[dead] - self.fade_rate)

        return numpy.where(next_generation < 0.00001, 0.0, next_generation)

    def apply_rules(self, neighbors):
        """Apply Rules
        ====

        Determines the new state of each cell for the current tick.

        :param np.array neighbors: The number of neighbors for each cell.

        :return: New state of cells.
        :rtype: np.array int
        """
        # Create a copy of the grid to store the next generation
        next_generation = numpy.copy(self.grid)

        # Find the indices of cells that are currently alive
        alive = numpy.where(self.grid == 1)

        # Find the indices of cells that are currently dead
        dead = numpy.where(self.grid == 0)

        # Apply the rules to cells that are currently alive
        next_generation[alive] = numpy.where((neighbors[alive] == 2) | (neighbors[alive] == 3), 1, 0)

        # Apply the rule to cells that are currently dead
        next_generation[dead] = numpy.where(neighbors[dead] == 3, 1, 0)

        return next_generation

    def update(self):
        """Update World
        ====

        Updates the state of the cells in the world according to the rules of the Game of Life.
        """
        # Get neighbors
        neighbors = self.get_neighbors()

        # Apply rules
        self.grid = self.apply_rules_fade(neighbors)
