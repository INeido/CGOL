"""
World
====
"""
import numpy


class World:
    """World
    ====

    Contains various functions to store and update a grid with Cells.

    :param int gw: Width of the World.
    :param int gh: Height of the World.
    :param int se: Seed for the array generation. Default is random.
    :param float fr: Value a cell should loose per generation after death.
    :param float fd: Fade value a cell should start with after death.
    :param array rows: The 2D Array filled with random 0s and 1s with the last being settings.
    """

    def __init__(self, gw: int, gh: int, se: int, fr: float, fd: float, rows=[]):
        self.grid_width = gw
        self.grid_height = gh
        self.fade_rate = fr
        self.fade_dead = fd
        self.seed = numpy.random.randint(2**16 - 1) if se == -1 else se
        self.generations = 0

        # If 'rows' are empty, create new grid, else convert 'rows' to numpy array
        self.populate("seed") if len(rows) == 0 else self.load_from_csv(rows)
        self.grid_backup_0 = numpy.zeros_like(self.grid)
        self.grid_backup_1 = numpy.zeros_like(self.grid)

    def populate(self, mode: str) -> None:
        """Fill 'grid' with different values.

        :param bool mode: The mode based on which the array should be filled.
        """
        if mode == "seed":
            self.grid = numpy.random.default_rng(self.seed).choice([0.0, 1.0], size=(self.grid_width, self.grid_height), p=[0.75, 0.25])
        if mode == "random":
            self.grid = numpy.random.choice([0.0, 1.0], size=(self.grid_width, self.grid_height), p=[0.75, 0.25])
        elif mode == "alive":
            self.grid = numpy.ones((self.grid_width, self.grid_height), dtype=float)
        elif mode == "dead":
            self.grid = numpy.zeros((self.grid_width, self.grid_height), dtype=float)
        elif mode == "kill":
            self.grid[self.grid == 1.0] = self.fade_dead
        else:
            return False

    def load_list(self, grid) -> None:
        """Loads data a list

        :param list grid: The 2D List filled with 0s and 1s.
        """
        self.grid = numpy.array(grid, dtype=float)

    def backup(self) -> None:
        """Creates a shallow copy of the grid.
        """
        temp = numpy.copy(self.grid_backup_0)
        self.grid_backup_0 = numpy.copy(self.grid)
        self.grid_backup_1 = numpy.copy(temp)

    def check_stalemate(self) -> bool:
        """Compares the last backup with the current grid to see of it changed.

        :return: Is the backup the same as the current grid?
        :rtype: bool
        """
        return numpy.array_equal(self.grid, self.grid_backup_0)

    def check_oscillators(self) -> bool:
        """Compares the second last backup with the current grid to see of it changed.

        :return: Is the second last backup the same as the current grid?
        :rtype: bool
        """
        return numpy.array_equal(self.grid, self.grid_backup_1)

    def extend(self) -> None:
        """Extends grid in every direction by one row/column.
        """
        self.grid = numpy.pad(self.grid, pad_width=1, mode='constant', constant_values=0)
        self.grid_width += 2
        self.grid_height += 2

    def reduce(self) -> None:
        """Reduce the size of the grid by removing the outermost row and column on all sides.
        If the grid has a width or height less than 3, the function returns without modifying the grid.
        """
        if len(self.grid) < 3 or len(self.grid[0]) < 3:
            return
        self.grid = self.grid[1:-1, 1:-1]
        self.grid_width -= 2
        self.grid_height -= 2

    def change_neighbours_func(self, toroid: bool):
        if toroid:
            self.get_neighbors = self.get_neighbors_toroidal
        else:
            self.get_neighbors = self.get_neighbors_normal

    def change_rules_func(self, fade: bool):
        if fade:
            self.apply_rules = self.apply_rules_fade
        else:
            self.apply_rules = self.apply_rules_normal

    def get_neighbors_normal(self) -> numpy.array:
        """Gets the number of alive neighbors of a cell in normal space.
        It uses the numpy roll function to shift the values in the
        grid along the x and y axis, but pads the grid by one in every
        directio, to avoid wrapping around borders.
        The resulting shifted arrays are summed and returned as the
        number of neighbors for each cell.

        The faded values are clipped so that they become integers.

        self.grid:          clipped_grid:   padded_grid:
                                                [[0 0 0 0 0]
            [[1. 0.2 1. ]       [[1 0 1]         [0 1 0 1 0]
             [0. 1.  0.4]   ->   [0 1 0]   ->    [0 0 1 0 0]
             [1. 0.  1. ]]       [1 0 1]]        [0 1 0 1 0]
                                                 [0 0 0 0 0]]

        Afterwards the grid is rolled and the values, minus the
        borders, are added onto 'neighbors'.

        :return: An array with the count of alive neighbors for each cell.
        :rtype: numpy.array int
        """
        # Create a new array the same size as 'grid'
        neighbors = numpy.zeros_like(self.grid, dtype=int)

        # Convert faded values to zeros
        clipped_grid = numpy.where(self.grid < 1, 0, 1)

        # Add padding to the grid using numpy.pad
        padded_grid = numpy.pad(clipped_grid, pad_width=1, mode='constant', constant_values=0)

        # Roll over every axis to get a new array with the number of neighbors
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                # Don't roll if both directions are 0.
                if not dx and not dy:
                    continue
                neighbors += numpy.roll(numpy.roll(padded_grid, dx, axis=0), dy, axis=1)[1:-1, 1:-1]

        return neighbors

    def get_neighbors_toroidal(self) -> numpy.array:
        """Gets the number of alive neighbors of a cell in a toroidal space.
        It uses the numpy roll function to shift the values in the
        grid along the x and y axis.
        The resulting shifted arrays are summed and returned as the
        number of neighbors for each cell.

        The faded values are clipped so that they become integers.

        self.grid:          clipped_grid:
            [[1. 0.2 1. ]       [[1 0 1]
             [0. 1.  0.4]   ->   [0 1 0]
             [1. 0.  1. ]]       [1 0 1]]

        Afterwards the grid is rolled and added onto 'neighbors'.

        neighbors after the rolls:
        1.  [[1 0 0] -> 2.  [[1 0 0] -> 3.  [[1 1 1] ->
             [0 1 1]         [1 1 2]         [2 2 2]
             [0 1 1]]        [1 1 2]]        [2 2 2]]

        4.  [[1 2 2] ->                 5.  [[2 3 2] ->
             [3 2 2]          skip           [3 2 3]
             [2 3 3]]                        [3 4 3]]

        6.  [[2 4 3] -> 7.  [[3 4 4] -> 8.  [[4 5 4]
             [3 3 4]         [4 3 5]         [5 4 5]
             [4 4 3]]        [4 5 3]]        [4 5 4]]

        :return: An array with the count of alive neighbors for each cell.
        :rtype: numpy.array int
        """
        # Create a new array the same size as 'grid'
        neighbors = numpy.zeros_like(self.grid, dtype=int)

        # Convert faded values to zeros
        clipped_grid = numpy.where(self.grid < 1, 0, 1)

        # Roll over every axis to get a new array with the number of neighbors
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                # Dont roll if both directions are 0.
                if not dx and not dy:
                    continue
                neighbors += numpy.roll(numpy.roll(clipped_grid, dx, axis=0), dy, axis=1)

        return neighbors

    def apply_rules_normal(self, neighbors) -> numpy.array:
        """Determines the new state of each cell for the current tick using numpy.where()
            to avaid nested for loops.

            The standard rules of Conway's Game of Life apply. (B3/S23)

            :param numpy.array neighbors: The number of neighbors for each cell.
            :return: New state of cells.
            :rtype: numpy.array int
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

    def apply_rules_fade(self, neighbors) -> numpy.array:
        """Determines the new state of each cell for the current tick using the "fade" implementation
        and numpy.where() to avaid nested for loops.
        In this implementation, cell values are stored as floats:
            1.0 = alive
            < 1.0 || > 0.0 = fading
            0.0 = dead

        Still B3/S23 rules, but with varying states inbetween.

        For cells that are currently alive, the rules are applied as follows:
            If the number of neighbors is 2 or 3, the cell remains alive (value = 1.0).
            Otherwise, the cell is considered dead and its value is set to the "fade_dead" value.

        For cells that are currently dead, the rules are applied as follows:
            If the number of neighbors is 3, the cell becomes alive (value = 1.0).
            Otherwise, the cell's value is decreased by the "fade_rate" value.

        :param numpy.array neighbors: The number of neighbors for each cell.
        :return: New state of cells.
        :rtype: numpy.array float
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

    def update(self) -> None:
        """Updates the state of the cells in the world according to the rules of the Game of Life.
        """
        # Get neighbors
        neighbors = self.get_neighbors()

        # Apply rules
        self.grid = self.apply_rules(neighbors)
