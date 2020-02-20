from MAPFSolver import *
from GUI import plot_paths


problem_map = generate_random_map(3, 3, 0)

# problem_agents = [Agent(0, (0, 0), (2, 1)), Agent(1, (3, 0), (1, 1))]
# problem_agents = [Agent(0, (6, 6), (0, 4)), Agent(1, (2, 0), (4, 6)), Agent(2, (3, 6), (4, 3)), Agent(3, (0, 2), (7, 4))]
# problem_agents = [Agent(0, (6, 6), (0, 4)), Agent(1, (2, 0), (4, 6)), Agent(2, (3, 6), (4, 3)), Agent(3, (0, 2), (7, 4)),
#                   Agent(4, (6, 4), (0, 7)), Agent(5, (2, 1), (4, 7)), Agent(6, (3, 7), (4, 1)), Agent(7, (0, 0), (7, 5))]

problem_agents = [Agent(0, (1, 2), (1, 2)), Agent(1, (1, 1), (0, 2)), Agent(2, (0, 2), (0, 1))]

problem_instance = ProblemInstance(problem_map, problem_agents)

#problem_instance = generate_problem_m_star_slides()

solver_settings = SolverSettings(heuristic="RRA", objective_function="SOC", stay_in_goal=True,  goal_occupation_time=1,
                                 is_edge_conflict=True)
solver = AStarSolver(solver_settings)

paths = solver.solve(problem_instance, verbose=True, time_out=None)
print(paths)

plot_paths(problem_instance, solver_settings, paths)


'''
RESULTS:    stay        not stay    1       2       3       4       5
A*:         30,9                    30,10   30,9    30,9    30,9    30,9
A*+OD:      30,10                   30,10   30,10   30,10   30,10   30,10
'''