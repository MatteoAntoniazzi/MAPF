"""
M* algorithm, a complete and optimal implementation of sub-dimensional expansion which uses A* as the
underlying planner. The basic idea of the algorithm is the following:
1. Find optimal path for each agent individually;
2. Start the search. Generate only nodes on optimal paths;
3. If conflict occurs – backtrack and consider all ignored actions;

Implementation idea:
The primary difference whit A* is that M* restricts the set of possible successors of a vertex based on the collision
set. Here each node has his collision set which contains the agents that has a conflict in that node or in one of his
successors.
Only robots in the collision set are allowed to consider any possible action. All other robots must obey their
individual policies
"""
from MAPFSolver.Utilities.MAPFSolver import MAPFSolver
from MAPFSolver.Utilities.SingleAgentState import SingleAgentState
from Heuristics.initialize_heuristics import initialize_heuristics
from Utilities.StatesQueue import StatesQueue
from SearchBasedAlgorithms.MStar.MStarState import MStarState
import time


class SolverMStar(MAPFSolver):
    def __init__(self, solver_settings):
        super().__init__(solver_settings)
        self._frontier = None
        self._n_of_expanded_nodes = 0
        self._n_of_loops = 0

    def solve(self, problem_instance, verbose=False, print_output=True, return_infos=False):
        """
        Solve the MAPF problem using the M* algorithm returning the paths as lists of list of (x, y) positions.
        It start following the optimal policy and each time a conflict occur it updates the collision set and back
        propagate it to the ancestors. So, when the collision set is not empty it will considers for those agents all
        the possible moves.
        """
        start = time.time()

        self.initialize_problem(problem_instance)

        while not self._frontier.is_empty():
            self._frontier.sort_by_f_value()
            cur_state = self._frontier.pop()

            print("CUR STATE: ", cur_state.g_value(), end=" ")
            # [print(s.get_position(), " ", s.g_value(), " ", s.f_value(), end=" ") for s in cur_state.get_single_agent_states()]
            [print(s.f_value(), end=" ") for s in self._frontier._queue[:15]]
            print(" ")

            if cur_state.is_completed():
                if print_output:
                    print("Total Expanded Nodes: ", self._n_of_expanded_nodes, " Number of loops: ", self._n_of_loops,
                          " Total time: ", cur_state.time_step()-1, " Total cost:", cur_state.g_value())

                if return_infos:
                    output_infos = {
                        "sum_of_costs": cur_state.g_value(),
                        "makespan": cur_state.time_step()-1,
                        "expanded_nodes": self._n_of_expanded_nodes,
                        "computation_time": time.time() - start
                    }
                    return cur_state.get_paths_to_parent(), output_infos

                return cur_state.get_paths_to_parent()

            expanded_nodes = cur_state.expand(verbose=verbose)
            for node in expanded_nodes:
                self.back_propagate(cur_state, node)
                if len(node.get_collisions_set()) == 0:
                    self._frontier.add(node)
                    self._n_of_expanded_nodes += 1
            self._n_of_loops += 1

        return []

    def back_propagate(self, vk, vl):
        """
        Takes the parent node vk and the expanded node vl and back propagate the collision set of the expanded node vl
        to his ancestors recursively.
        :param vk: previous state
        :param vl: expanded state
        """
        cl = vl.get_collisions_set()
        ck = vk.get_collisions_set()

        if not cl.issubset(ck):
            vk.set_collisions_set(ck.union(cl))
            if not self._frontier.contains_state(vk):
                self._frontier.add(vk)

            for vm in vk.get_back_propagation_set():
                self.back_propagate(vm, vk)

    def initialize_problem(self, problem_instance):
        """
        Initialize the frontier and the heuristic for the given problem.
        """
        self._heuristics = initialize_heuristics(self._solver_settings.get_heuristics_str(), problem_instance)
        self._frontier = StatesQueue()
        self._n_of_expanded_nodes = 0
        self._n_of_loops = 0

        single_agents_states = []
        for i, agent in enumerate(problem_instance.get_agents()):
            s = SingleAgentState(problem_instance.get_map(), agent.get_id(), agent.get_goal(), agent.get_start(),
                                 self._heuristics, self._solver_settings.get_goal_occupation_time())
            single_agents_states.append(s)

        starter_state = MStarState(problem_instance, single_agents_states, self._heuristics,
                                   self._solver_settings.get_objective_function(),
                                   self._solver_settings.is_edge_conflict())
        self._frontier.add(starter_state)

    def __str__(self):
        return "M* Solver using " + self._solver_settings.get_heuristics_str() + " heuristics minimazing " + \
               self._solver_settings.get_objective_function()
