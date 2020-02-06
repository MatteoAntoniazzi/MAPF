from MAPFSolver.SearchBasedAlgorithms.CBS.CBSSolver import CBSSolver
from MAPFSolver.Utilities.problem_generation import *

min_n_of_agents = 3
max_n_of_agents = 5
buckets_size = 100

problem_map = generate_random_map(8, 8, 0)
problem_agents_buckets = generate_random_agent_buckets(problem_map, min_n_of_agents,
                                                                        max_n_of_agents, buckets_size)

print("----------------------------------------------------------------------------------------------------")

for k in range(max_n_of_agents - min_n_of_agents + 1):
    total_nodes = 0
    total_time = 0
    total_cost = 0

    prefix_str = "Solving instances of " + str(k + min_n_of_agents) + " agents:"
    print_progress_bar(0, buckets_size, prefix=prefix_str, suffix='Complete', length=50)
    for b in range(buckets_size):
        problem_instance = ProblemInstance(problem_map, problem_agents_buckets[k][b])
        solver_settings = SolverSettings(heuristic="Manhattan", objective_function="SOC", stay_in_goal=True,
                                         goal_occupation_time=1, is_edge_conflict=True)
        # solver = IDFramework(AStarODSolver(solver_settings), solver_settings)
        solver = CBSSolver(solver_settings)

        paths, output_infos = solver.solve(problem_instance, verbose=False, return_infos=True)

        total_nodes += output_infos["generated_nodes"]
        total_time += output_infos["computation_time"]
        total_cost += output_infos["sum_of_costs"]

        print_progress_bar(b+1, buckets_size, prefix=prefix_str, suffix='Complete', length=50)

    print("----------------------------------------------------------------------------------------------------")
    print("Number of agents:", k+min_n_of_agents)
    print("Number of nodes: ", total_nodes / buckets_size)
    print("Time:            ", total_time / buckets_size)
    print("Cost:            ", total_cost / buckets_size)
    print("----------------------------------------------------------------------------------------------------")

"""root = Tk()
frame = Frame(root)
frame.pack()
problem_instance.plot_on_gui(frame, paths=paths)

root.mainloop()"""
