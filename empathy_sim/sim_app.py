import tkinter as tk
import random as rnd
from empathy_sim.core.world import World
from empathy_sim.ui.renderer import Renderer
from empathy_sim.ui.stats_window import StatsWindow
from empathy_sim.core.stats_recorder import StatsRecorder
from empathy_sim.ui.setup_window import SetupWindow
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from empathy_sim.config import SimConfig


class SimApp:
    def __init__(self, root: tk.Tk, config: "SimConfig"):
        self.root = root
        self.sim_state = {"paused": False, "speed": 1.0, "running": False}
        self.config = config
        self.setup = SetupWindow(root, config, on_start=self.start_sim)

        self.canvas: tk.Canvas | None = None
        self.world: World | None = None
        self.renderer: Renderer | None = None
        self.stats_recorder: StatsRecorder | None = None
        self.stats: StatsWindow | None = None
        self.controls: tk.Frame | None = None

    def start_sim(self):
        self.sim_state["running"] = True
        self.sim_state["paused"] = False
        seed = self.config.seed
        rnd.seed(seed)

        grid_w = self.config.grid_w
        grid_h = self.config.grid_h
        cell = self.config.cell

        self._create_ui(grid_w, grid_h, cell)
        self._create_simulation(grid_w, grid_h, cell)

        self.tick()

    def _create_ui(self, grid_w: int, grid_h: int, cell: int):
        self.canvas = tk.Canvas(
            self.root,
            width=grid_w * cell,
            height=grid_h * cell,
            bg="#0f0f0f",
            highlightthickness=0,
        )
        self.canvas.pack()

        self.controls = tk.Frame(self.root)
        self.controls.pack(fill="x")

        def toggle_pause():
            self.sim_state["paused"] = not self.sim_state["paused"]
            pause_button.config(text="Resume" if self.sim_state["paused"] else "Pause")

        pause_button = tk.Button(self.controls, text="Pause", command=toggle_pause)
        pause_button.pack(side="left")

        restart_button = tk.Button(self.controls, text="Restart", command=self.restart)
        restart_button.pack(side="left")

        def on_speed_change(value: str) -> None:
            self.sim_state["speed"] = float(value)

        speed_scale = tk.Scale(
            self.controls,
            from_=0.1,
            to=2.0,
            resolution=0.1,
            orient="horizontal",
            command=on_speed_change,
        )
        speed_scale.set(1.0)
        speed_scale.pack(side="left")

    def _create_simulation(self, grid_w: int, grid_h: int, cell: int):
        self.renderer = Renderer(self.canvas, grid_w, grid_h, cell)
        self.world = World(self.config)
        self.renderer.draw_grid()
        self.world.spawn()
        self.stats_recorder = StatsRecorder()
        self.stats = StatsWindow(self.root)

    def tick(self) -> None:
        if not self.sim_state["running"]:
            return
        # safegurad if attributes are not declared
        if (
            self.world is None
            or self.renderer is None
            or self.stats_recorder is None
            or self.stats is None
        ):
            return

        if not self.sim_state["paused"]:
            self.world.step()
            self.renderer.render(self.world.food, self.world.agents)
            self.stats_recorder.record_step_stats(self.world)
            self.stats.update(self.stats_recorder)

        base_delay = 100
        speed = self.sim_state.get("speed", 1.0)
        if speed <= 0:
            delay = base_delay
        else:
            delay = int(base_delay / speed)

        self.root.after(delay, self.tick)

    def restart(self):
        self.sim_state["paused"] = True
        self.sim_state["running"] = False

        if self.stats is not None:
            self.stats.window.destroy()

        if self.canvas is not None:
            self.canvas.destroy()

        if self.controls is not None:
            self.controls.destroy()

        self.world = None
        self.renderer = None
        self.stats_recorder = None
        self.stats = None
        self.canvas = None
        self.controls = None

        self.setup = SetupWindow(self.root, self.config, on_start=self.start_sim)
