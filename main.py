import random
import math


# --------------------------------------------------
# STAGE 2: GENERATE PROBLEM ENVIRONMENT
# --------------------------------------------------

# Initializing variables for my Roll Number, Grid Size
# and Obstacle Percentage
ROLL_NUMBER = 68
GRID_SIZE = 20
OBSTACLE_PERCENTAGE = 0.15


# Use my roll number as the random seed
random.seed(ROLL_NUMBER)


# Total number of cells = 20 * 20 = 400
total_cells = GRID_SIZE * GRID_SIZE


# Calculate number of obstacles
num_obstacles = int(total_cells * OBSTACLE_PERCENTAGE)


# Generate unique obstacles
obstacles = set()

while len(obstacles) < num_obstacles:

    row = random.randint(0, GRID_SIZE - 1)
    col = random.randint(0, GRID_SIZE - 1)

    obstacles.add((row, col))


# Generate Start Point
while True:

    start = (
        random.randint(0, GRID_SIZE - 1),
        random.randint(0, GRID_SIZE - 1)
    )

    # Start point must not be an obstacle
    if start not in obstacles:
        break


# Generate Goal Point
while True:

    goal = (
        random.randint(0, GRID_SIZE - 1),
        random.randint(0, GRID_SIZE - 1)
    )

    # Goal must not be an obstacle
    # and Goal must be different from Start
    if goal not in obstacles and goal != start:
        break


# Display generated problem
print("Seed:", ROLL_NUMBER)
print("Grid Size:", GRID_SIZE, "x", GRID_SIZE)
print("Number of Obstacles:", len(obstacles))
print("Start Point:", start)
print("Goal Point:", goal)

print("\nObstacles:")
print(obstacles)



# --------------------------------------------------
# STAGE 3: PSO INITIALIZATION
# --------------------------------------------------

# Initializing number of particles, waypoints and iterations
NUM_PARTICLES = 10
NUM_WAYPOINTS = 5
ITERATIONS = 30


# w  = inertia
# c1 = influence towards Personal Best
# c2 = influence towards Global Best
w = 0.6
c1 = 1.5
c2 = 1.5



# --------------------------------------------------
# CREATE PARTICLES AND VELOCITIES
# --------------------------------------------------

particles = []
velocities = []


# Create all particles
for _ in range(NUM_PARTICLES):

    particle = []
    velocity = []


    # Create waypoints for each particle
    for _ in range(NUM_WAYPOINTS):

        # Random row and column for waypoint
        row = random.uniform(0, GRID_SIZE - 1)
        col = random.uniform(0, GRID_SIZE - 1)

        particle.append([row, col])


        # Initially velocity is zero
        velocity.append([0.0, 0.0])


    particles.append(particle)
    velocities.append(velocity)



# --------------------------------------------------
# DISPLAY INITIAL PARTICLES
# --------------------------------------------------

print("\nPSO INITIALIZATION")

print("Number of Particles:", NUM_PARTICLES)
print("Waypoints per Particle:", NUM_WAYPOINTS)


for i in range(NUM_PARTICLES):

    print("\nParticle", i + 1)

    print("Start:", start)

    for j in range(NUM_WAYPOINTS):

        print(
            "Waypoint",
            j + 1,
            ":",
            particles[i][j]
        )

    print("Goal:", goal)



# --------------------------------------------------
# CALCULATE PATH COST
# --------------------------------------------------

# Calculate total distance of a particle's route
def calculate_path_cost(particle):

    # Complete path:
    # Start -> Waypoints -> Goal
    path = [start] + particle + [goal]

    total_distance = 0


    # Calculate distance between consecutive points
    for i in range(len(path) - 1):

        x1, y1 = path[i]
        x2, y2 = path[i + 1]


        # Euclidean Distance Formula
        distance = math.sqrt(
            (x2 - x1) ** 2
            +
            (y2 - y1) ** 2
        )


        # Add distance to total path distance
        total_distance += distance


    return total_distance



# --------------------------------------------------
# INITIALIZE PERSONAL BEST (PBEST)
# --------------------------------------------------

pbest_positions = []


# Initially each particle's current position
# is also its Personal Best position
for particle in particles:

    particle_copy = []

    for waypoint in particle:

        # Copy each waypoint
        particle_copy.append(waypoint[:])

    pbest_positions.append(particle_copy)



# Store Personal Best cost for each particle
pbest_costs = []


for particle in pbest_positions:

    cost = calculate_path_cost(particle)

    pbest_costs.append(cost)



# --------------------------------------------------
# INITIALIZE GLOBAL BEST (GBEST)
# --------------------------------------------------

