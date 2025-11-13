import tkinter as tk
import random as rnd
from utils import clamp
from food import Food


class Agent:
    def __init__(self, x=0, y=0):
        self.coords = (x, y)
        self.energy = 10

    def place_random(self, size: tuple[int, int]) -> None:
        w, h = size
        self.coords = rnd.randint(0, w - 1), rnd.randint(0, h - 1)

    def step(self, size: tuple[int, int], food: Food) -> None:
        food_amount = food.amount_at(self.coords[0], self.coords[1])
        if food_amount > 0:
            self.eat(food)
        else:
            self.move(size)

    def draw(self, canvas: tk.Canvas, cell_px: int) -> None:
        cx = self.coords[0] * cell_px + cell_px // 2
        cy = self.coords[1] * cell_px + cell_px // 2
        r = cell_px // 6
        canvas.create_oval(
            cx - r, cy - r, cx + r, cy + r, fill="#100dc4", outline="", tags="agent"
        )

    def eat(self, food: Food) -> None:
        self.energy += 1
        food.take_at(self.coords[0], self.coords[1], 1)

    def move(self, size: tuple[int, int]) -> None:
        self.energy -= 1
        w, h = size
        dx, dy = rnd.choice([(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)])
        x, y = self.coords
        self.coords = (clamp(x + dx, 0, w - 1), clamp(y + dy, 0, h - 1))
