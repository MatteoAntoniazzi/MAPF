from AStar import AStar
from Utilities.macros import *


class ConstraintTreeNode:
    def __init__(self, problem_instance, constraints_set=None, transactional_constraints=None, previous_solution=None,
                 agent_to_recompute=None, parent=None, heuristics_str="Manhattan"):

        self._problem_instance = problem_instance
        self._heuristics_str = heuristics_str
        self._parent = parent
        if constraints_set is None:
            self._constraints = set()
        else:
            self._constraints = constraints_set
        if transactional_constraints is None:
            self._transactional_constraints = set()
        else:
            self._transactional_constraints = transactional_constraints

        # self._solution = self.low_level_search()  # paths


        if agent_to_recompute is None:
            self._solution = self.low_level_search()  # paths
        else:
            self._solution = previous_solution
            path = self.single_agent_low_level_search(self._problem_instance.get_agents()[agent_to_recompute])
            self._solution[agent_to_recompute] = path

        self._total_cost = self.calculate_cost()

    def low_level_search(self):
        solution = []
        # Low level search considering the Constraints
        for agent in self._problem_instance.get_agents():
            path = self.single_agent_low_level_search(agent)
            solution.append(path)
        return solution

    def single_agent_low_level_search(self, agent):

        agent_constraints = []
        for constraint in self._constraints:
            agent_id, pos, ts = constraint
            if agent_id == agent.get_id():
                agent_constraints.append((pos, ts))

        agent_transactional_constraints = []
        for constraint in self._transactional_constraints:
            agent_id, pos_i, pos_f, ts = constraint
            if agent_id == agent.get_id():
                agent_transactional_constraints.append((pos_i, pos_f, ts))

        solver = AStar(self._heuristics_str)
        path = solver.find_path_with_constraints(self._problem_instance.get_map(), agent.get_start(),
                                                 agent.get_goal(), agent_constraints,
                                                 agent_transactional_constraints)

        return path

    def calculate_cost(self):
        return sum([len(path)-GOAL_OCCUPATION_TIME for path in self._solution])

    def total_cost(self):
        return self._total_cost

    def total_time(self):
        return max([len(path)-1 for path in self._solution])

    def constraints(self):
        return self._constraints

    def transactional_constraints(self):
        return self._transactional_constraints

    def solution(self):
        return self._solution

    def check_conflicts(self):
        """
        :return: the new possible constraint (ai, aj, v, t) -> as [(ai, v, t), (aj, v, t)] otherwise None
        In the case of an intersection it returns: [(ai, pos1, t), (aj, pos2, t)]
        In  the transactional case [(ai, pos_i, pos_f, ts_f), (aj, pos_i, pos_f, ts_f)]
        """
        reservation_table = dict()

        for ag_i, path in enumerate(self._solution):
            for ts, pos in enumerate(path):
                if reservation_table.get((pos, ts)) is not None:
                    return 'INPLACE', [(reservation_table[(pos, ts)], pos, ts), (ag_i, pos, ts)]  # [(ai, v, t), (aj, v, t)]
                reservation_table[(pos, ts)] = ag_i

        for ag_i, path in enumerate(self._solution):
            for ts, pos in enumerate(path):
                ag_j = reservation_table.get((pos, ts-1))  # Agent in the pos position at the previous time step
                if ag_j is not None and ag_j != ag_i:
                    if len(self._solution[ag_j]) > ts:
                        if self._solution[ag_j][ts] == path[ts-1]:
                            return 'TRANSACTIONAL', [(ag_j, self._solution[ag_j][ts-1], self._solution[ag_j][ts], ts),
                                                     (ag_i, path[ts-1], path[ts], ts)]
        return None
    # This code returns at most 2 agents. We can do the version with more agents but it's similar

    def expand(self):
        conflict_type, constraints = self.check_conflicts()

        node_a, node_b = None, None

        if conflict_type == 'INPLACE':
            agent, pos, ts = constraints[0]
            constraints_a = self._constraints.copy()
            constraints_a.add(constraints[0])
            node_a = ConstraintTreeNode(self._problem_instance, constraints_set=constraints_a,
                                        transactional_constraints=self._transactional_constraints.copy(),
                                        previous_solution=self._solution.copy(), agent_to_recompute=agent, parent=self,
                                        heuristics_str=self._heuristics_str)

            agent, pos, ts = constraints[1]
            constraints_b = self._constraints.copy()
            constraints_b.add(constraints[1])
            node_b = ConstraintTreeNode(self._problem_instance, constraints_set=constraints_b,
                                        transactional_constraints=self._transactional_constraints.copy(),
                                        previous_solution=self._solution.copy(), agent_to_recompute=agent, parent=self,
                                        heuristics_str=self._heuristics_str)

        if conflict_type == 'TRANSACTIONAL':
            agent, pos_i, pos_f, ts = constraints[0]
            constraints_a = self._transactional_constraints.copy()
            constraints_a.add(constraints[0])
            node_a = ConstraintTreeNode(self._problem_instance, constraints_set=self._constraints.copy(),
                                        transactional_constraints=constraints_a,
                                        previous_solution=self._solution.copy(), agent_to_recompute=agent, parent=self,
                                        heuristics_str=self._heuristics_str)

            agent, pos_i, pos_f, ts = constraints[1]
            constraints_b = self._transactional_constraints.copy()
            constraints_b.add(constraints[1])
            node_b = ConstraintTreeNode(self._problem_instance, constraints_set=self._constraints.copy(),
                                        transactional_constraints=constraints_b,
                                        previous_solution=self._solution.copy(), agent_to_recompute=agent, parent=self,
                                        heuristics_str=self._heuristics_str)
        return [node_a, node_b]

    def __str__(self):
        string = '[Constraints:' + str(self._constraints) + \
                 ' Transactional constraints:' + str(self._transactional_constraints) + \
                 ' Total Cost:' + str(self._total_cost) + \
                 ' PATH:' + str(self._solution) + ']'
        return string
