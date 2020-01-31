from MAPFSolver.SearchBasedAlgorithms.AStar.AStarSolver import AStarSolver
from tkinter import *

from MAPFSolver.SearchBasedAlgorithms.IDFramework import IDFramework
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


"""agents = [Agent(0, (6,6), (0,4)), Agent(1, (2,0), (4,6)), Agent(2, (3,6), (4,3)), Agent(3, (0,2), (7,4))]

problem_instance = ProblemInstance(problem_map, agents)
solver_settings = SolverSettings(heuristic="Manhattan", objective_function="SOC", stay_in_goal=True,
                                 goal_occupation_time=1, is_edge_conflict=True)
solver = IDFramework(AStarSolver(solver_settings), solver_settings)
# solver = AStarSolver(solver_settings)

paths, output_infos = solver.solve(problem_instance, verbose=True, return_infos=True)
print(paths)"""

min_n_of_agents = 3
max_n_of_agents = 5
buckets_size = 20

problem_agents_buckets = generate_agent_buckets_with_coupling_mechanism(problem_map, True, min_n_of_agents,
                                                                        max_n_of_agents, buckets_size)

for k in range(max_n_of_agents - min_n_of_agents + 1):
    print("Solving for number of agents:", k+min_n_of_agents, " with ", buckets_size, " number of instances...")
    total_nodes = 0
    total_time = 0
    total_cost = 0

    for b in range(buckets_size):
        problem_instance = ProblemInstance(problem_map, problem_agents_buckets[k][b])
        solver_settings = SolverSettings(heuristic="Manhattan", objective_function="SOC", stay_in_goal=True,
                                         goal_occupation_time=1, is_edge_conflict=True)
        solver = IDFramework(AStarSolver(solver_settings), solver_settings)
        # solver = AStarSolver(solver_settings)

        paths, output_infos = solver.solve(problem_instance, verbose=False, return_infos=True)

        total_nodes += output_infos["generated_nodes"]
        total_time += output_infos["computation_time"]
        total_cost += output_infos["sum_of_costs"]

    print("Number of agents:", k+min_n_of_agents)
    print("Number of nodes: ", total_nodes / buckets_size)
    print("Time:            ", total_time / buckets_size)
    print("Cost:            ", total_cost / buckets_size)

"""root = Tk()
frame = Frame(root)
frame.pack()
problem_instance.plot_on_gui(frame, paths=paths)

root.mainloop()"""
