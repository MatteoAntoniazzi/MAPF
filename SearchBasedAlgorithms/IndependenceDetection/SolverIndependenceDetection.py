"""
ID is an algorithm that is used in conjunction with a complete search algorithm such as A*, OD (Standley 2010), or
ICTS (Sharon et al. 2011). Since these search algorithms are all exponential in the number of agents, they are effective
only for small numbers of agents.
In order to solve larger problems, ID partitions the agents into several smaller travel groups in such a way that the
optimal paths found for each independent travel group do not conflict with the paths of other travel groups. Therefore,
the paths for all travel groups constitute a solution to the entire problem.

In simple words it works like this:
1. Solve optimally each agent separately
2. While some agents conflict
    2.1. Try to avoid conflict, with the same cost (NOT IMPLEMENTED HERE)
    2.2. Merge conflicting agents to one group
    2.3. Solve optimally new group
"""
from Utilities.MAPFSolver import MAPFSolver
from Utilities.ProblemInstance import ProblemInstance
import time


class SolverIndependenceDetection(MAPFSolver):
    def __init__(self, solver, solver_settings):
        super().__init__(solver_settings)
        self._solver = solver
        self._problems = []
        self._paths = []

    def solve(self, problem_instance, verbose=False, print_output=True, return_infos=False):
        """
        Solve the MAPF problem using the desired algorithm with Independence detection, returning the path as lists of
        list of (x, y) positions.
        It starts considering each agent as a singleton group, and each time a conflict between 2 groups occur it merges
        them into a new group and so the next time they will be solved together.
        The time needed is exponential in the dimension of the largest group.
        """
        start = time.time()

        if not self.initialize_paths(problem_instance):
            return False

        # Check collisions
        conflict = self.check_conflicts()
        while conflict is not None:
            self.merge_group(conflict, problem_instance, verbose=verbose)
            conflict = self.check_conflicts()

        if print_output:
            print("Total time: ", max([len(path)-1 for path in self._paths]),
                  " Total cost:", sum([len(path)-self._solver_settings.get_goal_occupation_time() for path in self._paths]))

        if return_infos:
            output_infos = {
                "sum_of_costs": sum([len(path)-self._solver_settings.get_goal_occupation_time() for path in self._paths]),
                "makespan": max([len(path)-1 for path in self._paths]),
                "expanded_nodes": 0,
                "computation_time": time.time() - start
            }
            return self._paths, output_infos

        return self._paths

    def initialize_paths(self, problem_instance):
        """
        Initialize the groups with singleton groups. The list problem will contains the single agent problem for each
        agent. Solve the problems in this way and return the paths (with possible conflicts).
        """
        for agent in problem_instance.get_agents():
            self._problems.append(ProblemInstance(problem_instance.get_map(), [agent]))

        for problem in self._problems:
            paths = self._solver.solve(problem, print_output=False, return_infos=False)

            if not paths:
                return False
            self._paths.extend(paths)

        return True

    def merge_group(self, conflicting_agents, problem_instance, verbose=False):
        """
        Merge the two agents into a new merged problem.
        """
        new_problems = []

        j, k = conflicting_agents

        conflicting_problems = []
        for problem in self._problems:
            if j in problem.get_agents_id_list() or k in problem.get_agents_id_list():
                conflicting_problems.append(problem)
            else:
                new_problems.append(problem)

        merged_problem = ProblemInstance(problem_instance.get_map(),
                                         conflicting_problems[0].get_agents() + conflicting_problems[1].get_agents())

        new_problems.append(merged_problem)

        if verbose:
            print("Merged problem: {:<24} with problem: {:<24} ---> New problem: {:<24}"
                  .format(str(conflicting_problems[0].get_agents_id_list()),
                          str(conflicting_problems[1].get_agents_id_list()),
                          str(merged_problem.get_agents_id_list())))

        self._problems = new_problems
        self.update_paths()

    def update_paths(self):
        """
        Recompute the paths using the new problems configuration.
        """
        for problem in self._problems:
            paths = self._solver.solve(problem, print_output=False)
            if not paths:
                return False

            for i, path in enumerate(paths):
                self._paths[problem.get_agents()[i].get_id()] = path
        return True

    def check_conflicts(self):
        """
        Return the two paths (agents) that has a conflict
        """
        reservation_table = dict()

        for i, path in enumerate(self._paths):
            for ts, pos in enumerate(path):
                if reservation_table.get((pos, ts)) is not None:
                    return reservation_table[(pos, ts)], i
                reservation_table[(pos, ts)] = i

        if self._solver_settings.get_edge_conflicts():
            for ag_i, path in enumerate(self._paths):
                for ts, pos in enumerate(path):
                    ag_j = reservation_table.get((pos, ts-1))
                    if ag_j is not None and ag_j != ag_i:
                        if len(self._paths[ag_j]) > ts:
                            if self._paths[ag_j][ts] == path[ts-1]:
                                return ag_i, ag_j

        return None

    def __str__(self):
        return self._solver.__str__() + " with Independence Detection"