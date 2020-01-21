"""
This class represent a node of the Increasing Cost Tree.
Every node s consists of a k-vector of individual path costs, s = [C 1 , C 2 , . . . C k ] one cost per agent. Node s
represents all possible complete solutions in which the cost of the individual path of agent a i is exactly C i.
"""
from SearchBasedAlgorithms.IncreasingCostTreeSearch.MDD import MDD
from Utilities.AStar import AStar
from Utilities.SolverSettings import SolverSettings
import itertools


class IncreasingCostTreeNode:
    def __init__(self, problem_instance, solver_settings, path_costs_vector=None, parent=None):
        self._problem_instance = problem_instance
        self._solver_settings = solver_settings
        self._parent = parent

        if parent is None:
            self._path_costs_vector = self.compute_root_path_costs_vector()
            if self._solver_settings.get_objective_function() == "Makespan":
                max_value = max(self._path_costs_vector)
                for i, agent in enumerate(self._problem_instance.get_agents()):
                    self._path_costs_vector[i] = max_value
        else:
            self._path_costs_vector = path_costs_vector


        self._solution = None
        self._mdd_vector = self.compute_mdds()
        self._total_mdd = self.compute_total_mdd()

    def expand(self):
        """
        Expand the current state.
        Based on the objective function we're using we've two cases.
        When we're minimazing the sum of costs the children nodes will be all the possible path costs vector obtained
        incrementing by one the total cost, so only one of the path costs.
        Example: node._path_cost_vector = [C1, C2, C3, ..] -> child1: [C1+1, C2, C3, ..], child2: [C1, C2+1, C3, ..], ..
        When we're minimazing the makespan  the task is to minimize the number of time steps elapsed until all agents
        reach their final positions. For this case, there is no meaning to the individual cost of a single agent.
        All agents virtually use the same amount of time steps. Thus, the size of the ICT will be linear in ∆ instead of
        exponential.
        Example: node._path_cost = 10 -> node._path_cost = 11 -> node._path_cost = 12
        :return: the list of possible next states.
        """
        candidate_list = []

        if self._solver_settings.get_objective_function() == "SOC":
            for i, agent in enumerate(self._problem_instance.get_agents()):
                path_costs = self._path_costs_vector.copy()
                path_costs[i] += 1
                candidate_list.append(IncreasingCostTreeNode(self._problem_instance, self._solver_settings,
                                                             path_costs_vector=path_costs, parent=self))

        # Adesso faccio così (10, 10, 10) espando --> (11, 11, 11) però non so se è il metodo migliore.
        # Se parte con (8, 9, 10) lo trasformo subito in (10, 10, 10)
        if self._solver_settings.get_objective_function() == "Makespan":
            path_costs = self._path_costs_vector.copy()
            print(self._path_costs_vector)
            for i, agent in enumerate(self._problem_instance.get_agents()):
                path_costs[i] += 1
            print("INCREEEEEEEEEEMMMMMMMMMMMEEEEEEEEENTTTTTOOOOOOOOOOOOOOOOOO")
            print(self._path_costs_vector)
            candidate_list.append(IncreasingCostTreeNode(self._problem_instance, self._solver_settings,
                                                         path_costs_vector=path_costs, parent=self))

        return candidate_list

    def compute_mdds(self):
        """
        Compute the mdd for each agents.
        """
        mdd_vector = []
        for i, agent in enumerate(self._problem_instance.get_agents()):
            mdd_vector.append(MDD(self._problem_instance.get_map(), agent, self._path_costs_vector[i],
                                  self._solver_settings.get_goal_occupation_time()))
        return mdd_vector

    def compute_total_mdd(self):
        """
        Compute the combined mdd by iterate over all the possible combinations of paths. Then check if exists a valid
        solution and in that case it returns it.
        """
        candidate_paths = []
        for mdd in self._mdd_vector:
            candidate_paths.append(mdd.get_paths())
        candidate_solutions = list(itertools.product(*candidate_paths))

        for solution in candidate_solutions:
            if self.check_validity(solution):
                self._solution = solution
                return solution
        return None

    def compute_root_path_costs_vector(self):
        path_costs_vector = []
        solver = AStar(SolverSettings(heuristics=self._solver_settings.get_heuristics_str()))
        for agent in self._problem_instance.get_agents():
            path = solver.find_path(self._problem_instance.get_map(), agent.get_start(), agent.get_goal())
            cost = len(path) - self._solver_settings.get_goal_occupation_time()
            path_costs_vector.append(cost)
        return path_costs_vector

    def is_goal(self):
        return self._solution is not None

    def solution(self):
        return self._solution

    def path_costs_vector(self):
        return self._path_costs_vector

    def total_cost(self):
        if self._solver_settings.get_objective_function() == "SOC":
            return sum(self._path_costs_vector)
        if self._solver_settings.get_objective_function() == "Makespan":
            return max(self._path_costs_vector)

    def check_validity(self, solution):
        """
        Check if a solution has no conflicts.
        Will be checked that:
            1. no agents occupy the same position in the same time step;
            2. no agent overlap (switch places).
        """
        reservation_table = dict()

        for i, path in enumerate(solution):
            for ts, pos in enumerate(path):
                if reservation_table.get((pos, ts)) is not None:
                    return False
                reservation_table[(pos, ts)] = i

        if self._solver_settings.get_edge_conflicts():
            for ag_i, path in enumerate(solution):
                for ts, pos in enumerate(path):
                    ag_j = reservation_table.get((pos, ts - 1))
                    if ag_j is not None and ag_j != ag_i:
                        if len(solution[ag_j]) > ts:
                            if solution[ag_j][ts] == path[ts - 1]:
                                return False

        return True
