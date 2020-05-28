import pathlib

from MAPFSolver import *
from GUI import plot_paths


maps_paths = []

root_path = pathlib.Path(__file__).parent.parent.parent
map_path = str(root_path / "MAPF/Maps/test_maps/" / "presentation.map")

problem_map = load_map_from_file(map_path)
problem_agents = [Agent(0, (1, 2), (7, 6)), Agent(1, (4, 4), (2, 1)), Agent(2, (7, 4), (17, 6)),
                  Agent(3, (10, 3), (3, 6)), Agent(4, (11, 6), (10, 1)), Agent(5, (16, 6), (5, 5))]
problem_instance = ProblemInstance(problem_map, problem_agents)


#problem_instance = generate_problem_m_star_slides()

solver_settings = SolverSettings(heuristic="AbstractDistance", objective_function="SOC", stay_at_goal=True,
                                 goal_occupation_time=1, edge_conflict=True, time_out=0)

solver = CBSSolver(solver_settings)

paths = solver.solve(problem_instance, verbose=True)

print(paths)

plot_paths(problem_instance, solver_settings, paths)
