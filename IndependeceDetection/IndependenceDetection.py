from Solver import Solver
from CooperativeAStar.AStar import AStar
from AStarOD.AStarOD import AStarOD
from Utilities.ProblemInstance import ProblemInstance
from CooperativeAStar.CooperativeAStar import CooperativeAStar
from CooperativeAStar.HiearachicalCooperativeAStar import HierarchicalCooperativeAStar
from AStarOD.AStarMultiAgent import AStarMultiAgent
from Utilities.Agent import Agent


class IndependenceDetection(Solver):
    def __init__(self, problem_instance):
        super().__init__(problem_instance)
        self._paths = []
        self._problems = []
        self._solver = None

    def compute_paths(self):
        if not self.initialize_paths():
            return False

        # Check collisions
        conflict = self.check_conflicts()

        while conflict is not None:
            self.merge_group(conflict)
            conflict = self.check_conflicts()

        return self._paths

    def initialize_paths(self):
        for agent in self._problem_instance.get_agents():
            self._problems.append(ProblemInstance(self._problem_instance.get_map(), [agent]))

        for problem in self._problems:
            solver = AStarMultiAgent(problem)
            paths = solver.compute_paths()
            if not paths:
                return False
            self._paths.extend(paths)
        return True

    def merge_group(self, conflicting_agents):
        new_problems = []

        j, k = conflicting_agents

        # Get the problems with the 2 conflicted agents
        conflicting_problems = []
        for problem in self._problems:
            if j in problem.get_agents_id_list() or k in problem.get_agents_id_list():
                conflicting_problems.append(problem)
            else:
                new_problems.append(problem)

        merged_problem = ProblemInstance(self._problem_instance.get_map(),
                                         conflicting_problems[0].get_agents() + conflicting_problems[1].get_agents())

        new_problems.append(merged_problem)

        self._problems = new_problems
        self.update_paths()

    def update_paths(self):
        for problem in self._problems:
            solver = CooperativeAStar(problem)
            print("PPPPPPPPP", problem.get_agents_id_list())
            paths = solver.compute_paths()
            print("dioc")

            if not paths:
                return False

            for i, path in enumerate(paths):
                self._paths[problem.get_agents()[i].get_id()] = path
        return True

    def check_conflicts(self):
        """
        :return: the two paths (agents) that has a conflict
        """
        largest_time_step = max([len(path) for path in self._paths])

        reservation_table = dict()

        for i, path in enumerate(self._paths):
            for ts, pos in enumerate(path):
                if reservation_table.get((pos, ts)) is not None:
                    print("CONFLICT IN:", pos, "at", ts, "BETWEEN", (reservation_table[(pos, ts)], i))
                    return reservation_table[(pos, ts)], i
                reservation_table[(pos, ts)] = i
                if ts == len(path)-1 and ts < largest_time_step:
                    for j in range(ts+1, largest_time_step):
                        reservation_table[(pos, j)] = i

        return None
