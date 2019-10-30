from Solver import Solver
from States.SingleAgentState import SingleAgentState
from States.MultiAgentState import MultiAgentState


class AStarMultiAgentSolver(Solver):
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

        single_agents_states = [SingleAgentState(self._problem_instance, agent.get_id(), agent.get_start(), 0)
                                for agent in self._problem_instance.get_agents()]

        print("INITIAL STATES: ", len(single_agents_states))
        starter_state = MultiAgentState(self._problem_instance, single_agents_states)
        frontier = [starter_state]
        closed_list = set()

        while frontier:
            frontier.sort(key=lambda x: (x.get_f_value(), x.get_h_value()), reverse=False)
            cur_state = frontier.pop(0)
            closed_list.add(cur_state)

            if cur_state.goal_test():
                return cur_state.get_paths_to_parent()

            expanded_nodes_list = cur_state.expand()

            print("front bef", len(frontier))
            print("EXPANDED NODES", len(expanded_nodes_list))
            # DA OTTIMIZZARE!!!
            for new_state in expanded_nodes_list:
                flag = False
                for state in frontier:
                    if new_state.equal_positions(state):
                        flag = True
                        break
                if not flag:
                    frontier.append(new_state)
            print("front aft", len(frontier))
        return []
