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
    rng = np.random.default_rng(seed)
    return rng.choice([0, 1], size=(size_x, size_y)), seed

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
        try:
            os.system("cls" if os.name in ('nt', 'dos') else "clear")
        except:
            pass

    for row in world:
        for cell in row:
            if cell == 0:
                print(" ", end=" ")
            else:
                print("■", end=" ")
        print()

def save(world, save_file:str, seed:int):
    """
    ### Save World
  
    Saves the World into a CSV file.

    Parameters:
    :param world: 2D Array of the World.
    :param save_file: Path of the output file.
    :param Seed: Seed value used to create World.
    """
    with open(save_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        for row in world:
            writer.writerow(row)
        writer.writerow([seed])

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

        # Last row is the seed.
        return np.array(rows[:-1], dtype=int), rows[-1][0]

def shutdown():
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)       

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
        save(world_prev, save_file, seed)
        print("Last tick saved into:", save_file)
    except Exception as e:
        print("Couldn't save file.", e)

    print("")
    print("Seed used: ", seed)
    print("Generations: ", generations)

    shutdown()      

def main():
    parser = argparse.ArgumentParser(prog = 'CGOL', description = "Conway's Game of Life")

    parser.add_argument('--size-x', '-x', dest='x', default=10, type=int, required=False, help='Height of the World.')
    parser.add_argument('--size-y', '-y', dest='y', default=10, type=int, required=False, help='Width of the World.')
    parser.add_argument('--tickrate', '-t', dest='tickrate', default=1, type=float, required=False, help='Number of times the game shall update in a second (FPS).')
    parser.add_argument('--seed', '-s', dest='seed', default=-1, type=int, required=False, help='Seed value used to create World.')
    parser.add_argument('--toroidal', '-o', dest='toroidal', default=False, type=bool, required=False, help='Boolean determining if the World should be in toroidal space.')
    parser.add_argument('--save-file', '-f', dest='save_file', default='./cgol.csv', type=str, required=False, help='Path of the in-/output file. (Should be .csv)')
    parser.add_argument('--load', '-l', dest='load', default=False, type=bool, required=False, help='Boolean determining if a previous save should be loaded.')
    
    args = parser.parse_args()

    # Get the World
    if args.load:
        try:
            world, seed = load(args.save_file)
        except Exception as e:
            print("Couldn't load file.", e)
            shutdown()
    else: 
        world, seed = init_world(args.x, args.y, args.seed)

    # Start Game
    game_loop(world, seed, args.tickrate, args.toroidal, args.save_file)

if __name__ == '__main__':
    main()