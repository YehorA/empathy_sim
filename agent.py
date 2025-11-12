import tkinter as tk
import random as rnd
from utils import clamp


class Agent:
    def __init__(self):
        self.coords = (0, 0)

    def spawn_agent(self, GRID_W: int, GRID_H: int) -> None:
        self.coords = rnd.randint(0, GRID_W - 1), rnd.randint(0, GRID_H - 1)

    def step(self, GRID_W: int, GRID_H: int) -> None:
        dx, dy = rnd.choice([(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)])
        nx = clamp(self.coords[0] + dx, 0, GRID_W - 1)
        ny = clamp(self.coords[1] + dy, 0, GRID_H - 1)
        self.coords = (nx, ny)

    def draw_agent(self, canvas: tk.Canvas, CELL: int) -> None:
        cx = self.coords[0] * CELL + CELL // 2
        cy = self.coords[1] * CELL + CELL // 2
        r = CELL // 6
        canvas.create_oval(
            cx - r, cy - r, cx + r, cy + r, fill="#100dc4", outline="", tags="agent"
        )
