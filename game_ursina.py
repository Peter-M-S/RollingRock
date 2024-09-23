import ursina as ur
import RR_classes


def cube_in_x() -> bool:
    return rock3D.x != int(rock3D.x)


def move_W() -> None:
    # print("W -z")
    rock2D.move("w")  # neg z
    if rock3D.y == ROCK2_Y:  # cube up
        rock3D.rotation_x += 90
        rock3D.y = ROCK1_Y
        rock3D.z -= 1.5
    elif cube_in_x():  # cube in x (pos_x = .5)
        rock3D.z -= 1
    else:  # cube in z
        rock3D.rotation_x += 90
        rock3D.y = ROCK2_Y
        rock3D.z -= 1.5
    if not rock2D.is_valid(grid2D):
        game_over()
    if rock2D.is_at_goal(grid2D):
        game_won()


def move_X() -> None:
    # print("X +z")
    rock2D.move("x")  # pos z
    if rock3D.y == ROCK2_Y:  # cube up
        rock3D.rotation_x += 90
        rock3D.y = ROCK1_Y
        rock3D.z += 1.5
    elif cube_in_x():  # cube in x (pos_x = .5)
        rock3D.z += 1
    else:  # cube in z
        rock3D.rotation_x += 90
        rock3D.y = ROCK2_Y
        rock3D.z += 1.5
    if not rock2D.is_valid(grid2D):
        game_over()
    if rock2D.is_at_goal(grid2D):
        game_won()

def move_A() -> None:
    # print("A -x")
    rock2D.move("a")  # neg x
    if rock3D.y == ROCK2_Y:  # cube up
        rock3D.rotation_z += 90
        rock3D.y = ROCK1_Y
        rock3D.x -= 1.5
    elif not cube_in_x():  # cube in z (pos_x = .0)
        rock3D.x -= 1
    else:  # cube in z
        rock3D.rotation_z += 90
        rock3D.y = ROCK2_Y
        rock3D.x -= 1.5
    if not rock2D.is_valid(grid2D):
        game_over()
    if rock2D.is_at_goal(grid2D):
        game_won()

def move_D() -> None:
    # print("D +x")
    rock2D.move("d")  # pos x
    if rock3D.y == ROCK2_Y:  # cube up
        rock3D.rotation_z += 90
        rock3D.y = ROCK1_Y
        rock3D.x += 1.5
    elif not cube_in_x():  # cube in z (pos_x = .0)
        rock3D.x += 1
    else:  # cube in z
        rock3D.rotation_z += 90
        rock3D.y = ROCK2_Y
        rock3D.x += 1.5
    if not rock2D.is_valid(grid2D):
        game_over()
    if rock2D.is_at_goal(grid2D):
        game_won()


def game_over():
    rock3D.color = ur.hsv(0, 10, 50)
    rock3D.animate("y", -4, duration=2)


def game_won():
    rock3D.color = ur.hsv(120, 100, 70)
    rock3D.animate("y", +4, duration=2)


grid2D = RR_classes.Grid()
rock2D = RR_classes.Rock()
rock2D.to_position(grid2D.start)
print(grid2D.start)

GAME_OVER = False
SIZE = 2 * max(grid2D.rows, grid2D.cols) + 1
ROCK1_Y, ROCK2_Y, TILE_Y = 0.5, 1, -0.1
ARROW_POSITIONS = {"X": (-2, TILE_Y, -1), "W": (-2, TILE_Y, -3), "D": (-1, TILE_Y, -2), "A": (-3, TILE_Y, -2)}

ROCK_COLOR = ur.hsv(60, 100, 80)
ARROW_COLOR = ur.hsv(0, 0, 100)
TILE_COLORS = (ur.hsv(120, 100, 50), ur.hsv(180, 100, 50), ur.hsv(240, 100, 50))  # start, field, goal

app = ur.Ursina()

(x, z), *_ = rock2D.footprint
rock3D = ur.Entity(model='cube', color=ROCK_COLOR, scale_y=2, collider='box', position=(x, ROCK2_Y, z))

tiles = []
for x, z in grid2D.positions:
    i = 1
    if (x, z) == grid2D.start: i = 0
    if (x, z) == grid2D.goal: i = 2
    tiles.append(ur.Entity(model='cube', color=TILE_COLORS[i], scale_y=0.2, collider='box',
                           position=(x, TILE_Y, z)))

arrows = dict()
for d in "DAXW":
    arrows[d] = ur.Entity(model='cube', color=ARROW_COLOR, scale_y=0.2, collider='box', position=ARROW_POSITIONS[d])

grid3D = ur.Entity(model=ur.Grid(SIZE, SIZE, thickness=1), position=(0, 0, 0))
grid3D.scale = SIZE
grid3D.rotation_x = -90

arrows["D"].on_click = move_D
arrows["A"].on_click = move_A
arrows["X"].on_click = move_X
arrows["W"].on_click = move_W

cam = ur.EditorCamera()  # add camera controls for orbiting and moving the camera

app.run()
