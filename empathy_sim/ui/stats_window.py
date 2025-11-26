import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from empathy_sim.core.world import World
    from empathy_sim.core.stats_recorder import StatsRecorder


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

        self.label_emphatic_alive = tk.Label(self.window, text="Emphatic alive: 0")
        self.label_emphatic_alive.pack(anchor="w", padx=10, pady=5)

        self.label_selfish_alive = tk.Label(self.window, text="Selfish alive: 0")
        self.label_selfish_alive.pack(anchor="w", padx=10, pady=5)

    def update(self, stats_recorder: "StatsRecorder") -> None:
        self._update_labels(stats_recorder)
        self._update_graph(stats_recorder)

    def _update_labels(self, stats_recorder: "StatsRecorder") -> None:
        # ------------ Stat Labels ------------------
        history = stats_recorder.history
        if len(history) < 2:
            return

        last = stats_recorder.history[-1]
        tick, alive_now, _, alive_emphatic_now, alive_selfish_now, avg_energy = last
        self.label_tick.config(text=f"Tick: {tick}")
        self.label_alive.config(text=f"Alive: {alive_now}")
        self.label_avg_energy.config(text=f"Abg energy: {avg_energy:.1f}")
        self.label_emphatic_alive.config(text=f"Emphatic alive: {alive_emphatic_now}")
        self.label_selfish_alive.config(text=f"Selfish alive: {alive_selfish_now}")

    def _update_graph(self, stats_recorder: "StatsRecorder") -> None:
        # ------------ Graph ------------------
        self.canvas.delete("graph")

        history = stats_recorder.history
        if len(history) < 2:
            return

        # show last points
        max_points = 1000
        history = history[-max_points:]

        # unpack history
        _, alive_series, food_series, alive_emphatic_series, alive_selfish_series, _ = (
            zip(*history)
        )

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

        alive_emphatic_points = [
            to_canvas(i, v) for i, v in enumerate(alive_emphatic_series)
        ]
        alive_selfish_points = [
            to_canvas(i, v) for i, v in enumerate(alive_selfish_series)
        ]

        # draw alive (yellow)
        for (x1, y1), (x2, y2) in zip(alive_points, alive_points[1:]):
            self.canvas.create_line(x1, y1, x2, y2, fill="#3ae424", tags="graph")

        # draw food (cyan)
        for (x1, y1), (x2, y2) in zip(food_points, food_points[1:]):
            self.canvas.create_line(x1, y1, x2, y2, fill="#ec4d4d", tags="graph")

        for (x1, y1), (x2, y2) in zip(alive_emphatic_points, alive_emphatic_points[1:]):
            self.canvas.create_line(x1, y1, x2, y2, fill="#2457e4", tags="graph")

        # draw food (cyan)
        for (x1, y1), (x2, y2) in zip(alive_selfish_points, alive_selfish_points[1:]):
            self.canvas.create_line(x1, y1, x2, y2, fill="#dcec4d", tags="graph")

        # -------------- Legend ---------------
        legend_x = 10
        legend_y = self.height - 70  # give more space

        items = [
            ("Alive", "#3ae424"),
            ("Food", "#ec4d4d"),
            ("Empathic alive", "#2457e4"),
            ("Selfish alive", "#dcec4d"),
        ]

        for idx, (label, color) in enumerate(items):
            y = legend_y + idx * 15

            self.canvas.create_rectangle(
                legend_x,
                y,
                legend_x + 10,
                y + 10,
                fill=color,
                outline="",
                tags="graph",
            )

            self.canvas.create_text(
                legend_x + 20,
                y + 5,
                text=label,
                anchor="w",
                fill="#ffffff",
                tags="graph",
            )
