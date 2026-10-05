
import random


NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8

ALL_WALLS = NORTH | EAST | SOUTH | WEST


class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        seed: int | None = None
    ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.random = random.Random(seed)
        self.blocked: set[tuple[int, int]] = set()
        self.grid = [
            [ALL_WALLS for _ in range(width)]
            for _ in range(height)
        ]

    def _place_42_pattern(self) -> None:
        if self.width < 9 or self.height < 7:
            print("Maze too small to display the 42 pattern")
            return

        center_x = self.width // 2
        center_y = self.height // 2

        pattern = [
            (-3, -2), (-3, -1), (-3, 0),
            (-2, 0),
            (-1, 0), (-1, 1), (-1, 2),

            (1, -2), (2, -2), (3, -2),
            (3, -1),
            (1, 0), (2, 0), (3, 0),
            (1, 1),
            (1, 2), (2, 2), (3, 2),
        ]

        for dx, dy in pattern:
            x = center_x + dx
            y = center_y + dy

            self.blocked.add((x, y))

    def remove_wall(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int
    ) -> None:
        if x2 == x1 + 1 and y2 == y1:
            self.grid[y1][x1] &= ~EAST
            self.grid[y2][x2] &= ~WEST
        elif x2 == x1 and y2 == y1 + 1:
            self.grid[y1][x1] &= ~SOUTH
            self.grid[y2][x2] &= ~NORTH
        elif x2 == x1 - 1 and y2 == y1:
            self.grid[y1][x1] &= ~WEST
            self.grid[y2][x2] &= ~EAST
        elif x2 == x1 and y2 == y1 - 1:
            self.grid[y1][x1] &= ~NORTH
            self.grid[y2][x2] &= ~SOUTH

    def is_inside(self, x: int, y: int) -> bool:
        return (
            0 <= x < self.width
            and 0 <= y < self.height
        )

    def get_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        neighbors = []
        nx = x
        ny = y - 1

        if self.is_inside(nx, ny):
            neighbors.append((nx, ny))

        nx = x + 1
        ny = y

        if self.is_inside(nx, ny):
            neighbors.append((nx, ny))

        nx = x
        ny = y + 1

        if self.is_inside(nx, ny):
            neighbors.append((nx, ny))

        nx = x - 1
        ny = y

        if self.is_inside(nx, ny):
            neighbors.append((nx, ny))

        return neighbors

    def _open_border(self, position: tuple[int, int]) -> None:
        x, y = position

        if x == 0:
            self.grid[y][x] &= ~WEST
        elif x == self.width - 1:
            self.grid[y][x] &= ~EAST
        elif y == 0:
            self.grid[y][x] &= ~NORTH
        elif y == self.height - 1:
            self.grid[y][x] &= ~SOUTH

    def generate(self) -> None:
        self._place_42_pattern()

        self._open_border(self.entry)
        self._open_border(self.exit)

        visited: set[tuple[int, int]] = set()
        stack: list[tuple[int, int]] = []

        start = self.entry

        visited.add(start)
        stack.append(start)

        while stack:
            x, y = stack[-1]

            neighbors = self.get_neighbors(x, y)
            unvisited = []

            for nx, ny in neighbors:
                if (
                    (nx, ny) not in visited
                    and (nx, ny) not in self.blocked
                ):
                    unvisited.append((nx, ny))

            if unvisited:
                nx, ny = self.random.choice(unvisited)

                self.remove_wall(x, y, nx, ny)
                visited.add((nx, ny))
                stack.append((nx, ny))

            else:
                stack.pop()


maze = MazeGenerator(9, 7, 42)

print("\nHEX:")

maze.generate()
for row in maze.grid:
    for cell in row:
        print(format(cell, "X"), end="")
    print()


# print("ANTES:")
# for row in maze.grid:
#     print(row)

# maze.generate()

# print("\nDESPUÉS:")
# for row in maze.grid:
#     print(row)











# print(maze.grid)
# print(maze.grid[2][2])
# maze.grid[2][2] &= ~EAST
# print(maze.grid[2][2])

# maze.remove_wall(0, 0, 1, 0)

# print(maze.grid)
