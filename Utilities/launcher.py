from Utilities.read_map_and_scenario import *
from Utilities.ProblemInstance import *
from Utilities.Agent import *
from Utilities.Map import *
from AStarSingleAgentSolver import AStarSingleAgentSolver
from AStarMultiAgentSolver import AStarMultiAgentSolver


args = setup_args()
print("Loading map")
map_width, map_height, occupancy_list = load_map_file(args.map)
print("Map loaded")

print("Loading scenario file")
agents = load_scenario_file(args.scenario, occupancy_list, map_width, map_height, 8)
print("Scenario loaded")

map = Map(map_height, map_width, occupancy_list)

agents = [Agent(i, a[0], a[1]) for i, a in enumerate(agents)]

problem_instance = ProblemInstance(map, agents)

solver = AStarMultiAgentSolver(problem_instance)
paths = solver.compute_paths()

print(paths)

problem_instance.plot_on_terminal(paths)
problem_instance.plot_on_gui(paths)

