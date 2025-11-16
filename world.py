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
        self.agents: list[Agent] = []

    def count_alive(self) -> int:
        count = 0
        for i in self.agents:
            if i.alive:
                count += 1
        return count

    def average_energy(self) -> float:
        sum = 0
        alive = self.count_alive()
        for i in self.agents:
            if i.alive:
                sum += i.energy
        if alive == 0:
            return 0.0
        return sum / alive

    # Draw simple stats of the simulation
    def draw_hud(self) -> None:
        self.canvas.delete("hud")
        alive = self.count_alive()
        avg_energy = self.average_energy()

        self.canvas.create_text(
            10,
            10,
            text=f"Alive: {alive}",
            fill="#ffffff",
            anchor="nw",
            tags="hud",
            font=("Helvetica", 12),
        )

        self.canvas.create_text(
            10,
            30,
            text=f"Avg energy: {avg_energy}",
            fill="#ffffff",
            anchor="nw",
            tags="hud",
            font=("Helvetica", 12),
        )

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
                # give agent info about how much food there is in the cell
                i.is_there_food(self.food.amount_at(i.coords[0], i.coords[1]))
                # if agent found any food at the cell, it took one food from the cell
                if i.there_is_food:
                    self.food.take_at(i.coords[0], i.coords[1], 1)
                i.step((self.width, self.height))
                i.draw(self.canvas, self.cell)
            else:
                i.draw(self.canvas, self.cell, "#c40d0d")

        self.draw_hud()

        root.after(400, lambda: self.tick(root))
