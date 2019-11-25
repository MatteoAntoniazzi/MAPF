from Utilities.MAPFSolver import MAPFSolver
from Utilities.ProblemInstance import ProblemInstance
from Utilities.macros import *


class IndependenceDetection(MAPFSolver):
    def __init__(self, solver):
        super().__init__(None)
        self._solver = solver
        self._problems = []
        self._paths = []

    def solve(self, problem_instance, verbose=False, print_output=True):
        if not self.initialize_paths(problem_instance):
            return False

        # Check collisions
        conflict = self.check_conflicts()
        while conflict is not None:
            self.merge_group(conflict, problem_instance, verbose=verbose)
            conflict = self.check_conflicts()

        if print_output:
            print("Total time: ", max([len(path)-1 for path in self._paths]),
                  " Total cost:", sum([len(path)-GOAL_OCCUPATION_TIME for path in self._paths]))
        return self._paths

    def initialize_paths(self, problem_instance):
        for agent in problem_instance.get_agents():
            self._problems.append(ProblemInstance(problem_instance.get_map(), [agent]))

        for problem in self._problems:
            paths = self._solver.solve(problem, print_output=False)

            if not paths:
                return False
            self._paths.extend(paths)

        return True

    def merge_group(self, conflicting_agents, problem_instance, verbose=False):
        new_problems = []

        j, k = conflicting_agents

        # Get the problems with the 2 conflicted agents
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
        for problem in self._problems:
            paths = self._solver.solve(problem, print_output=False)
            if not paths:
                return False

            for i, path in enumerate(paths):
                self._paths[problem.get_agents()[i].get_id()] = path
        return True

    def check_conflicts(self):
        """
        :return: the two paths (agents) that has a conflict
        """
        # largest_time_step = max([len(path) for path in self._paths])

        reservation_table = dict()

        for i, path in enumerate(self._paths):
            for ts, pos in enumerate(path):
                if reservation_table.get((pos, ts)) is not None:
                    return reservation_table[(pos, ts)], i
                reservation_table[(pos, ts)] = i

        for ag_i, path in enumerate(self._paths):
            for ts, pos in enumerate(path):
                ag_j = reservation_table.get((pos, ts-1))  # Agent in the pos position at the previous time step
                if ag_j is not None and ag_j != ag_i:
                    if len(self._paths[ag_j]) > ts:
                        if self._paths[ag_j][ts] == path[ts-1]:
                            return ag_i, ag_j

        return None
