# from __future__ import annotations
import tkinter as tk


class StatsWindow:
    def __init__(self, master: tk.Tk) -> None:
        self.window = tk.Toplevel(master)
        self.window.title("empathy_sim — statistics")

        self.label_tick = tk.Label(self.window, text="Tick: 0")
        self.label_tick.pack(anchor="w", padx=10, pady=5)

        self.label_alive = tk.Label(self.window, text="Alive: 0")
        self.label_alive.pack(anchor="w", padx=10, pady=5)

        self.label_avg_energy = tk.Label(self.window, text="Abg energy: 0.0")
        self.label_avg_energy.pack(anchor="w", padx=10, pady=5)

    def update(self, world) -> None:
        tick = getattr(world, "tick_count", 0)

        alive = world.count_alive()
        avg_energy = world.average_energy()
        self.label_tick.config(text=f"Tick: {tick}")
        self.label_alive.config(text=f"Alive: {alive}")
        self.label_avg_energy.config(text=f"Abg energy: {avg_energy:.1f}")
