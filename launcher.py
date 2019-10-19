from read_map_and_scenario import *
from GridWorld import *


args = setup_args()
print("Loading map")
map_width, map_height, obstacles_list = load_map_file(args.map)
print("Map Width: ", map_width, "\nMap Height: ", map_height, "\nObstacles: ", obstacles_list)


args = setup_args()
print("Loading map")
map_width, map_height, occupancy_list = load_map_file(args.map)
print("Map loaded")

print("Loading scenario file")
agents = load_scenario_file(args.scenario, occupancy_list, map_width, map_height, 20)
print("Scenario loaded")

grid_world = GridWorld(map_height, map_width, obstacles_list)
grid_world.add_agents(agents)
grid_world.print_grid_on_terminal()
grid_world.print_on_gui()
