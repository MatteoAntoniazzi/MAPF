from MAPFSolver import *
from GUI import plot_paths


problem_map = generate_random_map(8, 8, 0)

# problem_agents = [Agent(0, (0, 0), (2, 1)), Agent(1, (3, 0), (1, 1))]
problem_agents = [Agent(0, (6, 6), (0, 4)), Agent(1, (2, 0), (4, 6)), Agent(2, (3, 6), (4, 3)), Agent(3, (0, 2), (7, 4))]

problem_instance = ProblemInstance(problem_map, problem_agents)

solver_settings = SolverSettings(objective_function="SOC", stay_in_goal=False,  goal_occupation_time=2,
                                 is_edge_conflict=True)
solver = AStarODSolver(solver_settings)

paths = solver.solve(problem_instance, verbose=True)
print(paths)

plot_paths(problem_instance, paths)


'''
RESULTS:    stay        not stay    1       2       3       4       5
A*:         30,9                    30,10   30,9    30,9    30,9    30,9
A*+OD:      30,10                   30,10   30,10   30,10   30,10   30,10
'''