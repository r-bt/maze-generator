from maze_generator import MazeGenerator


class MazeSolver:
    def __init__(self) -> None:
        pass

    def solve(self, maze: MazeGenerator, start: tuple, end: tuple) -> None:
        """
        Solves the maze with BFS

        :param maze: Maze to solve
        :return: None
        """

        if start == end:
            return

        # Setup BFS variables

        stack = [start]
        visited = set([start])
        parents = {start: None}

        while stack:
            current = stack.pop(0)

            if current == end:
                path = []
                parent = parents[end]

                while parent is not None:
                    path.append(parent)
                    parent = parents[parent]

                return path[::-1]

            for neighbour in maze._passages[current]:
                if neighbour not in visited:
                    stack.append(neighbour)
                    visited.add(neighbour)

                    parents[neighbour] = current

        return None
