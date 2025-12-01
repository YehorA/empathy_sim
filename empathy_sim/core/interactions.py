from typing import TYPE_CHECKING
from empathy_sim.core.agent import Agent
import random as rnd

if TYPE_CHECKING:
    from empathy_sim.core.world import World


def reproduction(world: "World", agent: Agent, agents_nearby: list[Agent]) -> None:
    cfg = world.config

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
            a = Agent(cfg)

            a.gene = a.gene.crossover(agent.gene, other_agent.gene)

            a.place_on_coords(
                agent.coords[0] + spawn_pos[0],
                agent.coords[1] + spawn_pos[1],
                (world.width, world.height),
            )
            world.agents.append(a)


def help_other_agent(world: "World", agent: Agent, agents_nearby: list[Agent]) -> None:
    cfg = world.config

    if agent.gene.empathy and agent.energy > cfg.can_help_energy:
        need_help_agents: list[Agent] = []
        for i in agents_nearby:
            if i.alive and i.energy < agent.gene.help_threshold:
                need_help_agents.append(i)
        if need_help_agents:
            other_agent = rnd.choice(need_help_agents)
            agent.energy -= agent.gene.help_amount
            other_agent.energy += agent.gene.help_amount
