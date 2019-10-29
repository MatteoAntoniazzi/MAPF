from Solver import Solver
from States.SingleAgentState import SingleAgentState


class AStarSingleAgentSolver(Solver):
    def __init__(self, problem_instance):
        super().__init__(problem_instance)

    def compute_paths(self):
        paths = []
        for agent in self._agents:
            path = self.find_path(agent)
            paths.append(path)
        return paths

    def find_path(self, agent):
        """
        Returns the path between two nodes as a list of nodes using the A* algorithm.
        If no path could be found, an empty list is returned.

        grid -> is the map with obstacles
        start -> is the robot starting position (sx, sy)
        end -> is the robot ending position (gx, gy)

        return the path as list of (x, y) positions
        """
        starter_state = SingleAgentState(self._problem_instance, agent.get_id(), agent.get_start(), 0)
        frontier = [starter_state]
        closed_list = set()

        while frontier:
            print("FRONTIER")
            frontier.sort(key=lambda x: x.f_value(), reverse=False)
            cur_state = frontier.pop(0)
            print("CUR: ", cur_state.get_position())
            closed_list.add(cur_state.get_position())

            if cur_state.goal_test():
                return cur_state.get_path_to_parent()

            expanded_nodes_list = cur_state.expand()
            # [frontier.append(state) for state in expanded_nodes_list if state.get_position() not in closed_list]
            for state in expanded_nodes_list:
                if state.get_position() not in closed_list:
                    print("POS: ", state.get_position(), "CLOSED LIST: ", closed_list)
                    frontier.append(state)

        return []
