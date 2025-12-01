import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from empathy_sim.core.stats_recorder import StatsRecorder


class StatsWindow:
    WINDOW_WIDTH = 500
    WINDOW_HEIGHT = 300

    LABEL_PAD_X = 10
    LABEL_PAD_Y = 5

    GRAPH_MARGIN = 20
    MAX_POINTS_GRAPH = 1000

    LEGEND_Y_OFFSET = 70
    LEGEND_X_OFFSET = 15

    FOOD_SCALE = 10

    LEGEND_HEIGHT = 80

    SERIES_COLORS = {
        "alive": "#3ae424",
        "food": "#ec4d4d",
        "empathic": "#2457e4",
        "selfish": "#dcec4d",
    }

    LEGEND_ITEMS = [
        ("Alive", "alive"),
        ("Food", "food"),
        ("Empathic alive", "empathic"),
        ("Selfish alive", "selfish"),
    ]

    def __init__(self, master: tk.Tk) -> None:
        self.window = tk.Toplevel(master)
        self.window.title("empathy_sim — statistics")

        self.width = self.WINDOW_WIDTH
        self.height = self.WINDOW_HEIGHT

        self.canvas = tk.Canvas(
            self.window,
            width=self.width,
            height=self.height,
            bg="#111111",
            highlightthickness=0,
        )
        self.canvas.pack()

        self.label_tick = tk.Label(self.window, text="Tick: 0")
        self.label_tick.pack(anchor="w", padx=self.LABEL_PAD_X, pady=self.LABEL_PAD_Y)

        self.label_alive = tk.Label(self.window, text="Alive: 0")
        self.label_alive.pack(anchor="w", padx=self.LABEL_PAD_X, pady=self.LABEL_PAD_Y)

        self.label_avg_energy = tk.Label(self.window, text="Abg energy: 0.0")
        self.label_avg_energy.pack(
            anchor="w", padx=self.LABEL_PAD_X, pady=self.LABEL_PAD_Y
        )

        self.label_emphatic_alive = tk.Label(self.window, text="Emphatic alive: 0")
        self.label_emphatic_alive.pack(
            anchor="w", padx=self.LABEL_PAD_X, pady=self.LABEL_PAD_Y
        )

        self.label_selfish_alive = tk.Label(self.window, text="Selfish alive: 0")
        self.label_selfish_alive.pack(
            anchor="w", padx=self.LABEL_PAD_X, pady=self.LABEL_PAD_Y
        )

    # ---------------------------------------------------------------------------------

    def update(self, stats_recorder: "StatsRecorder") -> None:
        self._update_labels(stats_recorder)
        self._update_graph(stats_recorder)

    # -------------------------Stat Labels ------------------------------------

    def _update_labels(self, stats_recorder: "StatsRecorder") -> None:
        history = stats_recorder.history
        if not history:
            return

        last = history[-1]
        tick, alive_now, _, alive_emphatic_now, alive_selfish_now, avg_energy = last
        self.label_tick.config(text=f"Tick: {tick}")
        self.label_alive.config(text=f"Alive: {alive_now}")
        self.label_avg_energy.config(text=f"Abg energy: {avg_energy:.1f}")
        self.label_emphatic_alive.config(text=f"Emphatic alive: {alive_emphatic_now}")
        self.label_selfish_alive.config(text=f"Selfish alive: {alive_selfish_now}")

    # --------------------------- Graph -----------------------------------------------

    def _update_graph(self, stats_recorder: "StatsRecorder") -> None:
        self.canvas.delete("graph")

        history = stats_recorder.history
        if len(history) < 2:
            return

        max_points = self.MAX_POINTS_GRAPH
        history = history[-max_points:]

        series, max_y = self._get_series(history)

        margin = self.GRAPH_MARGIN
        graph_top = margin
        graph_bottom = self.height - self.LEGEND_HEIGHT  # reserve bottom space
        h = graph_bottom - graph_top
        w = self.width - 2 * margin

        n = len(next(iter(series.values())))

        def to_canvas(i: int, value: int) -> tuple[float, float]:
            x = margin + (w * i) / (n - 1)
            y = margin + h - (h * value) / max_y
            return x, y

        points = self._build_points(series, to_canvas)
        self._draw_series(points)
        self._draw_legend()
        self._create_axis(graph_top, graph_bottom, h, w, margin, history, max_y)

    # ---------------------------------------------------------------------------------

    def _create_axis(
        self, graph_top, graph_bottom, h, w, margin, history, max_y
    ) -> None:
        # Y axis
        self.canvas.create_line(
            graph_top,
            graph_bottom,
            margin,
            margin,
            fill="#E7E7E7",
            arrow=tk.LAST,
            arrowshape=(6, 8, 4),
            tags="graph",
        )

        # X axis
        self.canvas.create_line(
            margin,
            margin + h,
            margin + w,
            margin + h,
            arrow=tk.LAST,
            fill="#E7E7E7",
            tags="graph",
        )

        # --- X-axis tick labels ---
        tick_count = history[-1][0]
        if tick_count < 10:
            return

        step_x = tick_count // 10

        def tick_to_x(i):
            return margin + (w * i) / (tick_count - 1)

        for i in range(0, tick_count, step_x):
            x = tick_to_x(i)
            self.canvas.create_text(
                x,
                margin + h,
                text=str(i),
                anchor="n",
                fill="#cccccc",
                tags="graph",
            )

        # --- Y-axis tick labels ---
        if max_y <= 0:
            return

        step_y = max(1, int(max_y // 5))

        def value_to_y(v: int) -> float:
            return graph_bottom - (h * v) / max_y

        for v in range(0, int(max_y + 1), step_y):
            if v == 0:
                continue
            y = value_to_y(v)
            self.canvas.create_text(
                margin - 4,
                y,
                text=str(v),
                anchor="e",
                fill="#cccccc",
                tags="graph",
            )

    def _get_series(self, history):
        _, alive, food, empathic, selfish, _ = zip(*history)

        food = [f / self.FOOD_SCALE for f in food]

        max_y = max(max(alive) or 1, max(food) or 1)

        return {
            "alive": alive,
            "food": food,
            "empathic": empathic,
            "selfish": selfish,
        }, max_y

    def _build_points(self, series: dict[str, list[float]], to_canvas):
        points: dict[str, list[tuple[float, float]]] = {}
        for name, values in series.items():
            points[name] = [to_canvas(i, v) for i, v in enumerate(values)]
        return points

    def _draw_series(self, points: dict[str, list[tuple[float, float]]]) -> None:
        colors = self.SERIES_COLORS

        for name, pts in points.items():
            for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
                self.canvas.create_line(x1, y1, x2, y2, fill=colors[name], tags="graph")

    def _draw_legend(self) -> None:
        legend_x = self.LEGEND_X_OFFSET
        legend_y = self.height - self.LEGEND_HEIGHT + 40

        x = legend_x
        for label, name in self.LEGEND_ITEMS:
            # box
            self.canvas.create_rectangle(
                x,
                legend_y,
                x + 10,
                legend_y + 10,
                fill=self.SERIES_COLORS[name],
                outline="",
                tags="graph",
            )

            # text
            text_id = self.canvas.create_text(
                x + 20,
                legend_y + 5,
                text=label,
                anchor="w",
                fill="#ffffff",
                tags="graph",
            )

            bbox = self.canvas.bbox(text_id)
            text_width = bbox[2] - bbox[0]
            x += 20 + text_width + 15
