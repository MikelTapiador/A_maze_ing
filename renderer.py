from MazeGen.generator import MazeGenerator
from enum import Enum
from time import sleep
import shutil


class Ansi(str, Enum):
    ESC = '\033'

    CLEAR = ESC + '[2J'
    CLEAR_SCROLLBACK = ESC + '[3J'
    ERASE_LINE = ESC + '[2K'
    ERASE_DOWN = ESC + '[J'

    HOME = ESC + '[H'
    CURSOR_POSITION = ESC + '[{};{}H'
    HIDE_CURSOR = ESC + "[?25l"
    SHOW_CURSOR = ESC + "[?25h"

    RED = ESC + '[31m'
    YELLOW = ESC + '[33m'
    GREEN = ESC + '[32m'
    BLUE = ESC + '[34m'
    PURPLE = ESC + '[35m'
    WHITE_FG = ESC + '[37m'
    BROWN = ESC + '[38;2;139;69;19m'

    RED_BG = ESC + '[41m'
    YELLOW_BG = ESC + '[43m'
    GREEN_BG = ESC + '[42m'
    BLUE_BG = ESC + '[44m'
    PURPLE_BG = ESC + '[45m'
    BROWN_BG = ESC + '[48;2;139;69;19m'

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
    SINGLE_DOWN = "╵"
    SINGLE_LEFT = "╶"
    SINGLE_UP = "╷"
    SINGLE_RIGHT = "╴"
    RABBIT = "\U0001F430"
    CARROT = "\U0001F955"


