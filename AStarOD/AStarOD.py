from Solver import Solver
from States.SingleAgentState import SingleAgentState
from States.ODState import ODState
from QueueStructures.MultiAgentQueue import MultiAgentQueue
from CooperativeAStar.RRAStar import RRAStar


class AStarOD(Solver):
    def __init__(self):
        self._n_of_expanded_nodes = 0
        self._n_of_loops = 0

    def solve(self, problem_instance, verbose=False):
        """
        Returns the path between two nodes as a list of nodes using the A* algorithm.
        If no path could be found, an empty list is returned.

        grid -> is the map with obstacles
        start -> is the robot starting position (sx, sy)
        end -> is the robot ending position (gx, gy)

        return the path as list of (x, y) positions
        """
        frontier = MultiAgentQueue()
        closed_list = MultiAgentQueue()

        rra = []
        for agent in problem_instance.get_agents():
            rra.append(RRAStar(problem_instance.get_map(), agent))

        single_agents_states = [SingleAgentState(problem_instance.get_map(), agent.get_id(), agent.get_goal(),
                                                 agent.get_start(), 0, 0, heuristic="RRA", rra=rra[i])
                                for i, agent in enumerate(problem_instance.get_agents())]

        starter_state = ODState(problem_instance, single_agents_states)
        frontier.add(starter_state)

        while not frontier.is_empty():
            frontier.sort_by_f_value()
            cur_state = frontier.pop()

            if cur_state.goal_test():
                if verbose:
                    print("Total Expanded Nodes: ", self._n_of_expanded_nodes, " Number of loops: ", self._n_of_loops,
                          " Total time: ", cur_state.time_step(), " Total cost:", cur_state.g_value())
                return cur_state.get_paths_to_parent()

            if not closed_list.contains_state(cur_state):
                if cur_state.is_a_standard_state():
                    closed_list.add(cur_state)

                expanded_nodes = cur_state.expand(verbose=False)

                self._n_of_expanded_nodes += len(expanded_nodes)
                self._n_of_loops += 1

                frontier.add_list_of_states(expanded_nodes)

        return []
