empathy_sim

Small grid-based simulation with simple agents (selfish/empathic for now).

Current version: 0.2.x (refactoring + UI)
Python: 3.12+

How to run:
pip install -r requirements.txt
python -m empathy_sim.main

Controls

Setup window:
seed
grid width / height
starting number of selfish / empathic agents

Main window:
pause / resume
speed slider
restart simulation
separate stats window with graphs + basic numbers

Architecture:
ui.SimApp – main Tkinter app, creates windows + runs the loop
ui.Renderer – draws the grid, food and agents
ui.StatsWindow – shows the graph + counters
ui.SetupWindow – first window to configure the sim
core.World – simulation state and step() logic
core.Agent – agent data + methods
core.Food – food tiles
core.interactions – agent-agent interactions (reproduction, helping, etc.)
core.StatsRecorder – records history for the graph
config.SimConfig – all parameters in one place

Roadmap
0.2.x – UI, refactoring
0.3 – mutations
0.4 – territorial behavior
0.5 – aggression, etc.
(May change as the project grows and doesn't have strict plan or "final vision")