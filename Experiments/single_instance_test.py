import pathlib

from MAPFSolver import *
from GUI import plot_paths
from multiprocessing import Process
import time


root_path = pathlib.Path(__file__).parent.parent.parent
#map_path = str(root_path / "MAPF/Maps/test_maps/" / "teobellu.map")
map_path = str(root_path / "MAPF/Maps/maps/" / "empty-8-8.map")
print(map_path)
problem_map = load_map_from_file(map_path)

problem_agents = [Agent(0, (1,1), (2,2))]
#problem_agents = [Agent(0, (19,10), (1,1))]
#problem_agents = [Agent(0, (1,5), (0,1)), Agent(1, (2,10), (7,6)), Agent(2, (3,4), (19,7)), Agent(3, (3,9), (0,4)),
#                  Agent(4, (14,6), (12,6)), Agent(5, (16,4), (11,6)), Agent(6, (6,5), (2,5))]

#problem_agents = [Agent(0, (0,0), (2,6)), Agent(1, (14,4), (6,6)), Agent(2, (9,2), (11,5)), Agent(3, (16,10), (1,6)),
#                  Agent(4, (10,4), (14,0)), Agent(5, (4,5), (15,8)), Agent(6, (4,7), (15,10))]

#problem_agents = [Agent(0, (6,2), (15,2)), Agent(1, (7,9), (1,3)), Agent(2, (9,0), (12,5)), Agent(3, (2,1), (1,6)),
#                  Agent(4, (1,0), (6,9)), Agent(5, (14,5), (19,0)), Agent(6, (5,6), (8,10))]

#problem_map = generate_random_map(8, 8, 0)

#problem_agents = [Agent(0, (0, 0), (2, 1)), Agent(1, (3, 0), (1, 1))]
# problem_agents = [Agent(0, (6, 6), (0, 4)), Agent(1, (2, 0), (4, 6)), Agent(2, (3, 6), (4, 3)), Agent(3, (0, 2), (7, 4))]
# problem_agents = [Agent(0, (6, 6), (0, 4)), Agent(1, (2, 0), (4, 6)), Agent(2, (3, 6), (4, 3)), Agent(3, (0, 2), (7, 4)),
#                   Agent(4, (6, 4), (0, 7)), Agent(5, (2, 1), (4, 7)), Agent(6, (3, 7), (4, 1)), Agent(7, (0, 0), (7, 5))]

# problem_agents = [Agent(0, (1, 2), (1, 2)), Agent(1, (1, 1), (0, 2)), Agent(2, (0, 2), (0, 1))]

problem_instance = ProblemInstance(problem_map, problem_agents)

#problem_instance = generate_problem_m_star_slides()

solver_settings = SolverSettings(heuristic="AbstractDistance", objective_function="SOC", stay_at_goal=True,
                                 goal_occupation_time=1, edge_conflict=False)
solver = AStarODSolver(solver_settings)

paths = solver.solve(problem_instance, verbose=True, time_out=None)
for i, path in enumerate(paths):
    print("PATH", i, ": ", path)

plot_paths(problem_instance, solver_settings, paths)


'''
RESULTS:    stay        not stay    1       2       3       4       5
A*:         30,9                    30,10   30,9    30,9    30,9    30,9
A*+OD:      30,10                   30,10   30,10   30,10   30,10   30,10
'''