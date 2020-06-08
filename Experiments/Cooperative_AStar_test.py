import pathlib

from MAPFSolver import *
from GUI import plot_paths


maps_paths = []

for i in range(1, 11):
    root_path = pathlib.Path(__file__).parent.parent.parent
    suffix = "Cooperative_AStar_test_" + str(i) + ".map"
    map_path = str(root_path / "MAPF/Maps/test_maps/" / suffix)
    maps_paths.append(map_path)

#problem_agents = [Agent(0, (1,1), (2,2))]
#problem_agents = [Agent(0, (19,10), (1,1))]
#problem_agents = [Agent(0, (1,5), (0,1)), Agent(1, (2,10), (7,6)), Agent(2, (3,4), (19,7)), Agent(3, (3,9), (0,4)),
#                  Agent(4, (14,6), (12,6)), Agent(5, (16,4), (11,6)), Agent(6, (6,5), (2,5))]

#problem_agents = [Agent(0, (0,0), (2,6)), Agent(1, (14,4), (6,6)), Agent(2, (9,2), (11,5)), Agent(3, (16,10), (1,6)),
#                  Agent(4, (10,4), (14,0)), Agent(5, (4,5), (15,8)), Agent(6, (4,7), (15,10))]

#problem_agents = [Agent(0, (6,2), (15,2)), Agent(1, (7,9), (1,3)), Agent(2, (9,0), (12,5)), Agent(3, (2,1), (1,6)),
#                  Agent(4, (1,0), (6,9)), Agent(5, (14,5), (19,0)), Agent(6, (5,6), (8,10))]

#problem_map = generate_random_map(32, 32, 0.2)

#problem_agents = [Agent(0, (0, 0), (2, 1)), Agent(1, (3, 0), (1, 1))]
# problem_agents = [Agent(0, (6, 6), (0, 4)), Agent(1, (2, 0), (4, 6)), Agent(2, (3, 6), (4, 3)), Agent(3, (0, 2), (7, 4))]
#problem_agents = [Agent(0, (6, 6), (0, 4)), Agent(1, (2, 0), (4, 6)), Agent(2, (3, 6), (4, 3)), Agent(3, (0, 2), (7, 4)),
#                  Agent(4, (6, 4), (0, 7)), Agent(5, (2, 1), (4, 7)), Agent(6, (3, 7), (4, 1)), Agent(7, (0, 0), (7, 5))]

# problem_agents = [Agent(0, (1, 2), (1, 2)), Agent(1, (1, 1), (0, 2)), Agent(2, (0, 2), (0, 1))]


#problem_instance = generate_problem_m_star_slides()

solver_settings = SolverSettings(heuristic="AbstractDistance", objective_function="SOC", stay_at_goal=True,
                                 goal_occupation_time=1, edge_conflict=True, time_out=0)
#solver = IDFramework("Conflict Based Search", solver_settings)

#[10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

for map_path in maps_paths:
    problem_map = load_map_from_file(map_path)

    print("MAP:", map_path)

    for value in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]:

        problem_agents = generate_random_agents(problem_map, value)
        problem_instance = ProblemInstance(problem_map, problem_agents)

        solver = CooperativeAStarSolver(solver_settings)

        paths = solver.solve(problem_instance, verbose=False)

        #for i, path in enumerate(paths):
        #    print("PATH", i, ": ", path)

        empty = 0
        for path in paths:
            if not path:
                empty += 1

        print("Complete:", value-empty, " of:", value, end=".\t")

        # VECTOR OF LENGHTS
        lengths = []
        for path in paths:
            lengths.append(len(path))

        print("MIN:%-15s MAX:%-15s AVG:%-20s VECTOR:%s" % (min(lengths), max(lengths), sum(lengths) / len(lengths), lengths))

        plot_paths(problem_instance, solver_settings, paths)
