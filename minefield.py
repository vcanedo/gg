import random

class Minefield:
    def __init__(self, size, num_mines):
        self.size = size
        self.num_mines = num_mines
        self.field = [[' ' for _ in range(size)] for _ in range(size)]
        self.mines = set()
        self._place_mines()

    def _place_mines(self):
        while len(self.mines) < self.num_mines:
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            if (x, y) not in self.mines:
                self.mines.add((x, y))
                self.field[x][y] = '*'

    def display(self):
        for row in self.field:
            print(' '.join(row))

    def reveal(self, x, y):
        if (x, y) in self.mines:
            print("Boom! You hit a mine!")
            return False
        else:
            self.field[x][y] = self._count_adjacent_mines(x, y)
            return True

    def _count_adjacent_mines(self, x, y):
        count = 0
        for i in range(max(0, x-1), min(self.size, x+2)):
            for j in range(max(0, y-1), min(self.size, y+2)):
                if (i, j) in self.mines:
                    count += 1
        return str(count)

def main():
    size = 5
    num_mines = 5
    game = Minefield(size, num_mines)
    game.display()

    while True:
        x, y = map(int, input("Enter coordinates to reveal (x y): ").split())
        if not game.reveal(x, y):
            break
        game.display()

if __name__ == "__main__":
    main()
