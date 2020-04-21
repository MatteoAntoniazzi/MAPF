from GUI import plot_paths
from MAPFSolver import *


n_of_agents = 20
buckets_size = 20


print("----------------------------------------------------------------------------------------------------")

total_nodes = 0
total_exp_nodes = 0
total_time = 0
total_cost = 0
failed_times = 0

prefix_str = "Solving instances of " + str(n_of_agents) + " agents:"
print_progress_bar(0, buckets_size, prefix=prefix_str, suffix='Complete', length=50)

problem_instances = []
problem_paths = []
solver_settingss = []

for k in range(buckets_size):

    problem_map = generate_random_map(32, 32, 0.2)
    problem_agents = generate_random_agents(problem_map, n_of_agents)
    problem_instance = ProblemInstance(problem_map, problem_agents)
    solver_settings = SolverSettings(heuristic="AbstractDistance", objective_function="SOC", stay_at_goal=True,
                                     goal_occupation_time=1, edge_conflict=True, time_out=450)

    solver = MStarSolver(solver_settings)

    paths, output_infos = solver.solve(problem_instance, verbose=False, return_infos=True)

    problem_instances.append(problem_instance)
    problem_paths.append(paths)
    solver_settingss.append(solver_settings)

    if paths:
        total_nodes += output_infos["generated_nodes"]
        total_exp_nodes += output_infos["expanded_nodes"]
        total_time += output_infos["computation_time"]
        total_cost += output_infos["sum_of_costs"]
    else:
        failed_times += 1

    print_progress_bar(k + 1, buckets_size, prefix=prefix_str, suffix='Complete', length=50)

print("----------------------------------------------------------------------------------------------------")
if failed_times == buckets_size:
    print("NESSUN SUCCESSO CON QUESTO TIME OUT")
else:
    print("Number of agents:    {:d}".format(n_of_agents))
    print("Number of nodes:     {:0.1f}".format(total_nodes / (buckets_size - failed_times)))
    print("Number of exp nodes: {:0.1f}".format(total_exp_nodes / (buckets_size - failed_times)))
    print("Time:                {:0.5f}".format(total_time / (buckets_size - failed_times)))
    print("Cost:                {:0.2f}".format(total_cost / (buckets_size - failed_times)))
    print("SUCCESS:             {:d} of {:d}".format((buckets_size - failed_times), buckets_size))
print("----------------------------------------------------------------------------------------------------")

for k in range(buckets_size):
    plot_paths(problem_instances[k], solver_settingss[k], problem_paths[k])


"""root = Tk()
frame = Frame(root)
frame.pack()
problem_instance.plot_on_gui(frame, paths=paths)

root.mainloop()"""

