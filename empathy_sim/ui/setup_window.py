import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from empathy_sim.config import SimConfig


class SetupWindow(tk.Toplevel):
    WINDOW_WIDTH = 400
    WINDOW_HEIGHT = 200

    def __init__(self, master: tk.Tk, config: "SimConfig", on_start) -> None:
        super().__init__(master)
        self.title("empathy_sim — setup")

        self.config = config

        self.width = self.WINDOW_WIDTH
        self.height = self.WINDOW_HEIGHT

        self.on_start = on_start

        self.grid_w_var = tk.IntVar(value=config.grid_w)
        self.grid_h_var = tk.IntVar(value=config.grid_h)

        self.starting_emphatic = tk.IntVar(value=config.spawn_emphatic)
        self.starting_selfish = tk.IntVar(value=config.spawn_selfish)

        self.seed = tk.IntVar(value=config.seed)

        self.start_button: tk.Button

        self._create_UI()

    def _handle_start(self):
        self.config.grid_w = self.grid_w_var.get()
        self.config.grid_h = self.grid_h_var.get()

        self.config.spawn_emphatic = self.starting_emphatic.get()
        self.config.spawn_selfish = self.starting_selfish.get()

        self.start_button.config(state="disabled")
        self.on_start()
        self.destroy()

    def _create_UI(self):
        tk.Label(self, text="Grid width").grid(row=0, column=0)
        tk.Entry(self, textvariable=self.grid_w_var).grid(row=0, column=1)

        tk.Label(self, text="Grid height").grid(row=1, column=0)
        tk.Entry(self, textvariable=self.grid_h_var).grid(row=1, column=1)

        tk.Label(self, text="Starting emphatic").grid(row=2, column=0)
        tk.Entry(self, textvariable=self.starting_emphatic).grid(row=2, column=1)

        tk.Label(self, text="Starting selfish").grid(row=3, column=0)
        tk.Entry(self, textvariable=self.starting_selfish).grid(row=3, column=1)

        tk.Label(self, text="Seed").grid(row=4, column=0)
        tk.Entry(self, textvariable=self.seed).grid(row=4, column=1)

        self.start_button = tk.Button(self, text="Start", command=self._handle_start)
        self.start_button.grid(row=99, column=0, columnspan=2)
