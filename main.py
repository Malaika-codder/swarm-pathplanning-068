import random

#initializing variables for MY ROLL NUMBER , GRID SIZE and OBSTACLE_PERCENTAGE
ROLL_NUMBER = 68
GRID_SIZE = 20
OBSTACLE_PERCENTAGE = 0.15

#total number of cells 20 * 20
total_cells = GRID_SIZE * GRID_SIZE

#generating obstacles 
num_obstacles = int(total_cells * OBSTACLE_PERCENTAGE)

obstacles = set()

while len(obstacles) < num_obstacles:

    row = random.randint(0, GRID_SIZE - 1)
    col = random.randint(0, GRID_SIZE - 1)

    obstacles.add((row, col))

#Generate Start points
while True:

    start = (
        random.randint(0, GRID_SIZE - 1),
        random.randint(0, GRID_SIZE - 1)
    )

    if start not in obstacles:
        break

#Generate Goal
while True:

    goal = (
        random.randint(0, GRID_SIZE - 1),
        random.randint(0, GRID_SIZE - 1)
    )

    if goal not in obstacles and goal != start:
        break

#Display Roll number
print("Seed:", ROLL_NUMBER)

#Display Grid Size
print("Grid Size:", GRID_SIZE, "x", GRID_SIZE)

#Display Obstacles
print("Number of Obstacles:", len(obstacles))

#Display Starting Point
print("Start Point:", start)

#Display Goal Point or end point
print("Goal Point:", goal)

#show the obstacles
print("\nObstacles:")
print(obstacles)