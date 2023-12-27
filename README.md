# Pathfinder Visualizer

This is a simple visualizer for pathfinding algorithms using Pygame. Follow the instructions below to use the application:

## Instructions:

1. **Initialization:**
    - Run the script (`pathfinder.py`) to launch the visualizer.
    - The grid represents the environment where pathfinding algorithms operate.
    - Press `Esc` to clear the grid.

2. **Setting Start and End Points:**
    - Left-click on a grid cell to make it the starting point (orange).
    - Right-click to clear a cell. If the cleared cell was the starting point, it will be reset.

3. **Creating Barriers:**
    - Left-click on a grid cell to create a barrier (black).
    - Barriers are obstacles that the pathfinding algorithm should navigate around.

4. **Running Algorithms:**
    - Press `A` to run the A* algorithm 
    - Press `D` to run a depth-first search algorithm 
    - Press `B` to run a breadth-first search algorithm 

5. **Visualization:**
    - The visualization will show the algorithm's progress, with different colors representing different states:
        - **Red:** Closed (visited) nodes.
        - **Green:** Open nodes.
        - **Purple:** Path from the start to the end.

This is a simple visualizer for pathfinding algorithms using Pygame. Follow the instructions below to use the application:
