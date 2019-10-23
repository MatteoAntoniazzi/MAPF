from Utilities.read_map_and_scenario import *
from Utilities.ProblemInstance import *
from Utilities.Agent import *
from Utilities.GridMap import *
from a_star import *


args = setup_args()
print("Loading map")
map_width, map_height, occupancy_list = load_map_file(args.map)
print("Map loaded")

print("Loading scenario file")
agents = load_scenario_file(args.scenario, occupancy_list, map_width, map_height, 20)
print("Scenario loaded")

grid_map = GridMap(map_height, map_width, occupancy_list)

agents = [Agent(i, a[0], a[1]) for i, a in enumerate(agents)]

grid_instance = ProblemInstance(grid_map, agents)
grid_instance.plot_on_terminal()
grid_instance.plot_on_gui()

