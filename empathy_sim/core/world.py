from empathy_sim.core.food import Food
from empathy_sim.core.agent import Agent
from empathy_sim.core.utils import clamp
from empathy_sim.core.interactions import reproduction, help_other_agent
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from empathy_sim.config import SimConfig


class World:
    def __init__(self, config: "SimConfig"):
        self.config = config
        self.width = self.config.grid_w
        self.height = self.config.grid_h
        self.food = Food(self.width, self.height, max_food=self.config.max_food)
        self.agents: list[Agent] = []

    # -----------------------------------------------------------------------------------
    @property
    def alive_agents(self) -> list[Agent]:
        return [a for a in self.agents if a.alive]

    # -----------------------------------------------------------------------------------

    def count_alive(self) -> int:
        return len(self.alive_agents)

    def count_alive_emphatic(self) -> int:
        return sum(1 for a in self.alive_agents if a.gene.empathy)

    def count_alive_selfish(self) -> int:
        return sum(1 for a in self.alive_agents if not a.gene.empathy)

    def average_energy(self) -> float:
        alive = self.alive_agents
        if not alive:
            return 0.0
        return sum(a.energy for a in alive) / len(alive)

    def spawn(self) -> None:
        # food spawn
        self.food.randomize(
            self.config.min_starting_food_per_cell,
            self.config.max_starting_food_per_cell,
        )

        # agent spawn
        for _ in range(self.config.spawn_emphatic):
            a = Agent(self.config)
            a.place_random((self.width, self.height))
            a.gene.empathy = True
            self.agents.append(a)
        for _ in range(self.config.spawn_selfish):
            a = Agent(self.config)
            a.place_random((self.width, self.height))
            a.gene.empathy = False
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
        self.food.regrow_step(p=self.config.food_regrow_prob)

        alive_of_recent = []
        for i in self.agents:
            if not i.alive:
                i.death_time += 1
                # if dead for more then death_time ticks remove from the list
                if i.death_time > self.config.ticks_to_remove_corpse:
                    continue
            if i.alive:
                agents_nearby = self.coord_agent_view(i.coords[0], i.coords[1], i)
                reproduction(self, i, agents_nearby)
                help_other_agent(self, i, agents_nearby)

                view = self.coord_food_view(i.coords[0], i.coords[1])
                i.step((self.width, self.height), view)
                if i.ate:
                    self.food.take_at(i.coords[0], i.coords[1], 1)
            alive_of_recent.append(i)
        self.agents = alive_of_recent
