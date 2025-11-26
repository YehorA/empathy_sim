from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from empathy_sim.core.world import World


class StatsRecorder:
    def __init__(self):
        self.tick_count = 0
        self.history: list[tuple[int, int, int, int, int, float]] = []

    def record_step_stats(self, world: "World") -> None:
        # after everything done, update some statistics
        self.tick_count += 1
        alive = world.count_alive()
        total_food = sum(world.food.foods.values())

        alive_emphatic = world.count_alive_emphatic()
        alive_selfish = world.count_alive_selfish()
        avg_energy = world.average_energy()
        self.history.append(
            (
                self.tick_count,
                alive,
                total_food,
                alive_emphatic,
                alive_selfish,
                avg_energy,
            )
        )
