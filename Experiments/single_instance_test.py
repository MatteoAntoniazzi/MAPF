import pathlib

from MAPFSolver import *
from GUI import plot_paths


maps_paths = []

root_path = pathlib.Path(__file__).parent.parent.parent
map_path = str(root_path / "MAPF/Maps/maps/" / "narrow_corridor.map")

problem_map = load_map_from_file(map_path)
problem_agents = [Agent(0, (0,0), (8,0)), Agent(1, (1,0), (7,0))]
problem_instance = ProblemInstance(problem_map, problem_agents)


#problem_instance = generate_problem_m_star_slides()

solver_settings = SolverSettings(heuristic="AbstractDistance", objective_function="SOC", stay_at_goal=True,
                                 goal_occupation_time=1, edge_conflict=True, time_out=0)

solver = CooperativeAStarSolver(solver_settings)

paths = solver.solve(problem_instance, verbose=True)

print(paths)

plot_paths(problem_instance, solver_settings, paths)
