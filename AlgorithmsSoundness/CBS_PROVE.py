from MAPFSolver.SearchBasedAlgorithms.AStar.AStarSolver import AStarSolver
from tkinter import *
from MAPFSolver.Utilities.Agent import Agent
from MAPFSolver.Utilities.Map import Map
from MAPFSolver.Utilities.ProblemInstance import ProblemInstance
from MAPFSolver.Utilities.SolverSettings import SolverSettings
from MAPFSolver.Utilities.problem_generation import *
from Utilities.Reader import Reader

problem_map = generate_random_map(8, 8, 0)

"""
agents = [Agent(0, (6,6), (0,4)), Agent(1, (2,0), (4,6)), Agent(2, (3,6), (4,3)), Agent(3, (0,2), (7,4)),
          Agent(6, (5,7), (0,1)), Agent(7, (4,7), (4,2))]
"""

"""
agents = [Agent(0, (6,6), (0,4)), Agent(1, (2,0), (4,6)), Agent(2, (3,6), (4,3)), Agent(3, (0,2), (7,4)),
          Agent(4, (7,2), (3,2)), Agent(5, (7,1), (6,5)), Agent(6, (5,7), (0,1)), Agent(7, (4,7), (4,2)),
          Agent(8, (7,7), (1,7))]
"""
agents = [Agent(0, (6,6), (0,4)), Agent(1, (2,0), (4,6)), Agent(2, (3,6), (4,3)), Agent(3, (0,2), (7,4))]

# problem_instance = ProblemInstance(problem_map, agents)

problem_instance = generate_problem_from_map_and_scene(Reader(), 4)

solver_settings = SolverSettings(heuristic="Manhattan", objective_function="SOC", stay_in_goal=False,
                                 goal_occupation_time=1, is_edge_conflict=True)
# solver = SolverIndependenceDetection(SolverConflictBasedSearch(solver_settings), solver_settings)
solver = AStarSolver(solver_settings)

print("Solve")
paths = solver.solve(problem_instance, verbose=True)
print(paths)

root = Tk()
frame = Frame(root)
frame.pack()
problem_instance.plot_on_gui(frame, paths=paths)

root.mainloop()
