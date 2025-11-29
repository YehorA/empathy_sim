from empathy_sim.core.world import World
from empathy_sim.core.agent import Agent
from empathy_sim.core.interactions import help_other_agent
from empathy_sim.config import SimConfig


def test_world_initial_spawn():
    cfg = SimConfig(grid_w=10, grid_h=10, spawn_selfish=3, spawn_emphatic=2)
    world = World(cfg)
    world.spawn()

    assert world.count_alive() == 5
    assert world.count_alive_emphatic() == 2
    assert world.count_alive_selfish() == 3


def test_agent_ready_to_reproduce():
    cfg = SimConfig(ready_to_reproduce_energy=10)
    agent = Agent(cfg)

    agent.alive = False
    agent.energy = cfg.ready_to_reproduce_energy + 1
    agent.reproduction_cooldown = 0
    assert not agent.is_ready_to_reproduce()

    agent.alive = True
    agent.energy = cfg.ready_to_reproduce_energy - 1
    agent.reproduction_cooldown = 0
    assert not agent.is_ready_to_reproduce()

    agent.alive = True
    agent.energy = cfg.ready_to_reproduce_energy + 1
    agent.reproduction_cooldown = 20
    assert not agent.is_ready_to_reproduce()

    agent.alive = True
    agent.energy = cfg.ready_to_reproduce_energy + 1
    agent.reproduction_cooldown = 0
    assert agent.is_ready_to_reproduce()


def test_agent_after_reproduction():
    cfg = SimConfig()
    agent = Agent(cfg)
    agent.energy = cfg.ready_to_reproduce_energy

    agent.reproduce()
    assert agent.reproduction_cooldown == cfg.reproduction_cooldown_after_reproduction

    assert (
        agent.energy
        == cfg.ready_to_reproduce_energy - cfg.how_much_energy_spent_to_reproduce
    )


def test_share_energy():
    cfg = SimConfig()
    world = World(cfg)

    agent1 = Agent(cfg)
    agent1.energy = cfg.can_help_energy + 1
    agent1.empathy = True

    agent2 = Agent(cfg)
    agent2.energy = cfg.need_help_energy_below - 1

    help_other_agent(world, agent1, [agent2])

    assert agent1.energy == cfg.can_help_energy + 1 - cfg.energy_to_share
    assert agent2.energy == cfg.need_help_energy_below - 1 + cfg.energy_to_share
