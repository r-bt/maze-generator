import svgwrite
from maze_generator import MazeGenerator


class MazeDrawer:
    def __init__(self, cell_size=20, wall_thickness=2, animate=False):
        self._cell_size = cell_size
        self._wall_thickness = wall_thickness

    def draw(self, maze: MazeGenerator, solution: list = [], paths: list = []):
        """
        Given a width, height, and list of passages between cells, draws the maze
        """
        width = maze._width
        height = maze._height
        passages = maze._passages

        dwg = svgwrite.Drawing("maze.svg", profile="tiny")

        # Draw the cells
        for x in range(width):
            for y in range(height):
                dwg.add(
                    dwg.rect(
                        (x * self._cell_size, y * self._cell_size),
                        (self._cell_size, self._cell_size),
                        fill="white",
                    )
                )

        # Draw the walls
        for x in range(width):
            for y in range(height):
                # Check if should draw the top wall
                if ((x, y - 1) not in passages[(x, y)]) and (
                    (x, y) not in passages[(x, y - 1)]
                ):
                    dwg.add(
                        dwg.rect(
                            (x * self._cell_size, y * self._cell_size),
                            (
                                self._cell_size + self._wall_thickness,
                                self._wall_thickness,
                            ),
                            fill="black",
                        )
                    )

                # Check if should draw left wall
                if ((x - 1, y) not in passages[(x, y)]) and (
                    (x, y) not in passages[(x - 1, y)]
                ):
                    dwg.add(
                        dwg.rect(
                            (x * self._cell_size, y * self._cell_size),
                            (
                                self._wall_thickness,
                                self._cell_size + self._wall_thickness,
                            ),
                            fill="black",
                        )
                    )

                # If at the edge draw wall
                if x == width - 1:
                    dwg.add(
                        dwg.rect(
                            ((x + 1) * self._cell_size, y * self._cell_size),
                            (
                                self._wall_thickness,
                                self._cell_size + self._wall_thickness,
                            ),
                            fill="black",
                        )
                    )

                if y == height - 1:
                    dwg.add(
                        dwg.rect(
                            (x * self._cell_size, (y + 1) * self._cell_size),
                            (
                                self._cell_size + self._wall_thickness,
                                self._wall_thickness,
                            ),
                            fill="black",
                        )
                    )

        if len(solution) > 0:
            for point in solution:
                dwg.add(
                    dwg.rect(
                        (
                            point[0] * self._cell_size + (self._cell_size / 4),
                            point[1] * self._cell_size + (self._cell_size / 4),
                        ),
                        (self._cell_size / 2, self._cell_size / 2),
                        fill="green",
                    )
                )

        if len(paths) > 0:
            for point in paths:
                dwg.add(
                    dwg.rect(
                        (
                            point[0] * self._cell_size + (self._cell_size / 4),
                            point[1] * self._cell_size + (self._cell_size / 4),
                        ),
                        (self._cell_size / 2, self._cell_size / 2),
                        fill="red",
                    )
                )

        dwg.save()
