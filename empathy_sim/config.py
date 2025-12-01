from dataclasses import dataclass


@dataclass
class SimConfig:
    # main canvas
    grid_w: int = 30
    grid_h: int = 16
    cell: int = 32
    seed: int = 42

    # world
    spawn_emphatic: int = 10
    spawn_selfish: int = 10

    food_regrow_prob: float = 0.03
    max_food: int = 5
    min_starting_food_per_cell: int = 0
    max_starting_food_per_cell: int = 3

    # how much time has to pass for agent to be removed from the list
    ticks_to_remove_corpse: int = 10

    # interactions
    need_help_energy_below: int = 5
    can_help_energy: int = 14
    energy_to_share: int = 4

    # agent
    default_starting_energy: int = 20
    max_energy: int = 20
    starting_age: int = 0
    default_reproduction_cooldown: int = 10
    starting_energy: int = 10
    reproduction_cooldown: int = 10
    maximum_age: int = 200
    ready_to_reproduce_energy: int = 14
    how_much_energy_spent_to_reproduce: int = 5
    reproduction_cooldown_after_reproduction: int = 20
    movement_energy: int = 1
    eating_energy: int = 1

    default_mutation_chance: float = 0.02
