from MAPFSolver.SearchBasedAlgorithms.AStarOD.AStarODSolver import AStarODSolver
from MAPFSolver.SearchBasedAlgorithms.AStar.AStarSolver import AStarSolver
from MAPFSolver.SearchBasedAlgorithms.CBS.CBSSolver import CBSSolver
from MAPFSolver.SearchBasedAlgorithms.CooperativeAStar.CoopAStarSolver import CoopAStarSolver
from MAPFSolver.SearchBasedAlgorithms.ICTS.ICTSSolver import ICTSSolver
from MAPFSolver.SearchBasedAlgorithms.MStar.MStarSolver import MStarSolver
from MAPFSolver.Utilities.problem_generation import generate_random_map
from MAPFSolver.Utilities.ProblemInstance import ProblemInstance
from MAPFSolver.Utilities.SolverSettings import SolverSettings
from MAPFSolver.Utilities.Agent import Agent
from tkinter import *

from GUI.start_simulation import plot_on_gui

problem_map = generate_random_map(8, 8, 0)
#problem_agents = [Agent(0, (0, 0), (2, 1)), Agent(1, (3, 0), (1, 1))]
problem_agents = [Agent(0, (6, 6), (0, 4)), Agent(1, (2, 0), (4, 6)), Agent(2, (3, 6), (4, 3))]

problem_instance = ProblemInstance(problem_map, problem_agents)

solver_settings = SolverSettings(objective_function="SOC", stay_in_goal=True,  goal_occupation_time=5,
                                 is_edge_conflict=True)
solver = ICTSSolver(solver_settings)

paths = solver.solve(problem_instance, verbose=True)
print(paths)

root = Tk()
frame = Frame(root)
frame.pack()
plot_on_gui(problem_instance, frame, paths=paths)

root.mainloop()


'''
RESULTS:    stay        not stay    1       2       3       4       5
A*:         30,9                    30,10   30,9    30,9    30,9    30,9
A*+OD:      30,10                   30,10   30,10   30,10   30,10   30,10
'''