import copy

from MAPFSolver.Utilities.AbstractSolver import AbstractSolver
from MAPFSolver.Utilities.ProblemInstance import ProblemInstance
from MAPFSolver.Utilities.paths_processing import *
from MAPFSolver.Utilities.useful_functions import get_solver
from threading import Thread, Event
import time


class IDFramework(AbstractSolver):
    """
    Independence detection (ID) framework.
    """

    def __init__(self, solver_str, solver_settings):
        """
        Initialize the Independence Detection Framework with the solver to put on top of it.
        The number of generated/expanded nodes keep count of all the nodes generated/expanded during the solving. So, it
        will be the whole sum counting all the iterations.
        :param solver_str: string of the solver to put on top of ID.
        ["Cooperative A*", "A*", "A* with Operator Decomposition", "Increasing Cost Tree Search",
        "Conflict Based Search", "M*"]
        :param solver_settings: settings of the solver.
        """
        super().__init__(solver_settings)
        self._solver_str = solver_str
        self._problems = []
        self._paths = []
        self._biggest_subset = 1
        self._n_of_generated_nodes = 0
        self._n_of_expanded_nodes = 0
        self._solution = []

        self._start_time = None
        self._stop_event = Event()

    def solve(self, problem_instance, verbose=False, return_infos=False):
        """
        Solve the given MAPF problem with the specified algorithm with the ID framework and it returns, if exists, a
        solution.
        :param problem_instance: instance of the problem to solve.
        :param verbose: if True, infos will be printed on terminal.
        :param return_infos: if True in addition to the paths will be returned also a structure with output infos.
        :return the solution as list of paths, and, if return_infos is True, a tuple composed by the solution and a
        struct with output information.
        """
        self._start_time = time.time()
        self._stop_event = Event()
        start = time.time()

        thread = Thread(target=self.solve_problem, args=(problem_instance, verbose,))
        thread.start()
        thread.join(timeout=self._solver_settings.get_time_out())

        self._stop_event.set()

        soc = calculate_soc(self._solution, self._solver_settings.stay_at_goal(),
                            self._solver_settings.get_goal_occupation_time())
        makespan = calculate_makespan(self._solution, self._solver_settings.stay_at_goal(),
                                      self._solver_settings.get_goal_occupation_time())

        output_infos = self.generate_output_infos(soc, makespan, self._n_of_generated_nodes, self._n_of_expanded_nodes,
                                                  time.time() - start)
        if verbose:
            print("Problem ended: ", output_infos)

        return self._solution if not return_infos else (self._solution, output_infos)

    def solve_problem(self, problem_instance, verbose=False):
        """
        Solve the MAPF problem using the solver given in the initialization with Independence detection, returning the
        path as lists of list of (x, y) positions.
        It starts considering each agent as a singleton group, and each time a conflict between 2 groups occur it merges
        them into a new group and so the next time they will be solved together.
        The time needed is exponential in the dimension of the largest group.
        """
        if not self.initialize_paths(problem_instance):
            return False

        conflict = check_conflicts(self._paths, self._solver_settings.stay_at_goal(),
                                   self._solver_settings.is_edge_conflict())
        while conflict is not None:

            if self._stop_event.is_set():
                return

            merged_problem = self.merge_group(conflict, problem_instance, verbose=verbose)

            if not self.update_merged_paths(merged_problem):
                return

            conflict = check_conflicts(self._paths, self._solver_settings.stay_at_goal(),
                                       self._solver_settings.is_edge_conflict())

        self._solution = self._paths

    def initialize_paths(self, problem_instance):
        """
        Initialize the groups with singleton groups. The list problem will contains the single agent problem for each
        agent. Solve the problems in this way and return the paths (with possible conflicts).
        :param problem_instance: instance of the problem to solve.
        :return:
        """
        for agent in problem_instance.get_original_agents():
            self._problems.append(ProblemInstance(problem_instance.get_map(), [agent]))

        for problem in self._problems:
            solver_settings = copy.copy(self._solver_settings)
            solver_settings.set_time_out(self._solver_settings.get_time_out() - (time.time()-self._start_time))
            solver = get_solver(self._solver_str, solver_settings)
            paths, output_infos = solver.solve(problem, return_infos=True)
            if output_infos["generated_nodes"]:
                self._n_of_generated_nodes += output_infos["generated_nodes"]
                self._n_of_expanded_nodes += output_infos["expanded_nodes"]
            self._paths.extend(paths)

            if not paths:
                return False

        return True

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
            solver_settings = copy.copy(self._solver_settings)
            solver_settings.set_time_out(self._solver_settings.get_time_out() - (time.time()-self._start_time))
            solver = get_solver(self._solver_str, solver_settings)
            paths, output_infos = solver.solve(problem, return_infos=True)
            self._n_of_generated_nodes += output_infos["generated_nodes"]
            self._n_of_expanded_nodes += output_infos["expanded_nodes"]

            if not paths:
                return False

            for i, path in enumerate(paths):
                self._paths[problem.get_original_agents()[i].get_id()] = path

        return True

    def update_merged_paths(self, merged_problem):
        """
        Recompute the paths of the merged problem.
        """
        solver_settings = copy.copy(self._solver_settings)
        solver_settings.set_time_out(self._solver_settings.get_time_out() - (time.time()-self._start_time))
        solver = get_solver(self._solver_str, solver_settings)
        paths, output_infos = solver.solve(merged_problem, return_infos=True)
        if not paths:
            return False
        if output_infos["generated_nodes"]:
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
        self._start_time = time.time()

        list_of_buckets = []
        counter = min_n_of_agents
        merged_problem = None

        if not self.initialize_paths(problem_instance):
            return False

        while counter < (max_n_of_agents + 1):
            if merged_problem is not None:
                if not self.update_merged_paths(merged_problem):
                    return False

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
        """
        Return the dimension of the biggest subset.
        """
        return self._biggest_subset

    def __str__(self):
        return self._solver_str + " with ID Framework."


