from maze_generator import MazeGenerator
from maze_drawer import MazeDrawer
from maze_solver import MazeSolver
import json

width = 50
height = 24

text = "Richard"

maze = MazeGenerator(width, height, text)

solver = MazeSolver()

solution = solver.solve(maze, (0, 0), (49, 23))

f = open("letters.json", "r")
letters = json.load(f)
f.close()

drawer = MazeDrawer()

j = []

letter_offset = (int(width * 1 / 8), int(height * 1 / 4))

for char in text:
    for index, (x, y) in enumerate(letters[char]["path"]):
        # Mark the cell as part of the maze
        j.append(
            (
                x + letter_offset[0],
                y + letter_offset[1],
            )
        )

    # Increase the offset
    letter_offset = (
        letter_offset[0] + letters[char]["width"] + 1,
        letter_offset[1],
    )

if solution is None:
    print("None solution")

# drawer.draw(maze, j, maze.get_debug_points())
drawer.draw(maze, solution)