class Walls(int, Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8


class NeighborPos(str, Enum):
    NORTH = "north"
    EAST = "east"
    SOUTH = "south"
    WEST = "west"


class Renderer:
    CELL_WIDTH = 4
    CELL_HEIGHT = 2

    def __init__(self,
                 maze: MazeGenerator,
                 path: list[tuple[int, int]]) -> None:
        self.grid = maze.grid
        self.grid_width = maze.width
        self.grid_height = maze.height
        self.entry = maze.entry
        self.exit = maze.exit
        self.blocked = maze.blocked
        self.path = path

    def _create_canvas(self) -> list[list[str]]:
        drawing: list[list[str]] = []
        for _ in range(self.grid_height * self.CELL_HEIGHT + 1):
            row = []
            for _ in range(self.grid_width * self.CELL_WIDTH + 1):
                row.append(" ")
            drawing.append(row)
        return drawing

    def _get_cell_walls(self,
                        cell: int
                        ) -> dict[NeighborPos, bool]:
        drawing = {
            NeighborPos.NORTH: bool(cell & Walls.NORTH),
            NeighborPos.EAST: bool(cell & Walls.EAST),
            NeighborPos.SOUTH: bool(cell & Walls.SOUTH),
            NeighborPos.WEST: bool(cell & Walls.WEST),
        }
        return drawing

    def _draw_cell_walls(self,
                         row_index: int,
                         col_index: int,
                         drawing: dict[NeighborPos, bool],
                         draw_grid: list[list[str]]
                         ) -> None:
        top = row_index * self.CELL_HEIGHT
        left = col_index * self.CELL_WIDTH
        draw_grid[top][left] = "*"
        draw_grid[top][left + self.CELL_WIDTH] = "*"
        draw_grid[top + self.CELL_HEIGHT][left] = "*"
        draw_grid[top + self.CELL_HEIGHT][left + self.CELL_WIDTH] = "*"

        if drawing[NeighborPos.NORTH]:
            for position in range(1, self.CELL_WIDTH):
                draw_grid[top][left + position] = Unicode.HORIZONTAL.value
        if drawing[NeighborPos.SOUTH]:
            for position in range(1, self.CELL_WIDTH):
                draw_grid[top + self.CELL_HEIGHT][left + position] = (
                    Unicode.HORIZONTAL.value
                )
        if drawing[NeighborPos.EAST]:
            draw_grid[top + 1][left + self.CELL_WIDTH] = Unicode.VERTICAL.value
        if drawing[NeighborPos.WEST]:
            draw_grid[top + 1][left] = Unicode.VERTICAL.value

    def _draw_cell_corners(self, draw_grid: list[list[str]]) -> None:
        corners = {
            (False, False, False, False): " ",
            (True, False, False, False): Unicode.SINGLE_DOWN.value,
            (False, True, False, False): Unicode.SINGLE_LEFT.value,
            (False, False, True, False): Unicode.SINGLE_UP.value,
            (False, False, False, True): Unicode.SINGLE_RIGHT.value,
            (True, False, True, False): Unicode.VERTICAL.value,
            (False, True, False, True): Unicode.HORIZONTAL.value,
            (False, True, True, False): Unicode.TOP_LEFT.value,
            (False, False, True, True): Unicode.TOP_RIGHT.value,
            (True, True, False, False): Unicode.BOTTOM_LEFT.value,
            (True, False, False, True): Unicode.BOTTOM_RIGHT.value,
            (False, True, True, True): Unicode.TOP.value,
            (True, True, False, True): Unicode.BOTTOM.value,
            (True, True, True, False): Unicode.LEFT.value,
            (True, False, True, True): Unicode.RIGHT.value,
            (True, True, True, True): Unicode.CROSS.value,
        }

        for row_index in range(0, len(draw_grid), self.CELL_HEIGHT):
            for col_index in range(
                0, len(draw_grid[row_index]), self.CELL_WIDTH
            ):
                if draw_grid[row_index][col_index] != "*":
                    continue

                up = (
                    row_index > 0
                    and draw_grid[row_index - 1][col_index]
                    == Unicode.VERTICAL.value
                )
                right = (
                    col_index + 1 < len(draw_grid[row_index])
                    and draw_grid[row_index][col_index + 1]
                    == Unicode.HORIZONTAL.value
                )
                down = (
                    row_index + 1 < len(draw_grid)
                    and draw_grid[row_index + 1][col_index]
                    == Unicode.VERTICAL.value
                )
                left = (
                    col_index > 0
                    and draw_grid[row_index][col_index - 1]
                    == Unicode.HORIZONTAL.value
                )

                connections = (up, right, down, left)

                if connections in corners:
                    draw_grid[row_index][col_index] = corners[connections]

    def _draw_solution_path(
        self,
        path: list[tuple[int, int]],
        draw_grid: list[list[str]],
    ) -> None:
        arrows = {
            "E": "→",
            "W": "←",
            "S": "↓",
            "N": "↑",
        }
        for index, (col, row) in enumerate(path):
            top = row * self.CELL_HEIGHT
            left = col * self.CELL_WIDTH
            center = top + 1, left + (self.CELL_WIDTH // 2)

            if (col, row) == self.entry:
                draw_grid[center[0]][center[1]] = Unicode.RABBIT
            elif (col, row) == self.exit:
                draw_grid[center[0]][center[1]] = Unicode.CARROT
            else:
                next_col, next_row = path[index + 1]
                if next_col > col:
                    direction = "E"
                elif next_col < col:
                    direction = "W"
                elif next_row > row:
                    direction = "S"
                else:
                    direction = "N"
                char = arrows[direction]
                draw_grid[center[0]][center[1]] = (
                     Ansi.BROWN.value + char + Ansi.RESET.value
                 )

    def _draw_42_pattern(
                        self, draw_grid: list[list[str]], colour: bool
                        ) -> None:
        for x, y in self.blocked:
            top = y * self.CELL_HEIGHT
            left = x * self.CELL_WIDTH

            if not colour:
                for position in range(1, self.CELL_WIDTH):
                    draw_grid[top + 1][left + position] = (
                        Ansi.BROWN.value + "█" + Ansi.RESET.value
                    )
            if colour:
                for position in range(1, self.CELL_WIDTH):
                    draw_grid[top + 1][left + position] = (
                        Ansi.WHITE_FG.value + "█" + Ansi.RESET.value
                    )

    def _print_canvas(self, draw_grid: list[list[str]], colour: bool) -> None:

        for row in draw_grid:
            col_index = 0

            while col_index < len(row):
                col = row[col_index]
                if not colour:
                    color = Ansi.GREEN_BG.value + Ansi.WHITE_FG.value
                if colour:
                    color = Ansi.BLUE_BG.value + Ansi.WHITE_FG.value

                print(
                    f"{color}{col}{Ansi.RESET.value}",
                    end=""
                )

                if col in (Unicode.RABBIT, Unicode.CARROT):
                    col_index += 1

                col_index += 1

            print()

    def _wait_for_terminal_size(self) -> None:
        canvas_width = self.grid_width * self.CELL_WIDTH + 1
        canvas_height = self.grid_height * self.CELL_HEIGHT + 1

        while True:
            terminal_size = shutil.get_terminal_size()

            if (
                terminal_size.columns >= canvas_width
                and terminal_size.lines >= canvas_height
            ):
                break

            print(
                Ansi.HOME.value + Ansi.ERASE_DOWN.value,
                end="",
            )
            print(
                "Expand the terminal to view the maze.",
                flush=True,
            )
            sleep(0.1)

    def render(self, animated: bool, colour: bool, path: bool) -> None:
        self._wait_for_terminal_size()

        print(
            Ansi.CLEAR.value
            + Ansi.CLEAR_SCROLLBACK.value
            + Ansi.HOME.value,
            end="",
        )

        print(Ansi.HIDE_CURSOR.value, end="")

        try:
            draw_grid = self._create_canvas()

            for row_index, row in enumerate(self.grid):
                for col_index, cell in enumerate(row):
                    drawing = self._get_cell_walls(cell)

                    self._draw_cell_walls(
                        row_index,
                        col_index,
                        drawing,
                        draw_grid,
                    )

                    self._draw_cell_corners(draw_grid)

                    if animated:
                        print(Ansi.HOME.value, end="")

                        self._print_canvas(draw_grid, colour)

                        sleep(0.001)
            if path:
                self._draw_solution_path(self.path, draw_grid)

            self._draw_42_pattern(draw_grid, colour)

            print(Ansi.HOME.value, end="")
            self._print_canvas(draw_grid, colour)

        finally:
            print(Ansi.SHOW_CURSOR.value, end="")
