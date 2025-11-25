#!/usr/bin/env python3

import tkinter as tk
import random as rnd
from empathy_sim.core.world import World
from empathy_sim.ui.renderer import Renderer
from empathy_sim.ui.stats_window import StatsWindow
from empathy_sim.core.stats_recorder import StatsRecorder
from empathy_sim.version import __verison__

GRID_W = 30
GRID_H = 16
CELL = 32
SEED = 42


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
    rnd.seed(SEED)

    root = tk.Tk()
    root.title(f"empathy_sim — {__verison__}")

    canvas = tk.Canvas(
        root,
        width=GRID_W * CELL,
        height=GRID_H * CELL,
        bg="#0f0f0f",
        highlightthickness=0,
    )
    canvas.pack()

    renderer = Renderer(canvas, GRID_W, GRID_H, CELL)

    world = World(GRID_W, GRID_H)
    renderer.draw_grid()
    world.spawn()

    stats_recorder = StatsRecorder()

    stats = StatsWindow(root)

    tick(root, stats, world, renderer, stats_recorder)

    root.mainloop()


if __name__ == "__main__":
    main()
