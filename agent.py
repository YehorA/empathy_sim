import tkinter as tk
import random as rnd
from utils import clamp


class Agent:
    def __init__(self, x=0, y=0):
        self.coords = (x, y)

    def place_random(self, size: tuple[int, int]) -> None:
        w, h = size
        self.coords = rnd.randint(0, w - 1), rnd.randint(0, h - 1)

    def step(self, size: tuple[int, int]) -> None:
        w, h = size
        dx, dy = rnd.choice([(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)])
        x, y = self.coords
        self.coords = (clamp(x + dx, 0, w - 1), clamp(y + dy, 0, h - 1))

    def draw_agent(self, canvas: tk.Canvas, CELL: int) -> None:
        cx = self.coords[0] * CELL + CELL // 2
        cy = self.coords[1] * CELL + CELL // 2
        r = CELL // 6
        canvas.create_oval(
            cx - r, cy - r, cx + r, cy + r, fill="#100dc4", outline="", tags="agent"
        )
