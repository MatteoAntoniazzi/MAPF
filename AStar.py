from Heuristics.initialize_heuristics import initialize_heuristics
from States.SingleAgentState import SingleAgentState
from QueueStructures.SingleAgentQueue import SingleAgentQueue
from QueueStructures.PositionClosedList import PositionClosedList
from Utilities.Agent import Agent
from Utilities.ProblemInstance import ProblemInstance


class AStar:
    def __init__(self, heuristics_str="Manhattan"):
        self._heuristics_str = heuristics_str
        self._heuristics = None
        self._frontier = None
        self._closed_list = None  # Keep all the states already expanded
        self._closed_list_of_positions = None  # Keep all the positions already visited

    def find_path(self, map, start_pos, goal_pos):
        """
        It computes the path from his start position to his goal position using the A* algorithm.
        It return the path as list of (x, y) positions
        """
        self.initialize_problem(map, start_pos, goal_pos)

        while not self._frontier.is_empty():
            self._frontier.sort_by_f_value()
            cur_state = self._frontier.pop()

            if cur_state.goal_test():
                return cur_state.get_path_to_parent()

            if cur_state.get_position() not in self._closed_list_of_positions:
                self._closed_list_of_positions.add(cur_state.get_position())
                expanded_nodes = cur_state.expand()
                self._frontier.add_list_of_states(expanded_nodes)

        return []

    def find_path_with_reservation_table(self, map, start_pos, goal_pos, reservation_table):
        """
        It computes the path from his start position to his goal position using the A* algorithm with reservation table.
        It return the path as list of (x, y) positions.

        Closed lists are used to accelerate the process. When a state with a conflict is found the closed list with the
        positions empty in order to allow the wait moves.
        """
        self.initialize_problem(map, start_pos, goal_pos)

        # print("START POSITION:", start_pos)

        while not self._frontier.is_empty():
            self._frontier.sort_by_f_value()
            cur_state = self._frontier.pop()

            if cur_state.is_completed():
                return cur_state.get_path_to_parent()

            if not self._closed_list.contains_state(cur_state):
                self._closed_list.add(cur_state)

                expanded_nodes = cur_state.expand()

                # if start_pos == (1, 0):
                #     print("TS:", cur_state.time_step(), " EXPANDED NODES:", len(expanded_nodes))

                expanded_nodes_no_conflicts = []
                for state in expanded_nodes:

                    # if start_pos == (1, 0):
                    #     print("state:", state)

                    busy_times = reservation_table.get(state.get_position(), [])
                    cur_pos_busy_times = reservation_table.get(cur_state.get_position(), [])
                    # if start_pos == (1, 0):
                    #     print(busy_times)

                    if not (state.time_step() in busy_times or (state.time_step()-1 in busy_times and
                                                                state.time_step() in cur_pos_busy_times)):
                        # print("APPEND")
                        expanded_nodes_no_conflicts.append(state)

                self._frontier.add_list_of_states(expanded_nodes_no_conflicts)

        return []

    def initialize_problem(self, map, start_pos, goal_pos):
        problem_instance = ProblemInstance(map, [Agent(0, start_pos, goal_pos)])
        self._heuristics = initialize_heuristics(self._heuristics_str, problem_instance)

        self._frontier = SingleAgentQueue()
        self._closed_list = SingleAgentQueue()
        self._closed_list_of_positions = PositionClosedList()

        starter_state = SingleAgentState(map, 0, goal_pos, start_pos, 0, self._heuristics)
        self._frontier.add(starter_state)

