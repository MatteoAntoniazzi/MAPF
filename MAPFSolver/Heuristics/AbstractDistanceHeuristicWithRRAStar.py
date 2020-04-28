from MAPFSolver.Utilities.StatesQueue import StatesQueue
from .Heuristic import Heuristic


class AbstractDistanceHeuristicWithRRAStar(Heuristic):
    """
    Abstract distance heuristic. This heuristics can be viewed as perfect estimates of the distance to the destination.
    It is computed by running single-agent search from a location to the the goal with all the other agents removed.
    RRA* algorithm is used to computed the values.
    """

    def __init__(self, problem_instance):
        """
        Initialize the heuristic. It creates one open list dictionary, where the key is the goal position of the agent
        and the value is the open list of that goal, and a closed list, where the key is again the goal position of the
        agent. Instead of using the agent as key, we've choose to use his goal position.
        :param problem_instance: instance of the problem to compute the heuristic values.
        """
        self._problem_instance = problem_instance
        self._open_lists = dict()
        self._closed_lists = dict()
        self.initialize_table()

    def resume_rra_star(self, position, goal_pos):
        """
        Resume RRA*: it resumes the search in order to reach the goal node.
        :param position: position to reach.
        :param goal_pos: position of the goal of the agent.
        :return:
        """
        while not self._open_lists[goal_pos].is_empty():
            self._open_lists[goal_pos].sort_by_f_value()
            cur_state = self._open_lists[goal_pos].pop()
            self._closed_lists[goal_pos].add(cur_state)

            if cur_state.get_position() == position:
                self._open_lists[goal_pos].add(cur_state)
                return True

            expanded_nodes = cur_state.expand()
            for state in expanded_nodes:
                if not self._open_lists[goal_pos].contains_position(state.get_position()) and \
                        not self._closed_lists[goal_pos].contains_position(state.get_position()):
                    self._open_lists[goal_pos].add(state)
                if self._open_lists[goal_pos].contains_position(state.get_position()):
                    if state.f_value() < self._open_lists[goal_pos].contains_position(state.get_position()).f_value():
                        self._open_lists[goal_pos].update(state)
        return False

    def compute_heuristic(self, position, goal):
        """
        Compute the value of the heuristic in that position to the goal position.
        """
        if self._closed_lists[goal].contains_position(position):
            return self._closed_lists[goal].contains_position(position).g_value()
        if self.resume_rra_star(position, goal):
            return self._closed_lists[goal].contains_position(position).g_value()
        return None

    def initialize_table(self):
        """
        Initialize the table. For each agent it creates two queue structure (one open list and one closed list) that are
        stored in the respective dictionary at the goal position key. Then a reverse search from the goal to the start
        is done using Manhattan heuristic. In this way the closed list has been initialized and it stores all the
        positions from the goal to the start position. (Remember that the search has goal and start inverted)
        """
        for agent in self._problem_instance.get_agents():
            goal_pos = agent.get_goal()

            self._open_lists[goal_pos] = StatesQueue()
            self._closed_lists[goal_pos] = StatesQueue()

            from MAPFSolver.Utilities.SingleAgentState import SingleAgentState
            from MAPFSolver.Utilities.SolverSettings import SolverSettings
            solver_settings = SolverSettings(heuristic="Manhattan")
            solver_settings.initialize_heuristic(self._problem_instance)
            starter_state = SingleAgentState(self._problem_instance.get_map(), agent.get_start(), goal_pos,
                                             solver_settings)

            self._open_lists[goal_pos].add(starter_state)
            self.resume_rra_star(agent.get_start(), goal_pos)
