from MAPFSolver.Utilities.MAPFSolver import MAPFSolver
from MAPFSolver.Utilities.ProblemInstance import ProblemInstance
import time

from MAPFSolver.Utilities.paths_processing import *


class IDFramework(MAPFSolver):
    """
    ID is an algorithm that is used in conjunction with a complete search algorithm such as A*, OD (Standley 2010), or
    ICTS (Sharon et al. 2011). Since these search algorithms are all exponential in the number of agents, they are
    effective only for small numbers of agents.
    In order to solve larger problems, ID partitions the agents into several smaller travel groups in such a way that
    the optimal paths found for each independent travel group do not conflict with the paths of other travel groups.
    Therefore, the paths for all travel groups constitute a solution to the entire problem.
    In simple words it works like this:
    1. Solve optimally each agent separately
    2. While some agents conflict
        2.1. Try to avoid conflict, with the same cost (NOT IMPLEMENTED HERE)
        2.2. Merge conflicting agents to one group
        2.3. Solve optimally new group
    """

    def __init__(self, solver, solver_settings):
        """
        Initialize the Independence Detection Framework with the solver to put on top of it.
        The number of generated/expanded nodes keep count of all the nodes generated/expanded during the solving. So, it
        will be the whole sum counting all the iterations.
        :param solver: solver to put on top of ID.
        :param solver_settings: settings of the solver.
        """
        super().__init__(solver_settings)
        self._solver = solver
        self._problems = []
        self._paths = []
        self._biggest_subset = 1
        self._n_of_generated_nodes = 0
        self._n_of_expanded_nodes = 0

    def solve(self, problem_instance, verbose=False, return_infos=False):
        """
        Solve the MAPF problem using the solver given in the initialization with Independence detection, returning the
        path as lists of list of (x, y) positions.
        It starts considering each agent as a singleton group, and each time a conflict between 2 groups occur it merges
        them into a new group and so the next time they will be solved together.
        The time needed is exponential in the dimension of the largest group.
        """
        start = time.time()

        if not self.initialize_paths(problem_instance):
            return False

        conflict = check_conflicts(self._paths, self._solver_settings.is_edge_conflict())
        while conflict is not None:
            self.merge_group(conflict, problem_instance, verbose=verbose)
            self.update_paths()
            conflict = check_conflicts(self._paths, self._solver_settings.is_edge_conflict())

        output_infos = self.generate_output_infos(self.calculate_soc(self._paths), self.calculate_makespan(self._paths),
                                                  self._n_of_generated_nodes, self._n_of_expanded_nodes,
                                                  time.time() - start)

        if verbose:
            print("PROBLEM SOLVED: ", output_infos)

        if return_infos:
            return self._paths, output_infos
        return self._paths

    def initialize_paths(self, problem_instance):
        """
        Initialize the groups with singleton groups. The list problem will contains the single agent problem for each
        agent. Solve the problems in this way and return the paths (with possible conflicts).
        """
        for agent in problem_instance.get_original_agents():
            self._problems.append(ProblemInstance(problem_instance.get_map(), [agent]))

        for problem in self._problems:
            paths, output_infos = self._solver.solve(problem, return_infos=True)
            self._n_of_generated_nodes += output_infos["generated_nodes"]
            self._n_of_expanded_nodes += output_infos["expanded_nodes"]

            if not paths:
                return False

            self._paths.extend(paths)

        return True

    def all_agents_in_the_same_subset(self, problem_instance, verbose=False):
        """
        Return True if the dimension of the largest subset is equal to the number of agents.
        When agents are all in the same independent group found by ID.
        """
        if not self.initialize_paths(problem_instance):
            print("FFalse")
            return False

        # Check collisions
        conflict = check_conflicts(self._paths, self._solver_settings.is_edge_conflict())
        while conflict is not None:
            print("BIG:", self._biggest_subset)
            if self._biggest_subset == len(problem_instance.get_agents()):
                print("TRUE")
                return True
            self.merge_group(conflict, problem_instance, verbose=verbose)
            self.update_paths()
            conflict = check_conflicts(self._paths, self._solver_settings.is_edge_conflict())
        print("FALSE")
        return False

    def merge_group(self, conflicting_agents, problem_instance, verbose=False):
        """
        Merge the two agents into a new merged problem.
        :param conflicting_agents: ids of the agents involved in a conflict.
        :param problem_instance: instance of the problem.
        :param verbose: if True will be printed processing infos on terminal.
        :return: the merged problem.
        """
        j, k = conflicting_agents
        new_problems = []
        conflicting_problems = []

        for problem in self._problems:
            if j in problem.get_original_agents_id_list() or k in problem.get_original_agents_id_list():
                conflicting_problems.append(problem)
            else:
                new_problems.append(problem)

        merged_problem = ProblemInstance(problem_instance.get_map(), conflicting_problems[0].get_original_agents() +
                                         conflicting_problems[1].get_original_agents())
        new_problems.append(merged_problem)

        if verbose:
            print("Merged problem: {:<24} with problem: {:<24} ---> New problem: {:<24}"
                  .format(str(conflicting_problems[0].get_original_agents_id_list()),
                          str(conflicting_problems[1].get_original_agents_id_list()),
                          str(merged_problem.get_original_agents_id_list())))

        if len(merged_problem.get_original_agents_id_list()) > self._biggest_subset:
            self._biggest_subset = len(merged_problem.get_original_agents_id_list())

        self._problems = new_problems

        return merged_problem

    def update_paths(self):
        """
        Recompute the paths using the new problems configuration.
        """
        for problem in self._problems:
            paths, output_infos = self._solver.solve(problem, return_infos=True)
            self._n_of_generated_nodes += output_infos["generated_nodes"]
            self._n_of_expanded_nodes += output_infos["expanded_nodes"]

            if not paths:
                return False

            for i, path in enumerate(paths):
                self._paths[problem.get_original_agents()[i].get_id()] = path

        return True

    def get_some_conflicting_ids_for_buckets(self, problem_instance, min_n_of_agents, max_n_of_agents):
        """
        This function generate buckets from a min to a max with the ids of the conflicting agents.
        This function returns the buckets from the min to at most the max unless a problem bigger than the max is found.
        In that case this function returns less buckets.
        Example: min is 2 and max is 4. Return: [[4,7], [2,3,5], [4,7,8,9]]
        Unlucky example: min is 2 and max is 4. Return: [[4,7], [2,3,5]]
        :param problem_instance: instance of the problem.
        :param min_n_of_agents: minimum value of number of agent for which we want a bucket.
        :param max_n_of_agents: maximum value of number of agent for which we want a bucket.
        :return: k list of agent ids.
        """
        buckets_of_ids = []
        counter = min_n_of_agents

        if not self.initialize_paths(problem_instance):
            return False

        while counter < (max_n_of_agents + 1):

            self.update_paths()
            conflict = check_conflicts(self._paths, self._solver_settings.is_edge_conflict())

            if conflict is None:
                break

            merged_problem = self.merge_group(conflict, problem_instance)
            merged_problem_id_list = merged_problem.get_original_agents_id_list()
            if len(merged_problem_id_list) > counter:
                break

            if len(merged_problem_id_list) == counter:
                buckets_of_ids.append(merged_problem_id_list)
                counter += 1

        return buckets_of_ids

    def __str__(self):
        return self._solver.__str__() + " with ID Framework."
