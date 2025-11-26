#!/usr/bin/env python3

import tkinter as tk
import random as rnd
from empathy_sim.core.world import World
from empathy_sim.ui.renderer import Renderer
from empathy_sim.ui.stats_window import StatsWindow
from empathy_sim.core.stats_recorder import StatsRecorder
from empathy_sim.config import SimConfig
from empathy_sim.version import __verison__

sim_state = {"paused": False, "speed": 1.0}


def tick(
    root: tk.Tk,
    stats: StatsWindow,
    world: World,
    renderer: Renderer,
    stats_recorder: StatsRecorder,
) -> None:
    if not sim_state["paused"]:
        world.step()
        renderer.render(world.food, world.agents)
        stats_recorder.record_step_stats(world)
        stats.update(stats_recorder)

    base_delay = 100
    speed = sim_state.get("speed", 1.0)
    if speed <= 0:
        delay = base_delay
    else:
        delay = int(base_delay / speed)

    root.after(delay, tick, root, stats, world, renderer, stats_recorder)


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

    controls = tk.Frame(root)
    controls.pack(fill="x")

    def toggle_pause():
        sim_state["paused"] = not sim_state["paused"]
        pause_button.config(text="Resume" if sim_state["paused"] else "Pause")

    pause_button = tk.Button(controls, text="Pause", command=toggle_pause)
    pause_button.pack(side="left")

    def on_speed_change(value: str) -> None:
        sim_state["speed"] = float(value)

    speed_scale = tk.Scale(
        controls,
        from_=0.1,
        to=2.0,
        resolution=0.1,
        orient="horizontal",
        command=on_speed_change,
    )
    speed_scale.set(1.0)
    speed_scale.pack(side="left")

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
