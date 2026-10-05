from generator import MazeGenerator
from enum import Enum


class Ansi(str, Enum):
    ESC = '\033'
    CLEAR = ESC + '[2J'
    RED = ESC + '[31m'
    YELLOW = ESC + '[33m'
    GREEN = ESC + '[32m'
    BLUE = ESC + '[34m'
    PURPLE = ESC + '[35m'
    WHITE_FG = ESC + '[37m'
    RED_BG = ESC + '[41m'
    YELLOW_BG = ESC + '[43m'
    GREEN_BG = ESC + '[42m'
    BLUE_BG = ESC + '[44m'
    PURPLE_BG = ESC + '[45m'
    RESET = ESC + '[0m'


class Renderer:
    def __init__(self, maze: MazeGenerator) -> None:
        self.grid = maze.grid

    def draw(self) -> None:
        # Borrar pantalla
        print(Ansi.CLEAR.value, end="")
        # Imprimir grid
        for row in self.grid:
            print(Ansi.BLUE_BG.value)
            print(row)
            print(Ansi.RESET.value)

