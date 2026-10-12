from pydantic import ValidationError
from config_loader import config_load
from generator import MazeGenerator
from renderer import Renderer


def draw_menu() -> str:
    print()
    print("-" * 32)
    print("A-MAZE-ING")
    print("[R] Restart   [Q] Quit")

    option = input("Choose an option: ").strip().upper()
    return option


def main() -> None:
    try:
        config = config_load()
        while True:
            maze = MazeGenerator(config)
            maze.generate()
            print("\nHEX:")

            for row in maze.grid:
                for cell in row:
                    print(format(cell, "X"), end="")
                print()

            solution_path = maze.solve()
            print(solution_path)
            maze.write_output()
            renderer = Renderer(maze, solution_path)
            renderer.render()

            # Dibujar el menú abajo
            option = draw_menu()

            if option == "R":
                continue
            elif option == "Q":
                break
            else:
                print("Invalid option.")
                input("Press Enter to continue...")

    except ValidationError as e:
        for error in e.errors():
            loc = error["loc"]
            if loc:
                field = str(loc[0])
            else:
                field = "maze"
            message = error["msg"].replace("Value error, ", "")
            print(f"Error in '{field.upper()}': {message}")
        return

    except ValueError as e:
        print(e)
        return

    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Goodbye!")
        return

    except BaseException as e:
        print(e.__class__.__name__)


if __name__ == "__main__":
    main()
