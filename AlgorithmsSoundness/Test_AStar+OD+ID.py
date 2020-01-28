"""
Experiments:
- 32x32 grids were generated with random obstacles (each cell is an obstacle with 20% probability).
- Each agent was placed in a random unique location with a random unique destination.

The inadmissible algorithm, hierarchical cooperative A* (HCA*), from (Silver 2005), and admissible combinations of the
standard algorithm (S), operator decomposition (OD), and independence detection (ID) were run on the same 10,000
instances with a random number of agents chosen uniformly between 2 and 60.
"""
from SearchBasedAlgorithms.AStarMultiAgent.SolverAStarOD import SolverAStarOD
from MAPFSolver.Utilities.Agent import Agent
from MAPFSolver.Utilities.Map import Map
from MAPFSolver.Utilities.ProblemInstance import ProblemInstance
from MAPFSolver.Utilities.SolverSettings import SolverSettings
import random
from tkinter import *


occupancy_lst = set()
free_lst = set()

for x in range(32):
    for y in range(32):
        if random.random() < 0.2:
            occupancy_lst.add((x, y))
        else:
            free_lst.add((x, y))
            
map = Map(32, 32, occupancy_lst)

n_of_agents = random.randrange(2, 5)

agents = []
agents_starts = []
agents_goals = []
for i in range(n_of_agents):
    while True:
        random_start = random.sample(free_lst, 1)[0]
        if random_start not in agents_starts and random_start not in agents_goals:
            agents_starts.append(random_start)
            break
    while True:
        random_goal = random.sample(free_lst, 1)[0]
        if random_goal not in agents_starts and random_goal not in agents_goals:
            agents_goals.append(random_goal)
            break
    agents.append(Agent(i, random_start, random_goal))

problem_instance = ProblemInstance(map, agents)

solver_settings = SolverSettings(goal_occupation_time=100)
solver = SolverAStarOD(solver_settings)

paths = solver.solve(problem_instance, verbose=True)

root = Tk()
frame = Frame(root)
frame.pack()
problem_instance.plot_on_gui(frame, paths=paths)

root.mainloop()
