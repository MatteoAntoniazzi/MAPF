from Solver import Solver
from States.SingleAgentState import SingleAgentState
from States.MultiAgentState import MultiAgentState
from QueueStructures.MultiAgentQueue import MultiAgentQueue


class AStarMultiAgent(Solver):
    def __init__(self, problem_instance):
        super().__init__(problem_instance)

    def compute_paths(self):
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

        single_agents_states = [SingleAgentState(self._problem_instance.get_map(), agent.get_id(), agent.get_goal(),
                                                 agent.get_start(), 0, 0)
                                for agent in self._problem_instance.get_agents()]

        starter_state = MultiAgentState(self._problem_instance, single_agents_states)
        frontier.add(starter_state)

        while not frontier.is_empty():
            frontier.sort_by_f_value()
            cur_state = frontier.pop()

            if cur_state.goal_test():
                return cur_state.get_paths_to_parent()

            if not closed_list.contains(cur_state):
                closed_list.add(cur_state)

                expanded_nodes = cur_state.expand()
                print("Expanded Nodes: ", len(expanded_nodes))
                frontier.add_list_of_states(expanded_nodes)

        return []
