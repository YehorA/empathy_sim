from empathy_sim.core.food import Food
from empathy_sim.core.agent import Agent
from empathy_sim.core.utils import clamp
from empathy_sim.core.interactions import reproduction, help_other_agent


class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.food = Food(width, height, max_food=5)
        self.agents: list[Agent] = []

        # some info for the graph and statistics
        self.tick_count = 0
        # (tick, alive, total_food, empathy_alive, selfish_alive)
        self.history: list[tuple[int, int, int, int, int]] = []

    # -----------------------------------------------------------------------------------
    @property
    def alive_agents(self) -> list[Agent]:
        return [a for a in self.agents if a.alive]

    # -----------------------------------------------------------------------------------

    def count_alive(self) -> int:
        return len(self.alive_agents)

    def count_alive_emphatic(self) -> int:
        return sum(1 for a in self.alive_agents if a.empathy)

    def count_alive_selfish(self) -> int:
        return sum(1 for a in self.alive_agents if not a.empathy)

    def average_energy(self) -> float:
        alive = self.alive_agents
        if not alive:
            return 0.0
        return sum(a.energy for a in alive) / len(alive)

    def spawn(self) -> None:
        # food spawn
        self.food.randomize(0, 3)
        # self.food.draw(self.canvas, self.cell)

        # agent spawn
        for _ in range(10):
            a = Agent()
            a.place_random((self.width, self.height))
            self.agents.append(a)
        for _ in range(10):
            a = Agent()
            a.place_random((self.width, self.height))
            a.empathy = False
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

    # -----------------------------------------------------------

    # handles logic for "tick"
    def step(self) -> None:
        self.food.regrow_step(p=0.03)

        alive_of_recent = []
        for i in self.agents:
            if not i.alive:
                i.death_time += 1
                # if dead for more then 10 ticks remove from the list
                if i.death_time > 10:
                    continue
            if i.alive:
                agents_nearby = self.coord_agent_view(i.coords[0], i.coords[1], i)
                reproduction(self, i, agents_nearby)
                help_other_agent(i, agents_nearby)

                view = self.coord_food_view(i.coords[0], i.coords[1])
                i.step((self.width, self.height), view)
                if i.ate:
                    self.food.take_at(i.coords[0], i.coords[1], 1)
            alive_of_recent.append(i)
        self.agents = alive_of_recent

    # -----------------------------------------------------------

    def record_step_stats(self) -> None:
        # after everything done, update some statistics
        self.tick_count += 1
        alive = self.count_alive()
        total_food = sum(self.food.foods.values())

        alive_emphatic = self.count_alive_emphatic()
        alive_selfish = self.count_alive_selfish()
        self.history.append(
            (self.tick_count, alive, total_food, alive_emphatic, alive_selfish)
        )
