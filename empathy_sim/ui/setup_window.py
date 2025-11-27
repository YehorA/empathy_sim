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

        self._create_UI()

    def _handle_start(self):
        self.config.grid_w = self.grid_w_var.get()
        self.config.grid_h = self.grid_h_var.get()
        self.on_start(self.config)
        self.destroy()

    def _create_UI(self):
        tk.Label(self, text="Grid width").grid(row=0, column=0)
        tk.Entry(self, textvariable=self.grid_w_var).grid(row=0, column=1)

        tk.Label(self, text="Grid height").grid(row=1, column=0)
        tk.Entry(self, textvariable=self.grid_h_var).grid(row=1, column=1)

        tk.Button(self, text="Start", command=self._handle_start).grid(
            row=99, column=0, columnspan=2
        )
