from pydantic import ValidationError
from config_loader import config_load
from generator import MazeGenerator
from renderer import Renderer


def main() -> None:
    try:
        config = config_load()
        print(config)
        maze = MazeGenerator(10, 10, (0, 0), (1, 1), 42)
        maze.generate()
        print("\nHEX:")

        for row in maze.grid:
            for cell in row:
                print(format(cell, "X"), end="")
            print()

        renderer = Renderer(maze)
        renderer.draw()

    except ValidationError as e:
        for error in e.errors():
            field = str(error["loc"][0])
            message = error["msg"].replace("Value error, ", "")
            print(f"Error in '{field.upper()}': {message}")
        return
    except ValueError as e:
        print(e)
        return


if __name__ == "__main__":
    main()
