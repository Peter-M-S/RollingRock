from RR_classes import Grid, Rock


def get_direction() -> str:
    while True:
        direction: str = input("wadx: ").lower()
        if direction in "wadx": return direction
        print("input only w, a, d, or x for up, left, right or down!")


def get_option() -> str:
    while True:
        option: str = input("D.efault or R.andom or Q.uit? ").lower()
        if option in "drqs": return option
        print("input only d,r or q!")


def main(filename: str | None = None) -> None:
    if filename is None:
        filename = "default_grid.txt"
    grid = Grid(filename)
    rock = Rock()
    rock.to_position(grid.start)
    solution = grid.solve()

    grid.render(rock)
    while True:
        d = get_direction()
        rock.move(d)
        if not rock.is_valid(grid):
            print("Fallen off grid :-(")
            break
        grid.render(rock)
        if rock.is_at_goal(grid):
            print(f"Success in {len(rock.path)} steps: {rock.path}!")
            print(f"Ideal in {len(solution)} steps: {solution}!")
            print(f"{len(rock.path) - len(solution)} more steps than ideal.")
            break


if __name__ == '__main__':

    while True:
        match get_option():
            case "r":
                Grid.generate_grid_file(10,"random_grid.txt")
                main("random_grid.txt")
            case "d":
                main()
            case "s":
                grid = Grid("default_grid.txt")
                solution = grid.solve()
                print(solution)
            case _:
                break
