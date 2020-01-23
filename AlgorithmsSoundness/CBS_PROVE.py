from SearchBasedAlgorithms.AStarMultiAgent.SolverAStarOD import SolverAStarOD
from SearchBasedAlgorithms.ConflictBasedSearch.SolverConflictBasedSearch import SolverConflictBasedSearch
from SearchBasedAlgorithms.CooperativeAStar.SolverCooperativeAStar import SolverCooperativeAStar
from SearchBasedAlgorithms.IndependenceDetection.SolverIndependenceDetection import SolverIndependenceDetection
from Utilities.Agent import Agent
from Utilities.Map import Map
from Utilities.ProblemInstance import ProblemInstance
from Utilities.SolverSettings import SolverSettings
import random
from tkinter import *

occupancy_lst = set()
free_lst = set()

for x in range(8):
    for y in range(8):
        if random.random() < 0:
            occupancy_lst.add((x, y))
        else:
            free_lst.add((x, y))

assert len(occupancy_lst) == 0, "ha creato ostacoli noooooooo"

map = Map(8, 8, occupancy_lst)

agents = [Agent(0, (2,7), (0,4)), Agent(1, (0,6), (7,4)), Agent(2, (2,6), (4,0)), Agent(3, (7,6), (0,1))]
# agents = [Agent(0, (0,6), (7,4)), Agent(1, (7,6), (0,1))]

problem_instance = ProblemInstance(map, agents)

solver_settings = SolverSettings(goal_occupation_time=1)
solver = SolverIndependenceDetection(SolverConflictBasedSearch(solver_settings), solver_settings)
# solver = SolverConflictBasedSearch(solver_settings)

[print(a) for a in agents]

paths, output_infos = solver.solve(problem_instance, return_infos=True, verbose=True)
