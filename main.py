#!/usr/bin/env python3

import tkinter as tk
import random as rnd
from food import Food
from agent import Agent

GRID_W = 20
GRID_H = 12
CELL = 32
SEED = 42


def draw_grid(canvas: tk.Canvas) -> None:
    for i in range(GRID_W + 1):
        X = i * CELL
        canvas.create_line(X, 0, X, GRID_H * CELL, fill="#333", tags="grid")
    for i in range(GRID_H + 1):
        Y = i * CELL
        canvas.create_line(0, Y, GRID_W * CELL, Y, fill="#333", tags="grid")


def tick(canvas: tk.Canvas, root: tk.Tk, food: Food, agents: list[Agent]) -> None:
    food.regrow_step(p=0.03)
    canvas.delete("food")
    food.draw(canvas, CELL)

    canvas.delete("agent")

    for i in agents:
        i.step((GRID_W, GRID_H), food)
        i.draw(canvas, CELL)
        # print(i.energy)

    root.after(400, lambda: tick(canvas, root, food, agents))


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

    draw_grid(canvas)

    # food spawn
    food = Food(GRID_W, GRID_H, max_food=5)
    food.randomize(0, 3)
    food.draw(canvas, CELL)

    # agent spawn
    agents = []
    for _ in range(10):
        a = Agent()
        a.place_random((GRID_W, GRID_H))
        agents.append(a)

    tick(canvas, root, food, agents)
    root.mainloop()


if __name__ == "__main__":
    main()
