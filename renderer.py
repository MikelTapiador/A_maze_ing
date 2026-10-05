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


class Unicode(str, Enum):
    HORIZONTAL = "─"
    VERTICAL = "│"
    TOP_LEFT = "┌"
    TOP = "┬"
    TOP_RIGHT = "┐"
    LEFT = "├"
    CROSS = "┼"
    RIGHT = "┤"
    BOTTOM_LEFT = "└"
    BOTTOM = "┴"
    BOTTOM_RIGHT = "┘"


class Renderer:
    def __init__(self, maze: MazeGenerator) -> None:
        self.grid = maze.grid

    def _render_cell(self, cell: int, row_index: int, cell_index: int):
        # print(f"fila: {row_index} columna: {cell_index}")
        print(Ansi.GREEN_BG.value + str(cell) +
              ' ' + Ansi.RESET.value, end=""
              )

    def draw(self) -> None:
        # Borrar pantalla
        print(Ansi.CLEAR.value, end="")

        # Imprimir grid
        for row_index, row in enumerate(self.grid):
            for cell_index, cell in enumerate(row):
                self._render_cell(cell, row_index, cell_index)
            print()
