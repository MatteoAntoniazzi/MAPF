from Utilities.read_map_and_scenario import *
from Utilities.ProblemInstance import *
from Utilities.Agent import *
from Utilities.Map import *
from Solvers.AStarSingleAgent import AStarSingleAgent
from Solvers.AStarMultiAgent import AStarMultiAgent
from Solvers.AStarOD import AStarOD
from Solvers.CooperativeAStar import CooperativeAStar
from Solvers.IndependenceDetection import IndependenceDetection
from ConflictBasedSearch.ConflictBasedSearch import ConflictBasedSearch
from IncreasingCostTreeSearch.IncreasingCostTreeSearch import IncreasingCostTreeSearch

import time


args = setup_args()
print("Loading map")
map_width, map_height, occupancy_list = load_map_file(args.map)
print("Map loaded")

print("Loading scenario file")
agents = load_scenario_file(args.scenario, occupancy_list, map_width, map_height, 40)
print("Scenario loaded")

map = Map(map_height, map_width, occupancy_list)

agents = [Agent(i, a[0], a[1]) for i, a in enumerate(agents)]

problem_instance = ProblemInstance(map, agents)

start_time = time.time()

# solver = IndependenceDetection(ConflictBasedSearch("RRA"))
solver = AStarSingleAgent("Manhattan")
paths = solver.solve(problem_instance, verbose=True)

print("Precessed Time {:.2f} seconds.".format(time.time() - start_time))

print(paths)

# problem_instance.plot_on_terminal(paths)
problem_instance.plot_on_gui(paths)
