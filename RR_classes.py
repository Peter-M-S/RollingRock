from random import choice


class Rock(set):

    def __init__(self):
        super().__init__()
        self.footprint = {(0, 0)}

    def at_start(self, start: tuple[int, int]):
        self.footprint = {start}

    def move(self, direction: str) -> None:
        if len(self.footprint) == 1:  # rock upright
            x, y = list(self.footprint)[0]
            match direction:
                case "d":  # tilt to right (positive x)
                    self.footprint = {(x + 1, y), (x + 2, y)}
                case "a":  # tilt to left (negative x)
                    self.footprint = {(x - 1, y), (x - 2, y)}
                case "x":  # tilt to fwd (positive y)
                    self.footprint = {(x, y + 1), (x, y + 2)}
                case "w":  # tilt to right (positive x)
                    self.footprint = {(x, y - 1), (x, y - 2)}
                case _:
                    print("unknown direction")
        elif len(self.footprint) == 2:  # rock flat
            x0, y0 = list(self.footprint)[0]
            x1, y1 = list(self.footprint)[1]
            if x0 == x1:  # rock in y-axis
                match direction:
                    case "d":  # roll to right (positive x)
                        self.footprint = {(x0 + 1, y0), (x1 + 1, y1)}
                    case "a":  # roll to left (negative x)
                        self.footprint = {(x0 - 1, y0), (x1 - 1, y1)}
                    case "x":  # tilt to fwd (positive y)
                        self.footprint = {(x0, max(y0, y1) + 1)}
                    case "w":  # tilt to back (negative x)
                        self.footprint = {(x0, min(y0, y1) - 1)}
                    case _:
                        print("unknown direction")
            else:  # rock in x-axis
                match direction:
                    case "d":  # roll to right (positive x)
                        self.footprint = {(max(x0, x1) + 1, y0)}
                    case "a":  # roll to left (negative x)
                        self.footprint = {(min(x0, x1) - 1, y0)}
                    case "x":  # roll to fwd (positive y)
                        self.footprint = {(x0, y0 + 1), (x1, y1 + 1)}
                    case "w":  # roll back (negative x)
                        self.footprint = {(x0, y0 - 1), (x1, y1 - 1)}
                    case _:
                        print("unknown direction")
        else:
            print("false length of footprint")

    def undo(self, direction: str) -> None:
        opposites: dict = {"d": "a", "a": "d", "w": "x", "x": "w"}
        d = opposites[direction]
        self.move(d)

    def is_at_goal(self, grid) -> bool:
        # todo How to typehint a class that will follow?
        #  the following class will typehint this class in a function
        return len(self.footprint) == 1 and list(self.footprint)[0] == grid.goal

    def is_valid(self, grid) -> bool:
        return not (self.footprint - grid.positions)


class Grid:

    GRIDFIELD = u"\u25A2"
    # GRIDFIELD = "-"
    # GRIDFIELD = "#"

    @classmethod
    def generate_grid_file(cls, n: int, filename: str = "random_grid.txt") -> None:
        # randomly choose of "wadx" a string of length n
        # starting at 0,0 follow path and store footprint in grid
        # save grid to filename
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
                    line += cls.GRIDFIELD
            line += "\n"
            lines.append(line)

        with open(filename, "w") as f:
            f.writelines(lines)

        print(f"Grid with >={n} steps created and saved as {filename}.")
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

    def get_positions(self, filename: str) -> None:
        # x = columns, y = rows
        with open(filename, "r") as f:
            y = -1
            for line in f.readlines():
                y += 1
                x = -1
                for c in line:
                    x += 1
                    if c not in f"SG-#{self.GRIDFIELD}": continue
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
                    a += self.GRIDFIELD
                a += " "
            print(a)
        print()


if __name__ == '__main__':
    # test
    g = Grid()
    print(g.rows, g.cols)
    rock = Rock()
    rock.at_start(g.start)
    rock.move("d")
    print(rock.footprint)
    rock.undo("d")
    g.render(rock)

    Grid.generate_grid_file(20)
    g = Grid("random_grid.txt")
    g.render(rock)
