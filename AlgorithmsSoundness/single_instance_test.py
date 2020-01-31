"""
Experiments:
- 32x32 grids were generated with random obstacles (each cell is an obstacle with 20% probability).
- Each agent was placed in a random unique location with a random unique destination.

The inadmissible algorithm, hierarchical cooperative A* (HCA*), from (Silver 2005), and admissible combinations of the
standard algorithm (S), operator decomposition (OD), and independence detection (ID) were run on the same 10,000
instances with a random number of agents chosen uniformly between 2 and 60.
"""
from MAPFSolver.SearchBasedAlgorithms.AStarOD.AStarODSolver import AStarODSolver
from MAPFSolver.SearchBasedAlgorithms.AStar.AStarSolver import AStarSolver
from MAPFSolver.Utilities.problem_generation import generate_random_map
from MAPFSolver.Utilities.ProblemInstance import ProblemInstance
from MAPFSolver.Utilities.SolverSettings import SolverSettings
from MAPFSolver.Utilities.Agent import Agent
from tkinter import *


problem_map = generate_random_map(8, 8, 0)
problem_agents = [Agent(0, (6, 6), (0, 4)), Agent(1, (2, 0), (4, 6)), Agent(2, (3, 6), (4, 3)), Agent(3, (0, 2), (7, 4))]

problem_instance = ProblemInstance(problem_map, problem_agents)

solver_settings = SolverSettings(stay_in_goal=True)
solver = AStarODSolver(solver_settings)

paths = solver.solve(problem_instance, verbose=True)

root = Tk()
frame = Frame(root)
frame.pack()
problem_instance.plot_on_gui(frame, paths=paths)

root.mainloop()
