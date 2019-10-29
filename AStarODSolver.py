from Solver import Solver
from States.SingleAgentState import SingleAgentState
from States.ODState import ODState


# DEVO CONTROLLARE I CONFLITTI!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


def manhattan_dist(a, b):
    """
    Returns the Manhattan distance between two points.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


class AStarSolver(Solver):
    def __init__(self, problem_instance, heuristic=manhattan_dist):
        super().__init__(problem_instance)
        self._heuristic = heuristic

    def find_paths(self):
        """
        Returns the path between two nodes as a list of nodes using the A* algorithm.
        If no path could be found, an empty list is returned.

        grid -> is the map with obstacles
        start -> is the robot starting position (sx, sy)
        end -> is the robot ending position (gx, gy)

        return the path as list of (x, y) positions
        """
        # Initialize a state for each agent
        single_agent_states = []
        for agent in self._agents:
            single_agent_states.append(SingleAgentState(agent.get_start(), 0, self._heuristic(agent.get_start(), agent.get_goal())))
        starter_state = ODState(single_agent_states)
        frontier = [starter_state]
        closed_list = set()

        while frontier:
            frontier.sort(key=lambda x: x.get_f_value(), reverse=False)
            cur_state = frontier.pop(0)
            closed_list.add(cur_state)

            # check if current ODState is goal
            if cur_state.get_position() == goal:
                return cur_state.get_path_to_parent()

            cur_agent = cur_state.get_single_agent_states()[cur_state.get_next_to_move()]

            possible_moves = self._map.get_neighbours_xy(cur_state.get_position())
            possible_moves = [move for move in possible_moves if move not in closed_list]
            for i in possible_moves:
                n = SingleAgentState(i, cur_state.get_g_value() + 1, self._heuristic(i, cur_agent.get_goal()), cur_state)
                m = ODState()
                frontier.append(n)

        return []
