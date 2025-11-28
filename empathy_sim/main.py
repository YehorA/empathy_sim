#!/usr/bin/env python3

import tkinter as tk
from empathy_sim.config import SimConfig
from empathy_sim.version import __verison__
from empathy_sim.ui.sim_app import SimApp


def main() -> None:
    root = tk.Tk()
    root.title(f"empathy_sim — {__verison__}")
    config = SimConfig()
    SimApp(root, config)
    root.mainloop()


if __name__ == "__main__":
    main()
