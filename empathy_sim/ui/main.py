#!/usr/bin/env python3

import tkinter as tk
import random as rnd
from empathy_sim.core.world import World
from empathy_sim.ui.renderer import Renderer
from empathy_sim.ui.stats_window import StatsWindow
from empathy_sim.core.stats_recorder import StatsRecorder
from empathy_sim.config import SimConfig
from empathy_sim.version import __verison__


def tick(
    root: tk.Tk,
    stats: StatsWindow,
    world: World,
    renderer: Renderer,
    stats_recorder: StatsRecorder,
) -> None:
    world.step()
    renderer.render(world.food, world.agents)
    stats_recorder.record_step_stats(world)
    stats.update(world, stats_recorder)
    root.after(100, tick, root, stats, world, renderer, stats_recorder)


def main() -> None:
    config = SimConfig()

    seed = config.seed
    grid_w = config.grid_w
    grid_h = config.grid_h
    cell = config.cell

    rnd.seed(seed)

    root = tk.Tk()
    root.title(f"empathy_sim — {__verison__}")

    canvas = tk.Canvas(
        root,
        width=grid_w * cell,
        height=grid_h * cell,
        bg="#0f0f0f",
        highlightthickness=0,
    )
    canvas.pack()

    renderer = Renderer(canvas, grid_w, grid_h, cell)

    world = World(config)
    renderer.draw_grid()
    world.spawn()

    stats_recorder = StatsRecorder()

    stats = StatsWindow(root)

    tick(root, stats, world, renderer, stats_recorder)

    root.mainloop()


if __name__ == "__main__":
    main()
