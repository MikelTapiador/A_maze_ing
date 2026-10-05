
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
        seed: int | None = None
    ) -> None:
        self.width = width
        self.height = height
        self.random = random.Random(seed)

        self.grid = [
            [ALL_WALLS for _ in range(width)]
            for _ in range(height)
        ]

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

    def generate(self) -> None:
        visited = set()
        stack = []

        start = (0, 0)

        visited.add(start)
        stack.append(start)

        while stack:
            x, y = stack[-1]

            neighbors = self.get_neighbors(x, y)
            unvisited = []

            for nx, ny in neighbors:
                if (nx, ny) not in visited:
                    unvisited.append((nx, ny))

            if unvisited:
                nx, ny = self.random.choice(unvisited)

                self.remove_wall(x, y, nx, ny)
                visited.add((nx, ny))
                stack.append((nx, ny))

            else:
                stack.pop()



maze = MazeGenerator(4, 3, 42)

print("\nHEX:")

maze.generate()
for row in maze.grid:
    for cell in row:
        print(format(cell, "X"), end="")
    print()



print(99//2)

"ESTO ES UNA PRUEBA"
"PATATTAAAAAAA"



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
