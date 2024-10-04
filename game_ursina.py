import ursina as ur
import RR_classes

AX: dict = {
    'd': (0, 90, 1, 1.5, 0),
    'a': (0, 90, 1, -1.5, 0),
    'x': (0, 0, .5, 0, 1),
    'w': (0, 0, .5, 0, -1)
}
AZ: dict = {
    'd': (0, 0, .5, 1, 0),
    'a': (0, 0, .5, -1, 0),
    'x': (90, 0, 1, 0, 1.5),
    'w': (90, 0, 1, 0, -1.5)
}
AY: dict = {
    'd': (0, 90, .5, 1.5, 0),
    'a': (0, 90, .5, -1.5, 0),
    'x': (90, 0, .5, 0, 1.5),
    'w': (90, 0, .5, 0, -1.5)
}


def cube_in_x() -> bool:
    return rocks[0].x != int(rocks[0].x)


def move_W() -> None:
    move("w")


def move_X() -> None:
    move("x")


def move_A() -> None:
    move("a")


def move_D() -> None:
    move("d")


def move(d):
    rock2D[0].move(d)

    if rocks[0].y == RY2:  # cube up
        rx, rz, y, dx, dz = AY[d]
    elif cube_in_x():  # cube along x-axes
        rx, rz, y, dx, dz = AX[d]
    else:  # cube along z-axes
        rx, rz, y, dx, dz = AZ[d]
    rocks[0].rotation_x += rx
    rocks[0].rotation_z += rz
    rocks[0].y = y
    rocks[0].x += dx
    rocks[0].z += dz

    if not rock2D[0].is_valid(grid2D[0]):
        game_over()
    if rock2D[0].is_at_goal(grid2D[0]):
        game_won()


def game_over() -> None:
    rocks[0].color = ur.hsv(0, 10, 50)
    rocks[0].animate("y", -4, duration=2)


def game_won() -> None:
    rocks[0].color = ur.hsv(120, 100, 70)
    rocks[0].animate("y", +4, duration=2)


def clear_game() -> None:
    for t in tiles[:]:
        tiles.remove(t)
        ur.destroy(t)
    for r in rocks[:]:
        rocks.remove(r)
        ur.destroy(r)
    if grid2D: grid2D.pop()
    if rock2D: rock2D.pop()


def reset_game() -> None:
    clear_game()
    new_game(files[-1])


def new_game(filename: str = None) -> None:
    clear_game()
    if filename is None:
        filename = RR_classes.Grid.generate_grid_file()
        files.append(filename)
    grid2D.append(RR_classes.Grid(files[-1]))
    rock2D.append(RR_classes.Rock())
    rock2D[0].to_position(grid2D[0].start)
    (x, z), *_ = rock2D[0].footprint
    rocks.append(ur.Entity(model='cube', color=ROCK_COLOR, scale_y=2, collider='box', position=(x, RY2, z)))
    for x, z in grid2D[0].positions:
        i = 1
        if (x, z) == grid2D[0].start: i = 0
        if (x, z) == grid2D[0].goal: i = 2
        tiles.append(ur.Entity(model='cube', color=TILE_COLORS[i], scale_y=0.2, collider='box',
                               position=(x, TY, z)))


def quit_game() -> None:
    quit()


app = ur.Ursina()

SIZE = 13
RY1, RY2, TY = 0.5, 1, -0.1
BUTTON_POSITIONS = {"X": (-2, TY, -1), "W": (-2, TY, -3), "D": (-1, TY, -2), "A": (-3, TY, -2),
                    "N": (1, TY, -2), "R": (3, TY, -2), "Q": (5, TY, -2)}
BUTTON_TEXTURES = {
    "X": ("pfeil", 0),
    "W": ("pfeil", 180),
    "D": ("pfeil", 90),
    "A": ("pfeil", -90),
    "N": ("pfeil", 0),
    "R": ("reset", 0),
    "Q": ("quit", 0)
}

ROCK_COLOR = ur.hsv(60, 100, 80)
BUTTON_COLOR = ur.hsv(0, 0, 100)
TILE_COLORS = (ur.hsv(120, 100, 50), ur.hsv(180, 100, 50), ur.hsv(240, 100, 50))  # start, field, goal

files = ["default_grid.txt"]
grid2D = []
rock2D = []
rocks = []
tiles = []

buttons = dict()
for d in "DAXWRNQ":
    buttons[d] = ur.Entity(model="cube", color=BUTTON_COLOR, scale_y=0.2, collider='box',
                           position=BUTTON_POSITIONS[d],
                           texture=BUTTON_TEXTURES[d][0])
    buttons[d].y = -TY
    buttons[d].rotation_y = BUTTON_TEXTURES[d][1]

grid3D = ur.Entity(model=ur.Grid(SIZE, SIZE, thickness=1), position=(0, 0, 0))
grid3D.scale = SIZE
grid3D.rotation_x = -90

buttons["D"].on_click = move_D
buttons["A"].on_click = move_A
buttons["X"].on_click = move_X
buttons["W"].on_click = move_W
buttons["N"].on_click = new_game
buttons["R"].on_click = reset_game
buttons["Q"].on_click = quit_game

cam = ur.EditorCamera()  # add camera controls for orbiting and moving the camera
cam.position = 3, 4, -4
cam.rotation_y = -30
cam.rotation_x = 15

new_game("default_grid.txt")

app.run()
