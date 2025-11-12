import tkinter as tk
import random as rnd


class Food:
    def __init__(self, width: int, height: int, max_food: int = 5):
        self.width = width
        self.height = height
        self.max_food = max_food

        # initialize empty food map
        self.foods: dict[tuple[int, int], int] = {
            (x, y): 0 for x in range(width) for y in range(height)
        }

    def randomize(self, low: int = 0, high: int = 3, p: float = 0.05) -> None:
        for x, y in self.foods:
            if rnd.random() < p:
                self.set_at(x, y, rnd.randint(low, min(high, self.max_food)))

    def amount_at(self, x: int, y: int) -> int:
        return self.foods.get((x, y), 0)

    def set_at(self, x: int, y: int, value: int) -> None:
        self.foods[(x, y)] = value

    def take_at(self, x: int, y: int, value: int) -> int:
        amount = self.amount_at(x, y)
        if amount < value:
            self.set_at(x, y, 0)
            return amount
        else:
            self.set_at(x, y, amount - value)
            return value

    def regrow_step(self, p: float = 0.05, delta: int = 1) -> None:
        for x, y in self.foods:
            if rnd.random() < p:
                self.set_at(x, y, self.amount_at(x, y) + delta)

    def draw(self, canvas: tk.Canvas, cell_px: int) -> None:
        for (x, y), amt in self.foods.items():
            if amt == 0:
                continue
            x0, y0 = x * cell_px + 1, y * cell_px + 1
            x1, y1 = (x + 1) * cell_px - 1, (y + 1) * cell_px - 1

            level = int(255 * amt / self.max_food)  # 0..255
            hexc = f"#{level:02x}{level:02x}{level:02x}"  # using hexc to represent "amount" of food in one cell, by intensity of the color

            canvas.create_rectangle(x0, y0, x1, y1, fill=hexc, outline="", tags="food")
