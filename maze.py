import numpy as np
import random
import svgwrite


class Maze:
    """
    True = passage
    """

    def __init__(self, width, height, animate=False):
        self._width = width
        self._height = height

        self._grid = np.zeros((height, width), dtype=bool)
        self._edges = set()  # Set of all walls which won't exist in the maze

        self.__generate(animate)
        self.__draw(waitKey=0)

    def __get_adjecent(self, x, y, in_maze=True):
        """
        Wrapper function for get_frontier and get_neighbours

        Returns adjecent cells to (x,y) and checks if they are in the maze or not

        :param x: x coordinate of the cell
        :param y: y coordinate of the cell
        :return: list of cells that are in the frontier
        """

        f = set()

        if x > 0 and self._grid[x - 1][y] == in_maze:
            f.add((x - 1, y))
        if x + 1 < self._width and self._grid[x + 1][y] == in_maze:
            f.add((x + 1, y))
        if y > 0 and self._grid[x][y - 1] == in_maze:
            f.add((x, y - 1))
        if y + 1 < self._height and self._grid[x][y + 1] == in_maze:
            f.add((x, y + 1))

        return f

    def __get_frontier(self, x, y):
        """
        Returns the frontier of a cell (x,y)

        :param x: x coordinate of the cell
        :param y: y coordinate of the cell
        :return: list of cells that are in the frontier
        """

        return self.__get_adjecent(x, y, False)

    def __get_neighbours(self, x, y):
        """
        Returns the neighbours of a cell (x,y)

        :param x: x coordinate of the cell
        :param y: y coordinate of the cell
        :return: list of cells that are in the frontier
        """

        return self.__get_adjecent(x, y, True)

    def __generate(self, animate=False):
        """
        Generate a maze using Randomized Prim's Algorithm

        Steps:
        1. Start with a grid full of walls.
        2. Pick a cell at random, mark it as part of the maze. Add the walls of the cell to the wall list.
        3. Get the frontier fs of (x,y) and add to set s of all frontier cells
        4. While there are walls in the list:
            4a. Pick a random cell (x,y) from s and remove it
            4b. Get neigbours n of (x,y)
            4c. Connect (x,y) with a random neighbour (nx, ny) from n
            4d. Add frontier of (x,y) to s
        """

        # Pick a random starting cell

        (x, y) = (np.random.randint(0, self._width), np.random.randint(0, self._height))

        # Mark it as part of the maze

        self._grid[x][y] = True

        # Add the walls of the cell to the wall list

        s = self.__get_frontier(x, y)

        # While there are walls in the list

        while len(s) > 0:
            # Pick a random cell from the set of frontier cells

            (x, y) = random.choice(list(s))

            # Remove it from the set

            s.remove((x, y))

            # Get the neighbours of the cell

            neighbours = self.__get_neighbours(x, y)

            # Connect the cell with a random neighbour

            (nx, ny) = random.choice(list(neighbours))

            self._grid[x][y] = True

            self._edges.add(((x, y), (nx, ny)))

            # Add the frontier of the cell to the set

            s = s.union(self.__get_frontier(x, y))

    def __draw(
        self,
        pass_colour=(255, 255, 255),
        wall_colour=(0, 0, 0),
        highlight=None,
        highlight_colour=(255, 0, 0),
        waitKey=1,
    ):
        """
        Converts maze to SVG

        :param pass_colour: colour of the passage
        :param wall_colour: colour of the wall
        :param highlight: cell to highlight
        :param highlight_colour: colour of the highlight
        :param waitKey: wait time between frames
        """

        cell_size = 20
        wall_thickness = 2

        dwg = svgwrite.Drawing("maze.svg", profile="tiny")

        # Draw the cells
        for x in range(self._width):
            for y in range(self._height):
                dwg.add(
                    dwg.rect(
                        (x * cell_size, y * cell_size),
                        (cell_size, cell_size),
                        fill="white",
                    )
                )

        # Draw the walls
        for x in range(self._width):
            for y in range(self._height):
                # Check if should draw the top wall
                if ((x, y), (x, y - 1)) not in self._edges and (
                    (x, y - 1),
                    (x, y),
                ) not in self._edges:
                    dwg.add(
                        dwg.rect(
                            (x * cell_size, y * cell_size),
                            (cell_size + wall_thickness, wall_thickness),
                            fill="black",
                        )
                    )

                # Check if should draw left wall
                if ((x, y), (x - 1, y)) not in self._edges and (
                    (x - 1, y),
                    (x, y),
                ) not in self._edges:
                    dwg.add(
                        dwg.rect(
                            (x * cell_size, y * cell_size),
                            (wall_thickness, cell_size + wall_thickness),
                            fill="black",
                        )
                    )

                # If at the edge draw wall
                if x == self._width - 1:
                    dwg.add(
                        dwg.rect(
                            ((x + 1) * cell_size, y * cell_size),
                            (wall_thickness, cell_size + wall_thickness),
                            fill="black",
                        )
                    )

                if y == self._height - 1:
                    dwg.add(
                        dwg.rect(
                            (x * cell_size, (y + 1) * cell_size),
                            (cell_size + wall_thickness, wall_thickness),
                            fill="black",
                        )
                    )

        dwg.save()


m = Maze(int(50), int(50), animate=False)

print(len(m._edges))