# Find particle having minimum Personal Best cost
gbest_index = pbest_costs.index(
    min(pbest_costs)
)


# Copy Global Best particle position
gbest_position = []


for waypoint in pbest_positions[gbest_index]:

    gbest_position.append(
        waypoint[:]
    )


# Store Global Best cost
gbest_cost = pbest_costs[gbest_index]



# --------------------------------------------------
# DISPLAY INITIAL PBEST AND GBEST
# --------------------------------------------------

print("\nINITIAL PBEST COSTS")


for i in range(NUM_PARTICLES):

    print(
        "Particle",
        i + 1,
        "pbest cost:",
        pbest_costs[i]
    )



print("\nINITIAL GLOBAL BEST")

print(
    "Best Particle:",
    gbest_index + 1
)

print(
    "Global Best Cost:",
    gbest_cost
)



# --------------------------------------------------
# PSO OPTIMIZATION ALGORITHM
# --------------------------------------------------

for iteration in range(ITERATIONS):


    # Move every particle
    for i in range(NUM_PARTICLES):


        # Move every waypoint of the particle
        for j in range(NUM_WAYPOINTS):


            # Generate random PSO values
            r1 = random.random()
            r2 = random.random()



            # ------------------------------------------
            # UPDATE ROW VELOCITY
            # ------------------------------------------

            velocities[i][j][0] = (

                w * velocities[i][j][0]

                +

                c1 * r1 * (
                    pbest_positions[i][j][0]
                    -
                    particles[i][j][0]
                )

                +

                c2 * r2 * (
                    gbest_position[j][0]
                    -
                    particles[i][j][0]
                )
            )



            # ------------------------------------------
            # UPDATE COLUMN VELOCITY
            # ------------------------------------------

            velocities[i][j][1] = (

                w * velocities[i][j][1]

                +

                c1 * r1 * (
                    pbest_positions[i][j][1]
                    -
                    particles[i][j][1]
                )

                +

                c2 * r2 * (
                    gbest_position[j][1]
                    -
                    particles[i][j][1]
                )
            )



            # ------------------------------------------
            # UPDATE WAYPOINT POSITION
            # ------------------------------------------

            particles[i][j][0] += velocities[i][j][0]

            particles[i][j][1] += velocities[i][j][1]



            # ------------------------------------------
            # KEEP WAYPOINT INSIDE GRID
            # ------------------------------------------

            # Keep row between 0 and 19
            particles[i][j][0] = max(
                0,
                min(
                    GRID_SIZE - 1,
                    particles[i][j][0]
                )
            )


            # Keep column between 0 and 19
            particles[i][j][1] = max(
                0,
                min(
                    GRID_SIZE - 1,
                    particles[i][j][1]
                )
            )



        # ----------------------------------------------
        # UPDATE PERSONAL BEST
        # ----------------------------------------------

        # Calculate new cost after particle movement
        current_cost = calculate_path_cost(
            particles[i]
        )


        # If current path is better than old Personal Best
        if current_cost < pbest_costs[i]:

            # Update Personal Best cost
            pbest_costs[i] = current_cost


            # Update Personal Best position
            pbest_positions[i] = [

                waypoint[:]

                for waypoint in particles[i]
            ]



    # --------------------------------------------------
    # UPDATE GLOBAL BEST
    # --------------------------------------------------

    # Find best Personal Best after this iteration
    best_index = pbest_costs.index(
        min(pbest_costs)
    )


    # Update Global Best only if better
    if pbest_costs[best_index] < gbest_cost:

        gbest_cost = pbest_costs[best_index]


        gbest_position = [

            waypoint[:]

            for waypoint
            in pbest_positions[best_index]
        ]


        gbest_index = best_index



    # Display best cost after every iteration
    print(
        "Iteration",
        iteration + 1,
        "- Best Cost:",
        gbest_cost
    )



# --------------------------------------------------
# DISPLAY FINAL PSO RESULT
# --------------------------------------------------

print("\nFINAL PSO RESULT")

print("Best Particle:", gbest_index + 1)

print("Best Path Cost:", gbest_cost)


# --------------------------------------------------
# STORE COMPLETE BEST PATH
# --------------------------------------------------

# Start the path with the Start Point
best_path = [start]

# Add optimized waypoints
for waypoint in gbest_position:

    # Convert decimal PSO position into grid coordinates
    grid_row = round(waypoint[0])
    grid_col = round(waypoint[1])

    best_path.append((grid_row, grid_col))


# Add Goal Point at the end
best_path.append(goal)


# --------------------------------------------------
# DISPLAY COMPLETE BEST PATH
# --------------------------------------------------

print("\nBest Path:")

print(best_path)