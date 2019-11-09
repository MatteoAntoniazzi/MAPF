from Solvers.MAPFSolver import MAPFSolver
from Utilities.ProblemInstance import ProblemInstance


class IndependenceDetection(MAPFSolver):
    def __init__(self, solver):
        super().__init__(None)
        self._solver = solver
        self._problems = []
        self._paths = []

    def solve(self, problem_instance, verbose=False):
        print("STEP A")
        if not self.initialize_paths(problem_instance):
            return False
        print("STEP B")

        # Check collisions
        conflict = self.check_conflicts()
        while conflict is not None:
            self.merge_group(conflict, problem_instance, verbose=verbose)
            conflict = self.check_conflicts()
        print("STEP C")

        print("Total time: ", max([len(path)-1 for path in self._paths]),
              " Total cost:", sum([len(path)-1 for path in self._paths]))
        return self._paths

    def initialize_paths(self, problem_instance):
        for agent in problem_instance.get_agents():
            self._problems.append(ProblemInstance(problem_instance.get_map(), [agent]))

        for problem in self._problems:
            paths = self._solver.solve(problem)
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
            paths = self._solver.solve(problem)
            print(paths)
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
                # if ts == len(path)-1 and ts < largest_time_step:    --> dovrebbe essere quello vecchio per tenere occupata la posizione
                #     for j in range(ts+1, largest_time_step):
                #         reservation_table[(pos, j)] = i

        return None
