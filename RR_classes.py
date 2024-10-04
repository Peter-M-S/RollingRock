from random import choice
from collections import deque
import time


class Rock(set):

    def __init__(self):
        super().__init__()
        self.footprint = {(0, 0)}
        self.path = ""

    def to_position(self, start: tuple[int, int]):
        self.footprint = {start}

    @property
    def is_up(self) -> bool:
        return len(self.footprint) == 1

    @property
    def is_in_x_axis(self) -> bool:
        if self.is_up: return False
        (x0, y0), (x1, y1) = self.footprint
        return x0 != x1

    @property
    def is_in_y_axis(self) -> bool:
        if self.is_up: return False
        (x0, y0), (x1, y1) = self.footprint
        return y0 != y1

    def move(self, direction: str) -> None:
        if self.is_up:  # rock upright
            (x, y), *_ = self.footprint
            match direction:
                case "d":  # tilt to right (positive x)
                    self.footprint = {(x + 1, y), (x + 2, y)}
                    self.path += "d"
                case "a":  # tilt to left (negative x)
                    self.footprint = {(x - 1, y), (x - 2, y)}
                    self.path += "a"
                case "x":  # tilt to fwd (positive y)
                    self.footprint = {(x, y + 1), (x, y + 2)}
                    self.path += "x"
                case "w":  # tilt to back (negative y)
                    self.footprint = {(x, y - 1), (x, y - 2)}
                    self.path += "w"
                case _:
                    print("unknown direction")

        elif len(self.footprint) == 2:  # rock flat
            (x0, y0), (x1, y1) = self.footprint
            if self.is_in_y_axis:  # rock in y-axis
                match direction:
                    case "d":  # roll to right (positive x)
                        self.footprint = {(x0 + 1, y0), (x1 + 1, y1)}
                        self.path += "d"
                    case "a":  # roll to left (negative x)
                        self.footprint = {(x0 - 1, y0), (x1 - 1, y1)}
                        self.path += "a"
                    case "x":  # tilt to fwd (positive y)
                        self.footprint = {(x0, max(y0, y1) + 1)}
                        self.path += "x"
                    case "w":  # tilt to back (negative y)
                        self.footprint = {(x0, min(y0, y1) - 1)}
                        self.path += "w"
                    case _:
                        print("unknown direction")
            else:  # rock in x-axis
                match direction:
                    case "d":  # roll to right (positive x)
                        self.footprint = {(max(x0, x1) + 1, y0)}
                        self.path += "d"
                    case "a":  # roll to left (negative x)
                        self.footprint = {(min(x0, x1) - 1, y0)}
                        self.path += "a"
                    case "x":  # roll to fwd (positive y)
                        self.footprint = {(x0, y0 + 1), (x1, y1 + 1)}
                        self.path += "x"
                    case "w":  # roll back (negative y)
                        self.footprint = {(x0, y0 - 1), (x1, y1 - 1)}
                        self.path += "w"
                    case _:
                        print("unknown direction")
        else:
            print("false length of footprint")

    def undo(self, direction: str) -> None:
        opposites: dict = {"d": "a", "a": "d", "w": "x", "x": "w"}
        d = opposites[direction]
        self.move(d)
        self.path = self.path[:-2]

    def is_at_goal(self, grid) -> bool:
        # todo How to typehint a class that will follow?
        #  the following class will typehint this class in a function
        return len(self.footprint) == 1 and list(self.footprint)[0] == grid.goal

    def is_valid(self, grid) -> bool:
        return not (self.footprint - grid.positions)


