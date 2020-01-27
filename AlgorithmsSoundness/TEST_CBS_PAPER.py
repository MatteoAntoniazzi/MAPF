"""
Experiments:
- 32x32 grids were generated with random obstacles (each cell is an obstacle with 20% probability).
- Each agent was placed in a random unique location with a random unique destination.

The inadmissible algorithm, hierarchical cooperative A* (HCA*), from (Silver 2005), and admissible combinations of the
standard algorithm (S), operator decomposition (OD), and independence detection (ID) were run on the same 10,000
instances with a random number of agents chosen uniformly between 2 and 60.
"""
from SearchBasedAlgorithms.ConflictBasedSearch.SolverConflictBasedSearch import SolverConflictBasedSearch
from SearchBasedAlgorithms.IndependenceDetection.SolverIndependenceDetection import SolverIndependenceDetection
from Utilities.Agent import Agent
from Utilities.Map import Map
from MAPFSolver.Utilities.ProblemInstance import ProblemInstance
from MAPFSolver.Utilities.SolverSettings import SolverSettings
import random

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

agent_configurations = []

# ID Pre-processing get the 10 agent configurations [3:13] in which all agents belongs to the biggest subset of ID
for n in range(3, 14):  # Da 3 a 13

    print("-----------------------------------------------------------------------------------------------------------")
    print("AGENT NUMBER: ", n)
    print("-----------------------------------------------------------------------------------------------------------")

    while True:
        agents = []
        agents_starts = []
        agents_goals = []
        for i in range(n):
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

        print("PROBLEM: ", problem_instance.get_original_agents_id_list(), " ------------", problem_instance)

        solver_settings = SolverSettings(goal_occupation_time=1)
        solver = SolverIndependenceDetection(SolverConflictBasedSearch(solver_settings), solver_settings)

        paths, output_infos = solver.solve(problem_instance, return_infos=True, verbose=True)

        if output_infos["biggest_subset"] == n:
            agent_configurations.append(agents)
            break

assert len(agent_configurations) == 11, "ERRORRRRRRRRRRRRRR"

"""

problem_instance = ProblemInstance(map, agents)

solver_settings = SolverSettings(goal_occupation_time=100)
solver = SolverAStarOD(solver_settings)

paths = solver.solve(problem_instance, verbose=True)

root = Tk()
frame = Frame(root)
frame.pack()
problem_instance.plot_on_gui(frame, paths=paths)

root.mainloop()

"""