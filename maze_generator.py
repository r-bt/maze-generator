import numpy as np
import random
from collections import defaultdict
import json


class MazeGenerator:
    """
    True = passage
    """

    CHAR_SPACING = 1

    def __init__(self, width, height, solution=None):
        self._width = width
        self._height = height

        self._grid = np.zeros((height, width), dtype=bool)

        self._passages = defaultdict(list)
        self.__frontier = set()

        f = open("letters.json", "r")
        self.__letters = json.load(f)
        f.close()

        self.__debug_points = set()

        self.__add_preset_solution(solution)
        self.__generate()

    def get_debug_points(self):
        return self.__debug_points

    def __get_adjecent(
        self,
        x,
        y,
        in_maze=True,
        directions={"left": True, "right": True, "up": True, "down": True},
    ):
        """
        Wrapper function for get_frontier and get_neighbours

        Returns adjecent cells to (x,y) and checks if they are in the maze or not

        :param x: x coordinate of the cell
        :param y: y coordinate of the cell
        :return: list of cells that are in the frontier
        """

        f = set()

        if x > 0 and self._grid[y][x - 1] == in_maze and directions["left"]:
            f.add((x - 1, y))
        if (
            x + 1 < self._width
            and self._grid[y][x + 1] == in_maze
            and directions["right"]
        ):
            f.add((x + 1, y))
        if y > 0 and self._grid[y - 1][x] == in_maze and directions["up"]:
            f.add((x, y - 1))
        if (
            y + 1 < self._height
            and self._grid[y + 1][x] == in_maze
            and directions["down"]
        ):
            f.add((x, y + 1))

        return f

    def __get_frontier(
        self, x, y, directions={"left": True, "right": True, "up": True, "down": True}
    ):
        """
        Returns the frontier of a cell (x,y)

        :param x: x coordinate of the cell
        :param y: y coordinate of the cell
        :return: list of cells that are in the frontier
        """

        return self.__get_adjecent(x, y, False, directions)

    def __get_neighbours(
        self, x, y, directions={"left": True, "right": True, "up": True, "down": True}
    ):
        """
        Returns the neighbours of a cell (x,y)

        :param x: x coordinate of the cell
        :param y: y coordinate of the cell
        :return: list of cells that are in the frontier
        """

        return self.__get_adjecent(x, y, True, directions)

    def _add_passage(self, coord1, coord2):
        self._passages[coord1].append(coord2)
        self._passages[coord2].append(coord1)

    def __allocate_path_from_points(self, points):
        """
        Allocate path from a list of points

        :param points: List of points
        :return: None
        """

        for index, (x, y) in enumerate(points):
            # Mark the cell as part of the maze
            self._grid[y][x] = True

            # If we are not at the end of the path connect the cell with the next cell
            if index < len(points) - 1:
                (next_x, next_y) = points[index + 1]

                self._add_passage(
                    (
                        x,
                        y,
                    ),
                    (
                        next_x,
                        next_y,
                    ),
                )

            # Add the frontier of the cell to the set
            self.__frontier = self.__frontier.union(self.__get_frontier(x, y))

            # Remove the cell from the frontier if it is present
            if (x, y) in self.__frontier:
                self.__frontier.remove((x, y))

    def __find_empty_path(self, start, end):
        if start == end:
            return

        # Setup BFS variables
        stack = [start]
        visited = set([start])
        parents = {start: None}

        while stack:
            current = stack.pop(0)  # 0 needed to pop first not last element

            if current == end:
                path = [end]
                parent = parents[end]

                while parent is not None:
                    path.append(parent)
                    parent = parents[parent]

                return path[::-1]

            # If point is in grid continue
            if current != start and self._grid[current[1]][current[0]]:
                continue

            # Don't let the current_x go further than the end_x
            if current[0] > end[0]:
                continue

            all_neighbours = self.__get_frontier(
                current[0],
                current[1],
            ).union(self.__get_neighbours(current[0], current[1]))

            for neighbour in random.sample(all_neighbours, len(all_neighbours)):
                if neighbour not in visited:
                    stack.append(neighbour)
                    visited.add(neighbour)

                    parents[neighbour] = current

        return None

    def __find_windy_path(self, start, end):
        if start == end:
            return

        # Setup BFS variables
        stack = [start]
        visited = set([start])
        parents = {start: None}

        while stack:
            current = stack.pop()

            if current == end:
                path = [end]
                parent = parents[end]

                while parent is not None:
                    path.append(parent)
                    parent = parents[parent]

                return path[::-1]

            # If point is in grid continue
            if current != start and self._grid[current[1]][current[0]]:
                continue

            # If the current point is further away in x direction than the end point then we want to ignore it
            if abs(current[0] - start[0]) > abs(end[0] - start[0]):
                continue

            all_neighbours = self.__get_frontier(
                current[0],
                current[1],
            ).union(self.__get_neighbours(current[0], current[1]))

            for neighbour in random.sample(all_neighbours, len(all_neighbours)):
                if neighbour not in visited:
                    stack.append(neighbour)
                    visited.add(neighbour)

                    parents[neighbour] = current

        return None

    def __add_preset_solution(self, solution):
        """
        Add a preset solution to the maze

        1. First we allocate paths for all the letters
        2. Then we connect the indivdual letters
        3. Then we connect start point with the start of the first letter
        4. Finally we connect the end of the last letter with the end point

        :param solution: A string which will be turned into the solution
        :return: None
        """

        # Allocate paths for all the letters
        inital_offset = (int(self._width * 1 / 8), int(self._height * 1 / 4))
        letter_offset = inital_offset

        # Store the previous ending point
        previous_ending_point = None

        for char in solution:
            # Allocate space for the character
            points = [
                (x + letter_offset[0], y + letter_offset[1])
                for (x, y) in self.__letters[char]["path"]
            ]
            self.__allocate_path_from_points(points)

            # Connect the start of this character with the end of the previous
            if previous_ending_point is not None:
                connecting_path = self.__find_empty_path(
                    previous_ending_point,
                    (
                        letter_offset[0] + self.__letters[char]["path"][0][0],
                        letter_offset[1] + self.__letters[char]["path"][0][1],
                    ),
                )

                if connecting_path is not None:
                    self.__allocate_path_from_points(connecting_path)
                    self.__debug_points = self.__debug_points.union(
                        connecting_path[1:-1]
                    )

            # Store the ending point
            previous_ending_point = (
                letter_offset[0] + self.__letters[char]["path"][-1][0],
                letter_offset[1] + self.__letters[char]["path"][-1][1],
            )

            # Update the offset
            letter_offset = (
                letter_offset[0] + self.__letters[char]["width"] + self.CHAR_SPACING,
                letter_offset[1],
            )

        # Connect the start of the first character with the start of the maze
        start = (
            inital_offset[0] + self.__letters[solution[0]]["path"][0][0],
            inital_offset[1] + self.__letters[solution[0]]["path"][0][1],
        )

        connecting_path = self.__find_windy_path((0, 0), start)

        if connecting_path is not None:
            self.__allocate_path_from_points(connecting_path)
            self.__debug_points = self.__debug_points.union(connecting_path[1:-1])

        # Connect the end of the last character with the end of the maze
        connecting_path = self.__find_windy_path(
            (self._width - 1, self._height - 1), previous_ending_point
        )

        if connecting_path is not None:
            self.__allocate_path_from_points(connecting_path)
            self.__debug_points = self.__debug_points.union(connecting_path[1:-1])

    def __generate(self):
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

        # If we already added the preset solution we don't need to pick a random starting cell
        if len(self.__frontier) == 0:
            # Pick a random starting cell

            (x, y) = (
                np.random.randint(0, self._width),
                np.random.randint(0, self._height),
            )

            # Mark it as part of the maze

            self._grid[y][x] = True

            # Add the walls of the cell to the wall list

            self.__frontier = self.__get_frontier(x, y)

        # While there are walls in the list

        while len(self.__frontier) > 0:
            # Pick a random cell from the set of frontier cells

            (x, y) = random.choice(list(self.__frontier))

            # Remove it from the set

            self.__frontier.remove((x, y))

            # Get the neighbours of the cell

            neighbours = self.__get_neighbours(x, y)

            # Connect the cell with a random neighbour

            (nx, ny) = random.choice(list(neighbours))

            self._grid[y][x] = True

            self._add_passage((x, y), (nx, ny))

            # Add the frontier of the cell to the set

            self.__frontier = self.__frontier.union(self.__get_frontier(x, y))
