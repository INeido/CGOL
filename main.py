"""
CGOL
=====
A whack Conway's Game of Life implementation.
"""
import numpy as np
import argparse
import time
import csv
import sys
import os

def init_world(size_x:int, size_y:int, seed:int=-1):
    """
    ### Initiate World 
  
    Creates the World the game takes place in.
  
    Parameters:
    :param size_x: Height of the World.
    :param size_y: Width of the World.
    :param seed: Seed for the array generation. Default is random.
  
    Returns:
    2D Numpy Array: The 2D Array filled with random 0s and 1s.
    int: Seed value used to create World.
    """
    if seed == -1:
        seed = np.random.randint(2**32 - 1)
    np.random.seed(seed)
    return np.random.randint(0,2,(size_x, size_y)), seed

def get_neighbours(world, x:int, y:int):
    """
    ### Get Neighbours
  
    Counts the number of alive neighbours of a cell using a mask.
  
    Parameters:
    :param world: 2D Array of the World.
    :param x: X-Coordinate of the cell.
    :param y: Y-Coordinate of the cell.
  
    Returns:
    Integer: The number of neighbours of the cell.
    """
    count, mask = 0, [[-1, 1],  [0, 1],  [1, 1],
                      [-1, 0],           [1, 0],
                      [-1, -1], [0, -1], [1, -1]]

    for i in mask:
        if (0 <= x+i[0] < len(world)) and (0 <= y+i[1] < len(world[0])):
            count += world[x+i[0]][y+i[1]]
    return count

def get_neighbours_toroidal(world, x:int, y:int):
    """
    ### Get Neighbours in Toroidal Space
  
    Counts the number of alive neighbours of a cell inside a toroidal space. Neighbours off the edge will wrap around.
  
    Parameters:
    :param world: 2D Array of the World.
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
        if x+i[0] > len(world)-1:
            x_coord = 0
        elif x+i[0] < 0:
            x_coord = len(world)-1
        else:
            x_coord = x+i[0]

        # Check if Y Coordinate is off the edge, if so wrap around.
        if y+i[1] > len(world[0])-1:
            y_coord = 0
        elif y+i[1] < 0:
            y_coord = len(world[0])-1
        else:
            y_coord = y+i[1]

        count += world[x_coord][y_coord]
    return count

def get_state(world, neighbours:int, x:int, y:int):
    """
    ### Get State
  
    Determines the new state of a cell for the current tick.
    Rules:
    1. Any live cell with two or three live neighbours survives.
    2. Any dead cell with three live neighbours becomes a live cell.
    3. All other live cells die in the next generation. Similarly, all other dead cells stay dead.
  
    Parameters:
    :param world: 2D Array of the World.
    :param neighbours: The number of neighbours.
    :param x: X-Coordinate of the cell.
    :param y: Y-Coordinate of the cell.
  
    Returns:
    Integer: 0 for Dead, 1 for Alive.
    """
    if neighbours < 2 or neighbours > 3:
        return 0
    if world[x][y] == 0 and neighbours == 3:
        return 1
    return world[x][y]

def display(world, clear:bool=True):
    """
    ### Display
  
    Displays the World.

    Parameters:
    :param world: 2D Array of the World.
    :param clear: Defines if console should be cleared before outputting.
    """
    if clear:
        if os.name in ('nt', 'dos'):
            os.system('cls')
        os.system('clear')

    for row in world:
        for cell in row:
            if cell == 0:
                print(" ", end=" ")
            else:
                print("■", end=" ")
        print()

def save(world, save_file:str):
    """
    ### Save World
  
    Saves the World into a CSV file.

    Parameters:
    :param world: 2D Array of the World.
    :param save_file: Path of the output file.
    """
    with open(save_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        for row in world:
            writer.writerow(row)

def load(save_file:str):
    """
    ### Load World
  
    Loads the World from a CSV file.

    Parameters:
    :param save_file: Path of the input file.

    Returns:
    2D Numpy Array: The 2D Array filled with random 0s and 1s.
    int: Seed value used to create World.
    """
    with open(save_file, 'r') as csvfile:
        reader = csv.reader(csvfile)

        rows = [row for row in reader]

        return np.array(rows, dtype=int), None

def game_loop(world, seed:int, tickrate:float, toroidal:bool, save_file:str):
    """
    ### Game Loop
  
    The engine that runs the game indefinetly or until Keyboardinterrupt.
  
    Parameters:
    :param world: 2D Array of the World.
    :param seed: Seed value used to create World.
    :param tickrate: Number of times the game shall update in a second (FPS).
    :param toroidal: Boolean determining if the World should be in toroidal space.
    :param save_file: Path of the in-/output file.
    """
    generations = 0
    while(True):
        try:
            generations += 1
            # !!Shallow!! Copy is needed because we are updating 'world' in place and we want to save the last full World.
            world_prev = np.copy(world)

            # Display before we start updating the cells. 
            display(world)

            # Convert tickrate to seconds for sleep.
            time.sleep(1 / tickrate)

            # Loop through every cell to first get the count of the neighbours and then update the cell state.
            for x in range(len(world)):
                for y in range(len(world[0])):
                    if toroidal:
                        world[x][y] = get_state(world_prev, get_neighbours_toroidal(world_prev, x, y), x, y)
                    else:
                        world[x][y] = get_state(world_prev, get_neighbours(world_prev, x, y), x, y)

            # Catch if the World stopped developing because of a stalemate.
            if np.array_equal(world, world_prev):
                print("\nGame stopped. Reason: Stalemate.")
                break

        except (KeyboardInterrupt):
            print("\nGame stopped. Reason: KeyboardInterrupt.")
            break

    try:
        save(world_prev, save_file)
        print("Last tick saved into:", f"{os.getcwd()}/cgol.csv")
    except:
        print("Couldn't save file.")

    print("")
    print("Seed used: ", seed)
    print("Generations: ", generations)

    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)        

def main():
    parser = argparse.ArgumentParser(description="Conway's Game of Life")

    parser.add_argument('--size-x', dest='x', required=False)
    parser.add_argument('--size-y', dest='y', required=False)
    parser.add_argument('--tickrate', dest='tickrate', required=False)
    parser.add_argument('--seed', dest='seed', required=False)
    parser.add_argument('--toroidal', dest='toroidal', required=False)
    parser.add_argument('--save-file', dest='save_file', required=False)
    args = parser.parse_args()

    # Set the World Size
    x = 10
    if args.x:
        x = int(args.x)
    y = 10
    if args.y:
        y = int(args.y)

    # Set the Tickrate
    tickrate = 1
    if args.tickrate:
        tickrate = int(args.tickrate)

    # Set the World Seed ('-1' for random)
    seed = -1
    if args.seed:
        seed = int(args.seed)

    # Set the World Behaviour
    toroidal = False
    if args.toroidal:
        toroidal = bool(args.toroidal)

    # Set the save_file path
    save_file = './cgol.csv'
    if args.save_file:
        save_file = string(args.save_file)

    # Get the World
    if not os.path.exists('./cgol.csv'):
        print('File not found. Creating new World...')
        input('World created, press any key to start.')
        world, seed = init_world(x, y, seed)
    elif input('Load previous (L) or start New Game (N)? ').upper() == 'N':
        world, seed = init_world(x, y, seed)
    else:
        world, seed = load(save_file)

    # Start Game
    game_loop(world, seed, tickrate, toroidal, save_file)

if __name__ == '__main__':
    main()