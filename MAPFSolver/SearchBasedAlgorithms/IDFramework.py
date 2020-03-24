from MAPFSolver.Utilities.AbstractSolver import AbstractSolver
from MAPFSolver.Utilities.ProblemInstance import ProblemInstance
import time

from MAPFSolver.Utilities.paths_processing import *


class IDFramework(AbstractSolver):
    """
    Independence detection (ID) framework.
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

    def solve(self, problem_instance, verbose=False, return_infos=False, time_out=None):
        """
        Solve the MAPF problem using the solver given in the initialization with Independence detection, returning the
        path as lists of list of (x, y) positions.
        It starts considering each agent as a singleton group, and each time a conflict between 2 groups occur it merges
        them into a new group and so the next time they will be solved together.
        The time needed is exponential in the dimension of the largest group.
        """
        start = time.time()

        if not self.initialize_paths(problem_instance, time_out - (time.time() - start)):
            return False

        conflict = check_conflicts(self._paths, self._solver_settings.stay_at_goal(),
                                   self._solver_settings.is_edge_conflict())
        while conflict is not None:

            if time_out is not None:
                if (time.time() - start) > time_out:
                    output_infos = self.generate_output_infos(None, None, self._n_of_generated_nodes,
                                                              self._n_of_expanded_nodes, time.time() - start)

                    return [] if not return_infos else ([], output_infos)

            merged_problem = self.merge_group(conflict, problem_instance, verbose=verbose)

            if self.update_merged_paths(merged_problem, time_out - (time.time() - start)):
                conflict = check_conflicts(self._paths, self._solver_settings.stay_at_goal(),
                                           self._solver_settings.is_edge_conflict())
            else:
                output_infos = self.generate_output_infos(None, None, self._n_of_generated_nodes,
                                                          self._n_of_expanded_nodes, time.time() - start)

                return [] if not return_infos else ([], output_infos)

        paths = self._paths
        soc = calculate_soc(paths, self._solver_settings.stay_at_goal(),
                            self._solver_settings.get_goal_occupation_time())
        makespan = calculate_makespan(paths, self._solver_settings.stay_at_goal(),
                                      self._solver_settings.get_goal_occupation_time())
        output_infos = self.generate_output_infos(soc, makespan, self._n_of_generated_nodes,
                                                  self._n_of_expanded_nodes, time.time() - start)

        if verbose:
            print("PROBLEM SOLVED: ", output_infos)

        return self._paths if not return_infos else (self._paths, output_infos)

    def initialize_paths(self, problem_instance, time_out=None):
        """
        Initialize the groups with singleton groups. The list problem will contains the single agent problem for each
        agent. Solve the problems in this way and return the paths (with possible conflicts).
        :param problem_instance: instance of the problem to solve.
        :param time_out: maximum amount of time for solving the problems.
        :return:
        """
        start = time.time()

        for agent in problem_instance.get_original_agents():
            self._problems.append(ProblemInstance(problem_instance.get_map(), [agent]))

        for problem in self._problems:
            paths, output_infos = self._solver.solve(problem, return_infos=True, time_out=time_out-(time.time() - start))
            self._n_of_generated_nodes += output_infos["generated_nodes"]
            self._n_of_expanded_nodes += output_infos["expanded_nodes"]
            self._paths.extend(paths)

            if not paths:
                return False

        return True

    def all_agents_in_the_same_subset(self, problem_instance, verbose=False):
        """
        Return True if the dimension of the largest subset is equal to the number of agents.
        When agents are all in the same independent group found by ID.
        """
        if not self.initialize_paths(problem_instance):
            return False

        # Check collisions
        conflict = check_conflicts(self._paths, self._solver_settings.stay_at_goal(),
                                   self._solver_settings.is_edge_conflict())
        while conflict is not None:
            if self._biggest_subset == len(problem_instance.get_agents()):
                return True
            merged_problem = self.merge_group(conflict, problem_instance, verbose=verbose)
            self.update_merged_paths(merged_problem)
            conflict = check_conflicts(self._paths, self._solver_settings.stay_at_goal(),
                                       self._solver_settings.is_edge_conflict())
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

    def update_merged_paths(self, merged_problem, time_out=None):
        """
        Recompute the paths of the merged problem.
        """
        paths, output_infos = self._solver.solve(merged_problem, return_infos=True, time_out=time_out)
        if not paths:
            return False
        self._n_of_generated_nodes += output_infos["generated_nodes"]
        self._n_of_expanded_nodes += output_infos["expanded_nodes"]

        for i, agent_id in enumerate(merged_problem.get_original_agents_id_list()):
            self._paths[agent_id] = paths[i]

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
        :return: if found k list of agent ids otherwise it returns None.
        """
        list_of_buckets = []
        counter = min_n_of_agents
        merged_problem = None

        if not self.initialize_paths(problem_instance):
            return False

        while counter < (max_n_of_agents + 1):
            if merged_problem is not None:
                self.update_merged_paths(merged_problem)
            conflict = check_conflicts(self._paths, self._solver_settings.stay_at_goal(),
                                       self._solver_settings.is_edge_conflict())

            if conflict is None:
                break

            merged_problem = self.merge_group(conflict, problem_instance, verbose=False)
            merged_problem_id_list = merged_problem.get_original_agents_id_list()

            if len(merged_problem_id_list) > counter:
                break

            if len(merged_problem_id_list) == counter:
                list_of_buckets.append(merged_problem_id_list)
                counter += 1

        return list_of_buckets

    def get_dimension_of_biggest_subset(self):
        return self._biggest_subset

    def __str__(self):
        return self._solver.__str__() + " with ID Framework."
