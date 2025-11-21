import tkinter as tk
from food import Food
from agent import Agent
from utils import clamp
import random as rnd


class World:
    def __init__(self, width, height, cell, canvas):
        self.width = width
        self.height = height
        self.cell = cell
        self.canvas = canvas
        self.food = Food(width, height, max_food=5)
        self.agents: list[Agent] = []

        # some info for the graph and statistics
        self.tick_count: int
        # (tick, alive, total_food)
        self.history: list[tuple[int, int, int]]

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
    # def draw_hud(self) -> None:
    #     self.canvas.delete("hud")
    #     alive = self.count_alive()
    #     avg_energy = self.average_energy()

    #     self.canvas.create_text(
    #         10,
    #         10,
    #         text=f"Alive: {alive}",
    #         fill="#fffc4f",
    #         anchor="nw",
    #         tags="hud",
    #         font=("Helvetica", 12),
    #     )

    #     self.canvas.create_text(
    #         10,
    #         30,
    #         text=f"Avg energy: {avg_energy}",
    #         fill="#fffc4f",
    #         anchor="nw",
    #         tags="hud",
    #         font=("Helvetica", 12),
    #     )

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
        for _ in range(20):
            a = Agent()
            a.place_random((self.width, self.height))
            self.agents.append(a)

    def coord_food_view(self, x, y) -> dict[tuple[int, int], int]:
        # Returns food amount in the current cell and 4 neighbors
        dirs = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
        view = {}
        for dx, dy in dirs:
            nx = clamp(x + dx, 0, self.width - 1)
            ny = clamp(y + dy, 0, self.height - 1)
            view[(dx, dy)] = self.food.amount_at(nx, ny)
        return view

    def coord_agent_view(self, x, y, exclude: Agent) -> list[Agent]:
        # Returns agents in the current cell and 4 neighbors
        dirs = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
        agents_near: list[Agent] = []
        for dx, dy in dirs:
            nx = clamp(x + dx, 0, self.width - 1)
            ny = clamp(y + dy, 0, self.height - 1)
            for i in self.agents:
                if i is exclude:
                    continue
                if i.coords == (nx, ny):
                    agents_near.append(i)
        return agents_near

    def tick(self, root: tk.Tk, stats) -> None:
        self.food.regrow_step(p=0.03)
        self.canvas.delete("food")
        self.food.draw(self.canvas, self.cell)

        self.canvas.delete("agent")

        for i in self.agents:
            if i.alive:
                agents_nearby = self.coord_agent_view(i.coords[0], i.coords[1], i)
                self.reproduction(i, agents_nearby)

                view = self.coord_food_view(i.coords[0], i.coords[1])
                i.step((self.width, self.height), view)
                if i.ate:
                    self.food.take_at(i.coords[0], i.coords[1], 1)
                i.draw(self.canvas, self.cell)
            else:
                i.death_time += 1
                i.draw(self.canvas, self.cell)
                # if dead for more then 10 ticks remove from the list
                if i.death_time > 10:
                    self.agents.remove(i)

        # self.draw_hud()

        stats.update(self)

        root.after(100, lambda: self.tick(root, stats))

    def record_step_stats(self) -> None:
        # after everything done, update some statistics
        self.tick_count += 1
        alive = self.count_alive()
        total_food = sum(self.food.foods.values())
        self.history.append((self.tick_count, alive, total_food))

    # AGENT REPRODUCTION SHOULD BE SEPERATED INTO CLASS LATER

    def reproduction(self, agent: Agent, agents_nearby: list[Agent]) -> None:
        if agent.is_ready_to_reproduce():
            ready_to_reproduce_agents: list[Agent] = []
            for i in agents_nearby:
                if i.is_ready_to_reproduce():
                    ready_to_reproduce_agents.append(i)
            if ready_to_reproduce_agents:
                other_agent = rnd.choice(ready_to_reproduce_agents)
                agent.reproduce()
                other_agent.reproduce()

                spawn_pos = rnd.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
                a = Agent()
                a.place_on_coords(
                    agent.coords[0] + spawn_pos[0],
                    agent.coords[1] + spawn_pos[1],
                    (self.width, self.height),
                )
                self.agents.append(a)
