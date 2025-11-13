import tkinter as tk
from food import Food
from agent import Agent


class World:
    def __init__(self, width, height, cell, canvas):
        self.width = width
        self.height = height
        self.cell = cell
        self.canvas = canvas
        self.food = Food(width, height, max_food=5)
        self.agents = []

    def draw_grid(self) -> None:
        for i in range(self.width + 1):
            X = i * self.cell
            self.canvas.create_line(
                X, 0, X, self.height * self.cell, fill="#333", tags="grid"
            )
        for i in range(self.height + 1):
            Y = i * self.cell
            self.canvas.create_line(
                0, Y, self.width * self.cell, Y, fill="#333", tags="grid"
            )

    def spawn(self) -> None:
        # food spawn
        self.food.randomize(0, 3)
        self.food.draw(self.canvas, self.cell)

        # agent spawn
        for _ in range(10):
            a = Agent()
            a.place_random((self.width, self.height))
            self.agents.append(a)

    def tick(self, root: tk.Tk) -> None:
        self.food.regrow_step(p=0.03)
        self.canvas.delete("food")
        self.food.draw(self.canvas, self.cell)

        self.canvas.delete("agent")

        for i in self.agents:
            if i.alive:
                i.step((self.width, self.height), self.food)
                i.draw(self.canvas, self.cell)
            else:
                i.draw(self.canvas, self.cell, "#c40d0d")

        root.after(400, lambda: self.tick(root))
