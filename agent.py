import tkinter as tk
import random as rnd
from utils import clamp


class Agent:
    def __init__(self, x=0, y=0):
        self.coords = (x, y)
        self.energy = 20
        self.alive = True
        self.there_is_food = False
        self.max_energy = 20

    def place_random(self, size: tuple[int, int]) -> None:
        w, h = size
        self.coords = rnd.randint(0, w - 1), rnd.randint(0, h - 1)

    def step(self, size: tuple[int, int]) -> None:
        if self.there_is_food and self.energy < self.max_energy:
            self.eat()
        else:
            self.move(size)
        self.death()

    def compute_colour(self) -> str:
        if not self.alive:
            return "#600000"

        t = self.energy / self.max_energy
        t = max(0.0, min(t, 1.0))

        low_rgb = (16, 16, 64)
        high_rgb = (80, 180, 255)

        r = int(low_rgb[0] + t * (high_rgb[0] - low_rgb[0]))
        g = int(low_rgb[1] + t * (high_rgb[1] - low_rgb[1]))
        b = int(low_rgb[2] + t * (high_rgb[2] - low_rgb[2]))

        return f"#{r:02x}{g:02x}{b:02x}"

    def draw(self, canvas: tk.Canvas, cell_px: int) -> None:
        colour = self.compute_colour()
        cx = self.coords[0] * cell_px + cell_px // 2
        cy = self.coords[1] * cell_px + cell_px // 2
        r = cell_px // 6
        canvas.create_oval(
            cx - r, cy - r, cx + r, cy + r, fill=colour, outline="", tags="agent"
        )

    def eat(self) -> None:
        self.energy += 1

    def move(self, size: tuple[int, int]) -> None:
        self.energy -= 1
        w, h = size
        dx, dy = rnd.choice([(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)])
        x, y = self.coords
        self.coords = (clamp(x + dx, 0, w - 1), clamp(y + dy, 0, h - 1))

    def death(self):
        if self.energy <= 0:
            self.alive = False

    # ask world how much food there is in the current cell

    def is_there_food(self, food_amount: int) -> None:
        self.there_is_food = food_amount > 0
