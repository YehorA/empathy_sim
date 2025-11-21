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
        self.ate = False
        self.age = 0
        self.reproduction_cooldown = 10
        self.death_time = 0

    def place_random(self, size: tuple[int, int]) -> None:
        w, h = size
        self.coords = rnd.randint(0, w - 1), rnd.randint(0, h - 1)

    # additonal note, messy system, but if was "born" start with 10 energy and bigger reproduction_cooldown
    def place_on_coords(self, x, y, size: tuple[int, int]) -> None:
        w, h = size
        nx = clamp(x, 0, w - 1)
        ny = clamp(y, 0, h - 1)
        self.coords = (nx, ny)
        self.energy = 10
        self.reproduction_cooldown = 10

    def step(self, size: tuple[int, int], view: dict[tuple[int, int], int]) -> None:
        self.ate = False
        dx, dy = self.decide(view)

        if (dx, dy) == (0, 0):
            if self.energy < self.max_energy:
                self.eat()
        else:
            self.move(size, (dx, dy))
        self.age += 1
        self.reproduction_cooldown = max(0, self.reproduction_cooldown - 1)
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
        self.ate = True

    def move(self, size: tuple[int, int], direction: tuple[int, int]) -> None:
        self.energy -= 1
        w, h = size
        dx, dy = direction
        x, y = self.coords
        self.coords = (clamp(x + dx, 0, w - 1), clamp(y + dy, 0, h - 1))

    def death(self):
        if self.energy <= 0 or self.age > 200:
            self.alive = False

    # ask world how much food there is in the current cell

    # def is_there_food(self, food_amount: int) -> None:
    #     self.there_is_food = food_amount > 0

    # de cides direction to move to
    def decide(self, view: dict[tuple[int, int], int]):
        if view[0, 0] > 0 and self.energy < self.max_energy:
            return (0, 0)
        has_food: list[tuple[int, int]] = [
            (dx, dy) for (dx, dy), amt in view.items() if amt > 0
        ]
        if has_food:
            return rnd.choice(has_food)

        return rnd.choice([(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)])

    def is_ready_to_reproduce(self) -> bool:
        return self.alive and self.energy > 14 and self.reproduction_cooldown == 0

    def reproduce(self) -> None:
        self.energy -= 5
        self.reproduction_cooldown = 20
