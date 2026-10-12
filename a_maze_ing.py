from pydantic import ValidationError
from MazeGen.config_loader import config_load, Config
from MazeGen.generator import MazeGenerator
from renderer import Renderer


def draw_menu(config: Config) -> str:
    # Guardar la posición del cursor
    print("\033[s", end="")
    print()
    print("-" * 32)
    print("A-MAZE-ING")
    print("-" * 32)
    if config.width < 9 or config.height < 7:
        print()
        print("*** Maze too small to display the 42 pattern ***")
    print()
    print("[R] Restart    [A] Animate   [F] Real Sociedad   [Q] Quit")
    print()

    option = input("Choose an option: ").strip().upper()
    return option


def clear_menu() -> None:
    print("\033[u", end="")
    print("\033[J", end="")


def main() -> None:
    try:
        animated = False
        colour = False
        while True:
            config = config_load()
            maze = MazeGenerator(config)
            maze.generate()

            solution_path = maze.solve()
            maze.write_output()
            renderer = Renderer(maze, solution_path)
            renderer.render(animated, colour)
            animated = False
            colour = False

            while True:
                option = draw_menu(config)

                if option == "R":
                    clear_menu()
                    break
                elif option == "Q":
                    return
                elif option == "A":
                    animated = True
                    clear_menu()
                    break
                elif option == "F":
                    colour = True
                    clear_menu()
                    break
                else:
                    clear_menu()
                    print()
                    print("Invalid option.")
                    input("Press Enter to continue...")
                    clear_menu()

    except ValidationError as e:
        for error in e.errors():
            loc = error["loc"]
            if loc:
                field = str(loc[0])
            else:
                field = "maze"
            message = error["msg"].replace("Value error, ", "")
            print()
            print(f"Error in '{field.upper()}': {message}")
            print()
        return

    except ValueError as e:
        print()
        print(e)
        print()
        return

    except KeyboardInterrupt:
        print()
        print("\n\nProgram interrupted. Goodbye!")
        print()
        return


if __name__ == "__main__":
    main()
