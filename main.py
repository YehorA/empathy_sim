#!/usr/bin/env python3

import tkinter as tk
import random as rnd
from world import World
from stats_window import StatsWindow
from version import __verison__

GRID_W = 30
GRID_H = 16
CELL = 32
SEED = 42


def main() -> None:
    rnd.seed(SEED)

    root = tk.Tk()
    root.title(f"empathy_sim — {__verison__}")

    canvas = tk.Canvas(
        root,
        width=GRID_W * CELL,
        height=GRID_H * CELL,
        bg="#0f0f0f",
        highlightthickness=0,
    )
    canvas.pack()

    world = World(GRID_W, GRID_H, CELL, canvas)
    world.draw_grid()
    world.spawn()

    stats = StatsWindow(root)

    world.tick(root, stats)

    root.mainloop()


if __name__ == "__main__":
    main()
