"""
This class represents a single node of the constraint tree. It contains a set of constraints that the solution must
respect. In addition, there's also a set of transactional constraints in order to avoid that the move where two agents
switch places is not allowed. The attributes previous solution and agent_to_recompute are used to speed up the process
and avoid to recompute each time the path for each agent.
"""
from Utilities.AStar import AStar
from Utilities.SolverSettings import SolverSettings
from Utilities.macros import *


class ConstraintTreeNode:
    def __init__(self, problem_instance, solver_settings, constraints_set=None, transactional_constraints=None, previous_solution=None,
                 agent_to_recompute=None, parent=None):

        self._problem_instance = problem_instance
        self._solver_settings = solver_settings
        self._parent = parent
        if constraints_set is None:
            self._constraints = set()
        else:
            self._constraints = constraints_set
        if transactional_constraints is None:
            self._transactional_constraints = set()
        else:
            self._transactional_constraints = transactional_constraints

        if agent_to_recompute is None:
            self._solution = self.low_level_search()  # paths
        else:
            self._solution = previous_solution
            path = self.single_agent_low_level_search(self._problem_instance.get_agents()[agent_to_recompute])
            self._solution[agent_to_recompute] = path

        self._total_cost = self.calculate_cost()

    def low_level_search(self):
        """
        Low level search. For every agent it searches a possible valid path using A* which doesn't violate the set of
        constraints.
        """
        solution = []
        for agent in self._problem_instance.get_agents():
            path = self.single_agent_low_level_search(agent)
            solution.append(path)
        return solution

    def single_agent_low_level_search(self, agent):
        """
        Low level search for a single agent. It searches a possible valid path using A* which doesn't violate the set
        of constraints.
        """
        agent_constraints = []
        for constraint in self._constraints:
            agent_id, pos, ts = constraint
            if agent_id == agent.get_id():
                agent_constraints.append((pos, ts))

        agent_transactional_constraints = []
        if self._solver_settings.get_edge_conflicts():
            for constraint in self._transactional_constraints:
                agent_id, pos_i, pos_f, ts = constraint
                if agent_id == agent.get_id():
                    agent_transactional_constraints.append((pos_i, pos_f, ts))

        solver = AStar(self._solver_settings)
        path = solver.find_path_with_constraints(self._problem_instance.get_map(), agent.get_start(),
                                                 agent.get_goal(), agent_constraints,
                                                 agent_transactional_constraints)

        return path

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
                    return 'INPLACE', [(reservation_table[(pos, ts)], pos, ts), (ag_i, pos, ts)]
                reservation_table[(pos, ts)] = ag_i

        if self._solver_settings.get_edge_conflicts():
            for ag_i, path in enumerate(self._solution):
                for ts, pos in enumerate(path):
                    ag_j = reservation_table.get((pos, ts-1))  # Agent in the pos position at the previous time step
                    if ag_j is not None and ag_j != ag_i:
                        if len(self._solution[ag_j]) > ts:
                            if self._solution[ag_j][ts] == path[ts-1]:
                                return 'TRANSACTIONAL', [(ag_j, self._solution[ag_j][ts-1], self._solution[ag_j][ts], ts),
                                                         (ag_i, path[ts-1], path[ts], ts)]
        return None

    def expand(self):
        """
        Expand the current state. It generates the two child nodes, once with the conflict constraint added to the first
        agent and the other with the conflict constraint added to the second agent involved in the conflict.
        :return: the two possible next states.
        """
        conflict_type, constraints = self.check_conflicts()

        node_a, node_b = None, None

        if conflict_type == 'INPLACE':
            agent, pos, ts = constraints[0]
            constraints_a = self._constraints.copy()
            constraints_a.add(constraints[0])
            node_a = ConstraintTreeNode(self._problem_instance, self._solver_settings, constraints_set=constraints_a,
                                        transactional_constraints=self._transactional_constraints.copy(),
                                        previous_solution=self._solution.copy(), agent_to_recompute=agent, parent=self)

            agent, pos, ts = constraints[1]
            constraints_b = self._constraints.copy()
            constraints_b.add(constraints[1])
            node_b = ConstraintTreeNode(self._problem_instance, self._solver_settings, constraints_set=constraints_b,
                                        transactional_constraints=self._transactional_constraints.copy(),
                                        previous_solution=self._solution.copy(), agent_to_recompute=agent, parent=self)

        if conflict_type == 'TRANSACTIONAL':
            agent, pos_i, pos_f, ts = constraints[0]
            constraints_a = self._transactional_constraints.copy()
            constraints_a.add(constraints[0])
            node_a = ConstraintTreeNode(self._problem_instance, self._solver_settings, constraints_set=self._constraints.copy(),
                                        transactional_constraints=constraints_a,
                                        previous_solution=self._solution.copy(), agent_to_recompute=agent, parent=self)

            agent, pos_i, pos_f, ts = constraints[1]
            constraints_b = self._transactional_constraints.copy()
            constraints_b.add(constraints[1])
            node_b = ConstraintTreeNode(self._problem_instance, self._solver_settings, constraints_set=self._constraints.copy(),
                                        transactional_constraints=constraints_b,
                                        previous_solution=self._solution.copy(), agent_to_recompute=agent, parent=self)
        return [node_a, node_b]

    def calculate_cost(self):
        if self._solver_settings.get_objective_function() == "SOC":
            return sum([len(path)-self._solver_settings.get_goal_occupation_time() for path in self._solution])
        if self._solver_settings.get_objective_function() == "Makespan":
            return max([len(path)-self._solver_settings.get_goal_occupation_time() for path in self._solution])

    def total_cost(self):
        return self._total_cost

    def total_time(self):
        return max([len(path)-self._solver_settings.get_goal_occupation_time() for path in self._solution])

    def constraints(self):
        return self._constraints

    def transactional_constraints(self):
        return self._transactional_constraints

    def solution(self):
        return self._solution

    def __str__(self):
        string = '[Constraints:' + str(self._constraints) + \
                 ' Transactional constraints:' + str(self._transactional_constraints) + \
                 ' Total Cost:' + str(self._total_cost) + \
                 ' PATH:' + str(self._solution) + ']'
        return string
