import random

class Maze:
    def __init__(self, width:int, height:int):
        self.height = height
        self.width = width
        self.poi1 = [0,0]
        self.poi2 = [0,0]
        self.poi3 = [0,0]
        self.poi4 = [0,0]
        self.poi5 = [0,0]
        self.poi6 = [0,0]
        self.poi7 = [0,0]
        self.arr = []
    
    def generate(self):
        height = int(self.height)
        width = int(self.width)
        cell = "c"
        wall = "w"

        # ------------------- initial functions

        # define empty maze
        def grid():
            maze = []
            for i in range(0, height):
                line = []
                for j in range(0, width):
                    line.append('u')
                maze.append(line)
            return maze

        def make_remaining_walls():
            for i in range(0, height):
                for j in range(0, width):
                    if maze[i][j] == "u":
                        maze[i][j] = "w"

        def clear_cells():
            for i in range(0, height):
                for j in range(0, width):
                    if maze[i][j] != "w":
                        maze[i][j] = "c"
        
        # ------------------- functions to be used IN MAIN CODE

        def surrounding_cells(wall):
            surround_cells = 0
            if maze[wall[0]-1][wall[1]] == "c":
                surround_cells += 1
            if maze[wall[0]+1][wall[1]] == "c":
                surround_cells += 1
            if maze[wall[0]][wall[1]-1] == "c":
                surround_cells += 1
            if maze[wall[0]][wall[1]+1] == "c":
                surround_cells += 1
            return surround_cells

        # pick somewhere in the maze to start the random generation
        start_height = int(random.random()*height)
        start_width = int(random.random()*width)

        # cannot start on edge of maze
        if start_height == 0:
            start_height += 1
        if start_width == 0:
            start_width += 1
        if start_height == height - 1:
            start_height -= 1
        if start_width == width - 1:
            start_width -= 1

        maze = grid()

        maze[start_height][start_width] = cell

        # add all walls to list of walls
        walls = []
        walls.append([start_height-1, start_width])
        walls.append([start_height, start_width-1])
        walls.append([start_height+1, start_width])
        walls.append([start_height, start_width+1])

        # denote blocks as walls
        maze[start_height-1][start_width] = wall
        maze[start_height+1][start_width] = wall
        maze[start_height][start_width-1] = wall
        maze[start_height][start_width+1] = wall

        while walls:
            # pick random wall
            rand_wall = walls[int(random.random()*len(walls))-1]

            # check blocks surrounding random wall; make sure all cells can be accessed

            # if left wall
            if rand_wall[1] != 0:
                if maze[rand_wall[0]][rand_wall[1]-1] == 'u' and maze[rand_wall[0]][rand_wall[1]+1] == 'c':
                    # get surrounding cells
                    surround_cells = surrounding_cells(rand_wall)

                    if surround_cells < 2:
                        # denote new path
                        maze[rand_wall[0]][rand_wall[1]] = "c"

                        # new walls
                        if rand_wall[0] != 0:
                            local_cell = maze[rand_wall[0]-1][rand_wall[1]]
                            if local_cell != "c":
                                maze[rand_wall[0]-1][rand_wall[1]] = "w"
                            if local_cell not in walls:
                                walls.append([rand_wall[0]-1, rand_wall[1]])
                        if rand_wall[0] != height-1:
                            local_cell = maze[rand_wall[0]+1][rand_wall[1]]
                            if local_cell != "c":
                                maze[rand_wall[0]+1][rand_wall[1]] = "w"
                            if local_cell not in walls:
                                walls.append([rand_wall[0]+1, rand_wall[1]])
                        if rand_wall[1] != 0:
                            local_cell = maze[rand_wall[0]][rand_wall[1]-1]
                            if local_cell != "c":
                                maze[rand_wall[0]][rand_wall[1]-1] = "w"
                            if local_cell not in walls:
                                walls.append([rand_wall[0], rand_wall[1]-1])
                    for wall in walls:
                        if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                            walls.remove(wall)

            # if up wall
            if rand_wall[0] != 0:
                if maze[rand_wall[0]-1][rand_wall[1]] == 'u' and maze[rand_wall[0]+1][rand_wall[1]] == 'c':
                    surround_cells = surrounding_cells(rand_wall)
                    if surround_cells < 2:
                        maze[rand_wall[0]][rand_wall[1]] = "c"

                        # upper
                        if rand_wall[0] != 0:
                            local_cell = maze[rand_wall[0]-1][rand_wall[1]]
                            if local_cell != "c":
                                maze[rand_wall[0]-1][rand_wall[1]] = "w"
                            if local_cell not in walls:
                                walls.append([rand_wall[0]-1, rand_wall[1]])
                        # left
                        if rand_wall[1] != 0:
                            local_cell = maze[rand_wall[0]][rand_wall[1]-1]
                            if local_cell != "c":
                                maze[rand_wall[0]][rand_wall[1]-1] = "w"
                            if local_cell not in walls:
                                walls.append([rand_wall[0], rand_wall[1]-1])
                        # right
                        if rand_wall[1] != width-1:
                            local_cell = maze[rand_wall[0]][rand_wall[1]+1]
                            if local_cell != "c":
                                maze[rand_wall[0]][rand_wall[1]+1] = "w"
                            if local_cell not in walls:
                                walls.append([rand_wall[0], rand_wall[1]+1])
                    for wall in walls:
                        if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                            walls.remove(wall)

            # if bottom wall
            if rand_wall[0] != height-1:
                if maze[rand_wall[0]+1][rand_wall[1]] == 'u' and maze[rand_wall[0]-1][rand_wall[1]] == 'c':
                    surround_cells = surrounding_cells(rand_wall)
                    if surround_cells < 2:
                        maze[rand_wall[0]][rand_wall[1]] = "c"

                        if rand_wall[0] != height-1:
                            local_cell = maze[rand_wall[0]+1][rand_wall[1]]
                            if local_cell != 'c':
                                maze[rand_wall[0]+1][rand_wall[1]] = 'w'
                            if local_cell not in walls:
                                walls.append([rand_wall[0]+1, rand_wall[1]])
                        if rand_wall[1] != 0:
                            local_cell = [rand_wall[0], rand_wall[1]-1]
                            if local_cell != 'c':
                                maze[rand_wall[0]][rand_wall[1]-1] = 'w'
                            if local_cell not in walls:
                                walls.append([rand_wall[0], rand_wall[1]-1])
                        if (rand_wall[1] != width-1):
                            local_cell = maze[rand_wall[0]][rand_wall[1]+1]
                            if local_cell != 'c':
                                maze[rand_wall[0]][rand_wall[1]+1] = 'w'
                            if local_cell not in walls:
                                walls.append([rand_wall[0], rand_wall[1]+1])
                    for wall in walls:
                        if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                            walls.remove(wall)

            # if right wall
            if rand_wall[1] != width-1:
                if maze[rand_wall[0]][rand_wall[1]+1] == 'u' and maze[rand_wall[0]][rand_wall[1]-1] == 'c':
                    surround_cells = surrounding_cells(rand_wall)
                    if surround_cells < 2:
                        maze[rand_wall[0]][rand_wall[1]] = "c"

                        if rand_wall[1] != width-1:
                            local_cell = maze[rand_wall[0]][rand_wall[1]+1]
                            if local_cell != 'c':
                                maze[rand_wall[0]][rand_wall[1]+1] = 'w'
                            if local_cell not in walls:
                                walls.append([rand_wall[0], rand_wall[1]+1])
                        if rand_wall[0] != height-1:
                            local_cell = maze[rand_wall[0]+1][rand_wall[1]]
                            if local_cell != 'c':
                                maze[rand_wall[0]+1][rand_wall[1]] = 'w'
                            if local_cell not in walls:
                                walls.append([rand_wall[0]+1, rand_wall[1]])
                        if rand_wall[0] != 0:
                            local_cell = maze[rand_wall[0]-1][rand_wall[1]]
                            if local_cell != 'c':
                                maze[rand_wall[0]-1][rand_wall[1]] = 'w'
                            if local_cell not in walls:
                                walls.append([rand_wall[0]-1, rand_wall[1]])
                    for wall in walls:
                        if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                            walls.remove(wall)

            for wall in walls:
                if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                    walls.remove(wall)

        make_remaining_walls()

        # pick 6 random locations for the POIs
        def placeitems():
            # this clear_cells function turns all i's back to c's so there aren't accidental duplicates
            clear_cells()
            for i in range(1,7):
                row = random.randint(2, width - 2)
                column = random.randint(2, height - 2)

                # this line prevents items from being next to each other
                if maze[row][column] == "i" or maze[row-1][column] == "i" or maze[row][column-1] == "i" or maze[row+1][column] == "i" or maze[row][column+1] == "i":
                    placeitems()

                # now do item placement
                if maze[row][column] == "c":
                    maze[row][column] = "i"
                    if i == 1:
                        self.poi1 = [row, column]
                    if i == 2:
                        self.poi2 = [row, column]
                    if i == 3:
                        self.poi3 = [row, column]
                    if i == 4:
                        self.poi4 = [row, column]
                    if i == 5:
                        self.poi5 = [row, column]
                    if i == 6:
                        self.poi6 = [row, column]
                elif maze[row-1][column] == "c":
                    maze[row-1][column] = "i"
                    if i == 1:
                        self.poi1 = [row-1, column]
                    if i == 2:
                        self.poi2 = [row-1, column]
                    if i == 3:
                        self.poi3 = [row-1, column]
                    if i == 4:
                        self.poi4 = [row-1, column]
                    if i == 5:
                        self.poi5 = [row-1, column]
                    if i == 6:
                        self.poi6 = [row-1, column]
                elif maze[row][column-1] == "c":
                    maze[row][column-1] = "i"
                    if i == 1:
                        self.poi1 = [row, column-1]
                    if i == 2:
                        self.poi2 = [row, column-1]
                    if i == 3:
                        self.poi3 = [row, column-1]
                    if i == 4:
                        self.poi4 = [row, column-1]
                    if i == 5:
                        self.poi5 = [row, column-1]
                    if i == 6:
                        self.poi6 = [row, column-1]
                elif maze[row+1][column] == "c":
                    maze[row+1][column] = "i"
                    if i == 1:
                        self.poi1 = [row+1, column]
                    if i == 2:
                        self.poi2 = [row+1, column]
                    if i == 3:
                        self.poi3 = [row+1, column]
                    if i == 4:
                        self.poi4 = [row+1, column]
                    if i == 5:
                        self.poi5 = [row+1, column]
                    if i == 6:
                        self.poi6 = [row+1, column]
                elif maze[row][column+1] == "c":
                    maze[row][column+1] = "i"
                    if i == 1:
                        self.poi1 = [row, column+1]
                    if i == 2:
                        self.poi2 = [row, column+1]
                    if i == 3:
                        self.poi3 = [row, column+1]
                    if i == 4:
                        self.poi4 = [row, column+1]
                    if i == 5:
                        self.poi5 = [row, column+1]
                    if i == 6:
                        self.poi6 = [row, column+1]
                # if no item was placed, call function again?
                else:
                    placeitems()

        placeitems()

        # make entrance and exit
        for i in range(0, width):
            if maze[1][i] == "c":
                maze[1][i] = "en"
                break
        for i in range(width-1, 0, -1):
            if maze[height-2][i] == "c":
                maze[height-2][i] = "ex"
                break
        # set self.arr equal to the generated maze
        self.arr = maze

    def print_maze(self):
        height = self.height
        width = self.width
        for i in range(0, height):
            for j in range(0, width):
                if self.maze[i][j] == 'u':
                    print("u", end="")
                elif self.maze[i][j] == 'c':
                    print("*", end="")
                elif self.maze[i][j] == 'i':
                    print("0", end="")
                else:
                    print("x", end="")
            print('\n')

    def __str__(self):
        return f'{len(self.arr[0])}x{len(self.arr)} populated maze.'