from MAPFSolver.Utilities.State import State
from MAPFSolver.Utilities.SingleAgentState import SingleAgentState
import itertools


class MultiAgentState(State):
    """
    This class represent the single state (node) object for the A* algorithm.
    It is a subclass of the State class and in addition it stores all the single agent states of each agent.
    """

    def __init__(self, single_agents_states, solver_settings, parent=None):
        """
        Initialize the Multi Agent State. It receives the solver settings and the list of all single agent states.
        :param single_agents_states: list of SingleAgentState instances.
        :param solver_settings: settings of the solver.
        :param parent: Eventual parent State.
        """
        super().__init__(parent=parent)
        self._single_agents_states = single_agents_states
        self._solver_settings = solver_settings
        self.set_time_step(max([state.time_step() for state in single_agents_states]))
        self.compute_cost()
        self.compute_heuristics()

    def expand(self, verbose=False):
        """
        Expand the current state. For each single state it computes all the possible moves for that agent.
        Then these states are iterated in order to obtain all the possible multi agent state combinations.
        :return: the list of possible next states.
        """
        if verbose:
            print("Expansion in progress...", end=' ')

        candidate_list = []
        for single_state in self._single_agents_states:
            single_state_neighbor_list = single_state.expand()
            candidate_list.append(single_state_neighbor_list)

        candidate_state_list = list(itertools.product(*candidate_list))

        valid_states = []
        for i, multi_state in enumerate(candidate_state_list):
            if self.is_valid(multi_state):
                valid_states.append(multi_state)

        free_conflict_states = []
        for i, multi_state in enumerate(valid_states):
            m = MultiAgentState(multi_state, self._solver_settings, parent=self)
            if not self.is_conflict(m):
                free_conflict_states.append(m)

        if verbose:
            print("DONE! Number of expanded states:", len(free_conflict_states))

        return free_conflict_states

    def is_conflict(self, multi_state):
        """
        Return True if a conflict occur in the given multi agent state.
        Will be checked that:
        1. no agents occupy the same position in the same time step (vertex conflict);
        2. no agent overlap (edge conflict).
        """
        current_positions = self.get_positions_list()
        next_positions = multi_state.get_positions_list()

        next_active_positions = multi_state.get_active_positions()
        if len(next_active_positions) != len(set(next_active_positions)):
            return True

        if self._solver_settings.is_edge_conflict():
            for i, next_pos in enumerate(next_positions):
                for j, cur_pos in enumerate(current_positions):
                    if i != j:
                        if next_pos == cur_pos:
                            if next_positions[j] == current_positions[i]:
                                return True
        return False

    def colliding_robots(self, multi_state):
        """
        Return the set of robots which collide in the given multi agent state.
        Will be checked that:
        Will be checked that:
        1. no agents occupy the same position in the same time step (vertex conflict);
        2. no agent overlap (edge conflict).
        """
        colliding_robots = set()

        for i, next_state_i in enumerate(multi_state.get_single_agent_states()):
            for j, next_state_j in enumerate(multi_state.get_single_agent_states()):
                if i != j and next_state_i.get_position() == next_state_j.get_position() and \
                        not next_state_i.is_gone() and not next_state_j.is_gone():
                    colliding_robots.add(i)
                    colliding_robots.add(j)

        if self._solver_settings.is_edge_conflict():
            current_positions = self.get_positions_list()
            next_positions = multi_state.get_positions_list()

            for i, next_pos in enumerate(next_positions):
                for j, cur_pos in enumerate(current_positions):
                    if i != j:
                        if next_pos == cur_pos:
                            if next_positions[j] == current_positions[i]:
                                colliding_robots.add(i)
                                colliding_robots.add(j)

        return colliding_robots

    def get_active_positions(self):
        """
        Return the list of positions occupied by the agents.
        """
        pos_list = []
        for state in self._single_agents_states:
            if not state.is_gone():
                pos_list.append(state.get_position())
        return pos_list

    def goal_test(self):
        """
        Return True if all agents have arrived to the goal position. Remember that it not consider the occupation time.
        If stay at goal is False use the is_completed() method.
        """
        for single_state in self._single_agents_states:
            if not single_state.goal_test():
                return False
        return True

    def is_completed(self):
        """
        Return True if all agents have arrived to the goal position and stayed there for the time needed.
        So, all the agents will have completed.
        """
        for single_state in self._single_agents_states:
            if not single_state.is_completed():
                return False
        return True

    def compute_heuristics(self):
        """
        Compute the heuristic value for this state using the selected heuristic. (h-value)
        If the heuristic is Sum Of Cost it computes the sum over all single state heuristics.
        If the heuristic is Makespan it computes the maximum value over all single state heuristics.
        """
        self._h = 0
        if self._solver_settings.get_objective_function() == "SOC":
            for single_state in self._single_agents_states:
                self._h += single_state.h_value()
        if self._solver_settings.get_objective_function() == "Makespan":
            self._h = max([single_state.h_value() for single_state in self._single_agents_states])

    def compute_cost(self):
        """
        Compute the cost of the current state. (g-value)
        If the objective function is Sum Of Cost it computes the sum over all single state path costs.
        If the objective function is Makespan it computes the maximum value over all single path costs.
        """
        self._g = 0
        if self.is_root():
            return
        if self._solver_settings.get_objective_function() == "SOC":
            for single_state in self._single_agents_states:
                self._g += single_state.g_value()
        if self._solver_settings.get_objective_function() == "Makespan":
            self._g = max([single_state.g_value() for single_state in self._single_agents_states])

    def get_paths_to_root(self):
        """
        Compute and return the list of paths for each agent.
        """
        paths = []
        for single_state in self._single_agents_states:
            paths.append(single_state.get_path_to_root())
        return paths

    def get_single_agent_states(self):
        """
        Return the list of the single agent states.
        """
        return self._single_agents_states

    def get_positions_list(self):
        """
        Return the list of the positions of the single agent states.
        """
        return [state.get_position() for state in self._single_agents_states]

    def equal_position(self, other):
        """
        Return True if the multi agent state and the given multi agent state has the same positions for all the single
        agent states.
        :param other: state to compare positions.
        """
        assert isinstance(other, MultiAgentState)
        for i, single_state in enumerate(self._single_agents_states):
            if not single_state.equal_position(other.get_single_agent_states()[i]):
                return False
        return True

    def equal(self, other):
        """
        Return True if the multi agent state and the given multi agent state has the same positions and the same time
        steps for all the single agent states.
        :param other: state to compare position.
        """
        assert isinstance(other, MultiAgentState)
        for i, single_state in enumerate(self._single_agents_states):
            if not single_state.equal(other.get_single_agent_states()[i]):
                return False
        return True

    def __str__(self):
        string = '[F:' + str(self.f_value()) + ' G: ' + str(self.g_value()) + ' TS:' + str(self.time_step()) + ' '
        string += str(self.get_positions_list()) + ']'
        return string

    @staticmethod
    def is_valid(multi_state):
        """
        Check that the multi state has valid single agent states.
        :param multi_state: list of single agent states
        :return: True if the multi state is valid.
        """
        if len(multi_state) == 1:
            return True
        for s in multi_state:
            assert isinstance(s, SingleAgentState)
        return True
