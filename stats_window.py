import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from world import World


class StatsWindow:
    def __init__(self, master: tk.Tk) -> None:
        self.window = tk.Toplevel(master)
        self.window.title("empathy_sim — statistics")

        self.width = 400
        self.height = 200

        self.canvas = tk.Canvas(
            self.window,
            width=self.width,
            height=self.height,
            bg="#111111",
            highlightthickness=0,
        )
        self.canvas.pack()

        self.label_tick = tk.Label(self.window, text="Tick: 0")
        self.label_tick.pack(anchor="w", padx=10, pady=5)

        self.label_alive = tk.Label(self.window, text="Alive: 0")
        self.label_alive.pack(anchor="w", padx=10, pady=5)

        self.label_avg_energy = tk.Label(self.window, text="Abg energy: 0.0")
        self.label_avg_energy.pack(anchor="w", padx=10, pady=5)

    def update(self, world: "World") -> None:
        # ------------ Stat Labels ------------------

        tick = getattr(world, "tick_count", 0)
        alive_now = world.count_alive()
        avg_energy = world.average_energy()
        self.label_tick.config(text=f"Tick: {tick}")
        self.label_alive.config(text=f"Alive: {alive_now}")
        self.label_avg_energy.config(text=f"Abg energy: {avg_energy:.1f}")

        # ------------ Graph ------------------
        self.canvas.delete("graph")

        history = world.history
        if len(history) < 2:
            return

        # show last points
        max_points = 1000
        history = history[-max_points:]

        # unpack history
        _, alive_series, food_series = zip(*history)

        food_series = [f / 10 for f in food_series]

        max_alive = max(alive_series) or 1
        max_food = max(food_series) or 1
        max_y = max(max_alive, max_food, 1)

        # graph padding
        margin = 10
        w = self.width - 2 * margin
        h = self.height - 2 * margin
        n = len(alive_series)

        def to_canvas(i: int, value: int) -> tuple[float, float]:
            x = margin + (w * i) / (n - 1)
            y = margin + h - (h * value) / max_y
            return x, y

        # build points
        alive_points = [to_canvas(i, v) for i, v in enumerate(alive_series)]
        food_points = [to_canvas(i, v) for i, v in enumerate(food_series)]

        # draw alive (yellow)
        for (x1, y1), (x2, y2) in zip(alive_points, alive_points[1:]):
            self.canvas.create_line(x1, y1, x2, y2, fill="#2457e4", tags="graph")

        # draw food (cyan)
        for (x1, y1), (x2, y2) in zip(food_points, food_points[1:]):
            self.canvas.create_line(x1, y1, x2, y2, fill="#7aec4d", tags="graph")
