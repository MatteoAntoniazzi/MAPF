from States.SingleAgentState import SingleAgentState
from CooperativeAStar.StateClosedList import StateClosedList
from CooperativeAStar.PositionClosedList import PositionClosedList


class AStar:
    def __init__(self, map, heuristic="Manhattan", rra=None):
        self._map = map
        self._heuristic = heuristic
        self._rra = rra

    def find_path_with_reservation_table(self, agent, reservation_table):
        """
        Returns the path between two nodes as a list of nodes using the A* algorithm.
        If no path could be found, an empty list is returned.
        return the path as list of (x, y) positions.

        Closed lists are used to accelerate the process. When a state with a conflict is found the closed list with the
        positions empty in order to allow the wait moves.
        """
        frontier = StateClosedList()
        closed_list = StateClosedList()  # Keep all the states already expanded
        closed_list_of_positions = PositionClosedList()  # Keep all the positions already visited

        starter_state = SingleAgentState(self._map, agent.get_id(), agent.get_goal(), agent.get_start(), 0, 0,
                                         heuristic=self._heuristic, rra=self._rra)
        frontier.add(starter_state)
        to_print = False

        while not frontier.is_empty():
            if closed_list.size() % 2000 == 0 and closed_list.size() != 0:
                to_print = True
            if to_print:
                print("OpenListSize: {0}. closedListSize: {1}".format(frontier.size(), closed_list.size()))
                to_print = False

            frontier.sort_by_f_value()
            cur_state = frontier.pop()

            if cur_state.goal_test():
                return cur_state.get_path_to_parent()

            if cur_state not in closed_list and cur_state.get_position not in closed_list_of_positions:
                closed_list.add(cur_state)
                closed_list_of_positions.add(cur_state.get_position())

                expanded_nodes = cur_state.expand()

                expanded_nodes_no_conflicts = []
                for state in expanded_nodes:
                    busy_times = reservation_table.get(state.get_position(), [])
                    cur_pos_busy_times = reservation_table.get(cur_state.get_position(), [])

                    if state.get_timestamp() in busy_times or (state.get_timestamp()-1 in busy_times and
                                                               state.get_timestamp() in cur_pos_busy_times):
                        closed_list_of_positions = PositionClosedList()  # Empty the list to allow waiting moves
                    else:
                        expanded_nodes_no_conflicts.append(state)

                frontier.add_list_of_states(expanded_nodes_no_conflicts)
        return []
