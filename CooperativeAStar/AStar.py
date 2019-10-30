from States.SingleAgentState import SingleAgentState


class AStar:
    def __init__(self, map):
        self._map = map

    def find_path_with_reservation_table(self, agent, reservation_table):
        """
        Returns the path between two nodes as a list of nodes using the A* algorithm.
        If no path could be found, an empty list is returned.
        return the path as list of (x, y) positions
        """
        starter_state = SingleAgentState(self._map, agent.get_id(), agent.get_goal(), agent.get_start(), 0, 0)
        frontier = [starter_state]
        closed_list = set()
        closed_list_same_time = set()

        while frontier:
            frontier.sort(key=lambda x: x.f_value(), reverse=False)
            cur_state = frontier.pop(0)
            closed_list.add(cur_state.get_position())
            closed_list_same_time.add(cur_state)

            if cur_state.goal_test():
                return cur_state.get_path_to_parent()

            expanded_nodes_list = cur_state.expand()

            print("FRONTIERA", len(frontier))
            list_updated = []
            # Check not conflict
            for state in expanded_nodes_list:
                busy_timestamps = reservation_table.get(state.get_position())
                if busy_timestamps:
                    if not state.get_timestamp() in busy_timestamps:
                        list_updated.append(state)
                    else:
                        closed_list = set()
                        print("CONFLICTED STATE:", state.get_agent_id(), state.get_position(), "time", state.get_timestamp())
                else:
                    list_updated.append(state)

            for state in list_updated:
                if state.get_position() not in closed_list and all([not state.equal_position_and_timestamps(s) for s in closed_list_same_time]):
                    frontier.append(state)
        return []
