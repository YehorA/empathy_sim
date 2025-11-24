from typing import Sequence
from empathy_sim.core.food import Food
from empathy_sim.core.agent import Agent


class Renderer:
    def __init__(self, canvas, width, height, cell):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.cell = cell

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

    # handles visuals for "tick"

    def render(self, food: Food, agents: Sequence[Agent]) -> None:
        self.canvas.delete("food")
        food.draw(self.canvas, self.cell)

        self.canvas.delete("agent")
        for agent in agents:
            agent.draw(self.canvas, self.cell)