class Grid:
    GRID_FIELD = u"\u25A2"

    # GRID_FIELD = "-"
    # GRID_FIELD = "#"

    @classmethod
    def generate_grid_file(cls, n: int = None, filename: str = None) -> str:
        # randomly choose of "wadx" a string of length n
        # starting at 0,0 follow path and store footprint in grid
        # save grid to filename
        if n is None:
            n = choice(range(10, 21))
        rock = Rock()
        path = [choice("wadx") for _ in range(n)]
        grid = rock.footprint
        start = list(rock.footprint)[0]
        for d in path:
            rock.move(d)
            grid.update(rock.footprint)

        while len(rock.footprint) != 1 or list(rock.footprint)[0] == start:
            # ensure rock not flat on last position and is not on start
            d = choice("wdax")
            rock.move(d)
            grid.update(rock.footprint)
            path += d

        goal = list(rock.footprint)[0]

        xmin, xmax = min(x for x, _ in grid), max(x for x, _ in grid)
        ymin, ymax = min(y for _, y in grid), max(y for _, y in grid)
        cols = xmax - xmin + 1
        rows = ymax - ymin + 1
        lines = []
        for r in range(rows):
            line = ""
            for c in range(cols):
                x, y = c + xmin, r + ymin
                if (x, y) not in grid:
                    line += " "
                elif (x, y) == start:
                    line += "S"
                elif (x, y) == goal:
                    line += "G"
                else:
                    line += cls.GRID_FIELD
            line += "\n"
            lines.append(line)

        if filename is None:
            filename = f"random_grid_{int(time.time())}.txt"

        with open(filename, "w") as f:
            f.writelines(lines)

        return filename
        # print(f"Grid with >={n} steps created and saved as {filename}.")
        # print(f"Moves: {''.join(path)}")

    def __init__(self, filename: str = None):
        self.positions: set[tuple[int, int]] = set()
        self.start: tuple[int, int] = (0, 0)
        self.goal: tuple[int, int] = (0, 0)
        self.get_positions("default_grid.txt" if filename is None else filename)
        self.rows: int = 0
        self.cols: int = 0
        self.get_size()

    def get_size(self) -> None:
        for x, y in self.positions:
            self.cols = max(x, self.cols)
            self.rows = max(y, self.rows)
        self.cols += 1
        self.rows += 1

    def get_positions(self, filename: str) -> None:
        # x = columns, y = rows
        with open(filename, "r") as f:
            y = -1
            for line in f.readlines():
                y += 1
                x = -1
                for c in line:
                    x += 1
                    if c not in f"SG-#{self.GRID_FIELD}": continue
                    if c == "S":
                        self.start = (x, y)
                    if c == "G":
                        self.goal = (x, y)
                    self.positions.add((x, y))

    def render(self, rock: Rock) -> None:
        for y in range(self.rows + 1):
            a = ""
            for x in range(self.cols + 1):
                if (x, y) not in self.positions:
                    a += " "
                elif (x, y) in rock.footprint:
                    a += "R"
                elif (x, y) == self.start:
                    a += "S"
                elif (x, y) == self.goal:
                    a += "G"
                else:
                    a += self.GRID_FIELD
                a += " "
            print(a)
        print()

    def find_valid_moves(self, rock: Rock) -> list[tuple]:
        possibles: list = []
        for m in "wadx":
            rock.move(m)
            if rock.is_valid(self):
                possibles.append((m, rock.footprint))
            rock.undo(m)
        return possibles

    def solve(self) -> str:

        # find string of shortest "wadx" path
        # bfs, iter

        def bfs():
            rock = Rock()
            rock.to_position(self.start)

            queue = deque()  # list of state = (footprint, path) to check
            queue.append((rock.footprint, []))
            seen: set = set()  # tuples of footprints

            while queue:
                rock.footprint, path = queue.popleft()

                if tuple(rock.footprint) in seen: continue

                seen.add(tuple(rock.footprint))

                if rock.is_at_goal(self): return path

                possibles: list = self.find_valid_moves(rock)  # list of (wadx, footprint)
                for m, fp in possibles:
                    if tuple(fp) not in seen:
                        queue.append((fp, path + [m]))

        path = bfs()

        return "".join(path)


if __name__ == '__main__':
    # test
    g = Grid()
    print(g.rows, g.cols)
    rock = Rock()
    rock.to_position(g.start)
    rock.move("d")
    print(rock.footprint)
    print(rock.is_up, rock.is_in_x_axis, rock.is_in_y_axis)
    rock.undo("d")
    g.render(rock)

    Grid.generate_grid_file(20)
    g = Grid("default_grid.txt")
    g.render(rock)

    print(g.solve())
