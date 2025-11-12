#!/usr/bin/env python3

import tkinter as tk
import random as rnd
from food import Food

GRID_W = 20
GRID_H = 12
CELL = 32
SEED = 42

agents: list[tuple[int, int]] = []


def draw_grid(canvas: tk.Canvas) -> None:
    for i in range(GRID_W + 1):
        X = i * CELL
        canvas.create_line(X, 0, X, GRID_H * CELL, fill="#333", tags="grid")
    for i in range(GRID_H + 1):
        Y = i * CELL
        canvas.create_line(0, Y, GRID_W * CELL, Y, fill="#333", tags="grid")


def spawn_agents(n: int) -> None:
    for i in range(n):
        agents.append((rnd.randint(0, GRID_W - 1), rnd.randint(0, GRID_H - 1)))


def draw_agents(canvas: tk.Canvas) -> None:
    for x, y in agents:
        cx = x * CELL + CELL // 2
        cy = y * CELL + CELL // 2
        r = CELL // 6
        canvas.create_oval(
            cx - r, cy - r, cx + r, cy + r, fill="#100dc4", outline="", tags="agent"
        )


def clamp(v: int, lo: int, hi: int) -> int:
    return max(lo, min(v, hi))


def step() -> None:
    moved = []
    for x, y in agents:
        dx, dy = rnd.choice([(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)])
        nx = clamp(x + dx, 0, GRID_W - 1)
        ny = clamp(y + dy, 0, GRID_H - 1)
        moved.append((nx, ny))
    agents[:] = moved


def tick(canvas: tk.Canvas, root: tk.Tk, food: Food) -> None:
    food.regrow_step(p=0.03)
    canvas.delete("food")
    food.draw(canvas, CELL)

    step()
    canvas.delete("agent")
    draw_agents(canvas)
    root.after(200, lambda: tick(canvas, root, food))


def main() -> None:
    rnd.seed(SEED)

    root = tk.Tk()
    root.title("empathy_sim — 0.1")

    canvas = tk.Canvas(
        root,
        width=GRID_W * CELL,
        height=GRID_H * CELL,
        bg="#0f0f0f",
        highlightthickness=0,
    )
    canvas.pack()

    food = Food(GRID_W, GRID_H, max_food=5)
    food.randomize(0, 3)
    food.draw(canvas, CELL)

    draw_grid(canvas)

    spawn_agents(10)
    tick(canvas, root, food)
    root.mainloop()


if __name__ == "__main__":
    main()
