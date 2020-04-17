import pathlib

from MAPFSolver import *

min_n_of_agents = 12
max_n_of_agents = 12
buckets_size = 500


root_path = pathlib.Path(__file__).parent.parent.parent
map_path = str(root_path / "MAPF/Maps/test_maps/" / "teobellu.map")
print(map_path)

problem_map = load_map_from_file(map_path)

problem_agents_buckets = generate_random_agent_buckets(problem_map, min_n_of_agents, max_n_of_agents, buckets_size)

print("----------------------------------------------------------------------------------------------------")
for k in range(max_n_of_agents - min_n_of_agents + 1):
    total_nodes = 0
    total_exp_nodes = 0
    total_time = 0
    total_cost = 0
    k_primo = 0
    failed_times = 0

    prefix_str = "Solving instances of " + str(k + min_n_of_agents) + " agents:"
    print_progress_bar(0, buckets_size, prefix=prefix_str, suffix='Complete', length=50)
    for b in range(buckets_size):
        problem_instance = ProblemInstance(problem_map, problem_agents_buckets[k][b])
        solver_settings = SolverSettings(heuristic="Manhattan", objective_function="SOC", stay_at_goal=True,
                                         goal_occupation_time=1, edge_conflict=False, time_out=20)

        #print(problem_instance)

        #solver = IDFramework(ICTSSolver(solver_settings), solver_settings)
        solver = CBSSolver(solver_settings)

        paths, output_infos = solver.solve(problem_instance, verbose=False, return_infos=True)

        if paths:

            #biggest_subsest = solver.get_dimension_of_biggest_subset()

            #print(output_infos)

            total_nodes += output_infos["generated_nodes"]
            total_exp_nodes += output_infos["expanded_nodes"]
            total_time += output_infos["computation_time"]
            total_cost += output_infos["sum_of_costs"]

            #k_primo += biggest_subsest

        else:
            failed_times += 1

        print_progress_bar(b+1, buckets_size, prefix=prefix_str, suffix='Complete', length=50)

    print("----------------------------------------------------------------------------------------------------")
    if failed_times == buckets_size:
        print("NESSUN SUCCESSO CON QUESTO TIME OUT")
    else:
        print("Number of agents:    {:d}".format(k+min_n_of_agents))
        print("Number of nodes:     {:0.1f}".format(total_nodes / (buckets_size - failed_times)))
        print("Number of exp nodes: {:0.1f}".format(total_exp_nodes / (buckets_size - failed_times)))
        print("Time:                {:0.5f}".format(total_time / (buckets_size - failed_times)))
        print("Cost:                {:0.2f}".format(total_cost / (buckets_size - failed_times)))
        #print("k':                  {:0.2f}".format(k_primo / (buckets_size - failed_times)))
        print("SUCCESS:             {:d} of {:d}".format((buckets_size - failed_times), buckets_size))
    print("----------------------------------------------------------------------------------------------------")

"""root = Tk()
frame = Frame(root)
frame.pack()
problem_instance.plot_on_gui(frame, paths=paths)

root.mainloop()"""
