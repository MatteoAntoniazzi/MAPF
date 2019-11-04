from Utilities.read_map_and_scenario import *
from Utilities.ProblemInstance import *
from Utilities.Agent import *
from Utilities.Map import *
from CooperativeAStar.CooperativeAStar import CooperativeAStar
from CooperativeAStar.HiearachicalCooperativeAStar import HierarchicalCooperativeAStar
from AStarOD.AStarMultiAgentSolver import AStarMultiAgentSolver

import time


args = setup_args()
print("Loading map")
map_width, map_height, occupancy_list = load_map_file(args.map)
print("Map loaded")

print("Loading scenario file")
agents = load_scenario_file(args.scenario, occupancy_list, map_width, map_height, 10)
print("Scenario loaded")

map = Map(map_height, map_width, occupancy_list)

agents = [Agent(i, a[0], a[1]) for i, a in enumerate(agents)]

problem_instance = ProblemInstance(map, agents)

start_time = time.time()

solver = AStarMultiAgentSolver(problem_instance)
paths = solver.compute_paths()

print("Precessed Time {:.2f} seconds.".format(time.time() - start_time))

# problem_instance.plot_on_terminal(paths)
problem_instance.plot_on_gui(paths)
