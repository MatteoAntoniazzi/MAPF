from MAPFSolver.SearchBasedAlgorithms.ICTS.MDDNode import MDDNode
import itertools


class TotalMDDNode:

    def __init__(self, problem_map, solver_settings, list_of_mdd_nodes, time_step=0, parent=None):
        self._problem_map = problem_map
        self._solver_settings = solver_settings
        self._list_of_mdd_nodes = list_of_mdd_nodes
        self._time_step = time_step
        self._parent = parent

    def expand(self):
        """
        Expand the current state. For every mdd of the agents it returns their children and compute a cartesian product
        in order to get all the possible next states. It is also checked that those states are without conflict.
        :return: the list of possible next states.
        """
        candidate_list = []  # list of list of children. (One for each agent)
        for single_mdd_node in self._list_of_mdd_nodes:
            single_children_list = single_mdd_node.get_children()
            if not single_children_list:
                # Add a dummy node
                single_children_list = [MDDNode(self._problem_map, single_mdd_node.goal_position(),
                                                single_mdd_node.position(), time_step=self._time_step+1,
                                                parent=[single_mdd_node], dummy=True)]
            candidate_list.append(single_children_list)

        candidate_state_list = list(itertools.product(*candidate_list))

        free_conflict_states = []
        for multi_state in candidate_state_list:
            if not self.is_conflict(multi_state):
                free_conflict_states.append(TotalMDDNode(self._problem_map, self._solver_settings, multi_state,
                                                         time_step=self._time_step+1, parent=[self]))

        return free_conflict_states

    def is_conflict(self, multi_state):
        """
        Return True if a conflict occur in the given list of MDDNode.
        Will be checked that:
        1. no agents occupy the same position in the same time step (no vertex conflicts).
        2. no agent overlap (no edge conflicts).
        """
        current_positions = [mdd_node.position() for mdd_node in self._list_of_mdd_nodes]
        next_positions = [mdd_node.position() for mdd_node in multi_state]

        next_active_positions = []
        if self._solver_settings.stay_at_goal():
            next_active_positions = next_positions.copy()
        else:
            for mdd_node in multi_state:
                if mdd_node.is_blocking(self._solver_settings):
                    next_active_positions.append(mdd_node.position())

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

    def goal_test(self):
        """
        Check if this node is a goal test. That it is, if all positions are goal positions.
        """
        for mdd_node in self._list_of_mdd_nodes:
            if not mdd_node.goal_test():
                return False
        return True

    def get_paths_to_root(self):
        """
        Function used to get a possible set of paths from this node going up. This can be more than one since
        each node can have more than one parent. Despite this it'll return only a possible set of paths, if exists.
        """
        list_of_paths = []
        for agent in range(len(self._list_of_mdd_nodes)):
            list_of_paths.append([])

        node = self

        while node._parent is not None:
            for i, mdd_node in enumerate(node._list_of_mdd_nodes):
                if not mdd_node.is_dummy():
                    list_of_paths[i].append(mdd_node.position())
            node = node._parent[0]

        for i, mdd_node in enumerate(node._list_of_mdd_nodes):
            if not mdd_node.is_dummy():
                list_of_paths[i].append(mdd_node.position())
            list_of_paths[i].reverse()

        if not list_of_paths:
            return None
        return list_of_paths

    def add_parent(self, parent):
        """
        Add a parent to this node.
        :param parent: parent to add.
        """
        self._parent.append(parent)

    def time_step(self):
        """
        Returns the time step of this node.
        """
        return self._time_step

    def get_list_of_mdd_nodes(self):
        """
        Returns the list of mdd nodes.
        """
        return self._list_of_mdd_nodes

    def equal(self, other):
        """
        Return True if the total mdd node and the given total mdd node has the same positions and the same time
        steps for all the single agent states.
        :param other: state to compare position.
        """
        assert isinstance(other, TotalMDDNode)
        if other.time_step() == self.time_step():
            for i, mdd_node in enumerate(self._list_of_mdd_nodes):
                if not mdd_node.equal(other.get_list_of_mdd_nodes()[i]):
                    return False
            return True
        return False

    def __str__(self):
        return 'Node:' + str([mdd_node.position() for mdd_node in self._list_of_mdd_nodes]) + \
               ' TS: ' + str(self._time_step)