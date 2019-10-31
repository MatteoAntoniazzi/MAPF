from States.SingleAgentState import SingleAgentState
from CooperativeAStar.StateClosedList import StateClosedList
from CooperativeAStar.PositionClosedList import PositionClosedList


class AStar:
    def __init__(self, map):
        self._map = map
        self._frontier = StateClosedList()
        self._closed_list = StateClosedList()  # Keep all the states already expanded
        self._closed_list_of_positions = PositionClosedList()  # Keep all the positions already visited

    def find_path_with_reservation_table(self, agent, reservation_table):
        """
        Returns the path between two nodes as a list of nodes using the A* algorithm.
        If no path could be found, an empty list is returned.
        return the path as list of (x, y) positions.

        Closed lists are used to accelerate the process. When a state with a conflict is found the closed list with the
        positions empty in order to allow the wait moves.
        """
        starter_state = SingleAgentState(self._map, agent.get_id(), agent.get_goal(), agent.get_start(), 0, 0)
        self._frontier.add(starter_state)

        while not self._frontier.is_empty():
            self._frontier.sort_by_f_value()
            cur_state = self._frontier.pop()

            if cur_state.goal_test():
                return cur_state.get_path_to_parent()

            if cur_state not in self._closed_list and cur_state.get_position not in self._closed_list_of_positions:
                self._closed_list.add(cur_state)
                self._closed_list_of_positions.add(cur_state.get_position())

                expanded_nodes = cur_state.expand()

                for state in expanded_nodes:
                    busy_timestamps = reservation_table.get(state.get_position(), [])
                    if state.get_timestamp() in busy_timestamps:
                        print("CONFLICT IN:", state.get_position(), " AT TIME:", state.get_timestamp())
                        expanded_nodes.remove(state)
                        self._closed_list_of_positions = PositionClosedList()  # Empty the list to allow waiting moves

                self._frontier.add_list_of_states(expanded_nodes)
        return []
