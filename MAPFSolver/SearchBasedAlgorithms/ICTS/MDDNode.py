class MDDNode:
    """
    This class represent a node of the MDD diagram.
    Every node s represent a position and a time step. Remember that a node here can have multiple parents.
    """

    def __init__(self, problem_map, goal, position, time_step=0, parent=None, dummy=False):
        self._problem_map = problem_map
        self._parent = parent
        self._children = []
        self._goal = goal
        self._position = position
        self._time_step = time_step
        self._dummy = dummy
        self._number_of_dummy_predecessors = self.compute_number_of_dummy_predecessors()

    def expand(self):
        """
        Expand the current state. It computes all the possible moves from that position.
        :return: the list of possible next states.
        """
        possible_moves = self._problem_map.neighbours(self._position)
        possible_moves.insert(0, self._position)   # Wait move

        expanded_nodes_list = []
        for pos in possible_moves:
            expanded_nodes_list.append(MDDNode(self._problem_map, self._goal, pos, time_step=self._time_step+1,
                                               parent=[self]))

        return expanded_nodes_list

    def goal_test(self):
        """
        Check if it is in the goal position.
        """
        return self._goal == self._position

    def get_paths_to_root(self, solver_settings):
        """
        Return a list of all the possible paths from the start to the goal. It builds the paths starting from the goal
        and going up following all the possible parents alternatives.
        """
        paths = self.get_paths_to_parent_fun()

        for path in paths:
            path.reverse()

            if not solver_settings.stay_at_goal():
                goal = path[len(path)-1]
                for i in range(solver_settings.get_goal_occupation_time()-1):
                    path.append(goal)

        return paths

    def get_paths_to_parent_fun(self):
        """
        Recursive function used to get all the possible paths from a node going up. The paths can be more than one since
        each node can have more than one parent. It returns a list of paths from the node who call the method.
        """
        paths = []
        path = []
        node = self

        path.append(node._position)

        while node.parent() is not None and len(node.parent()) == 1:
            path.append(node.parent()[0].position())
            node = node.parent()[0]

        if node.parent() is not None:
            if len(node.parent()) > 1:
                for parent in node.parent():
                    parent_paths = parent.get_paths_to_parent_fun()
                    for parent_path in parent_paths:
                        new_path = path.copy()
                        new_path.extend(parent_path)
                        paths.append(new_path)

        if not paths:
            return [path]
        else:
            return paths

    def add_parent(self, parent):
        """
        Add a parent to this node.
        :param parent: parent to add.
        """
        self._parent.append(parent)

    def add_child(self, new_child):
        """
        Add a child to the list of children.
        :param new_child: child to add.
        """
        for child in self._children:
            if child.equal(new_child):
                return False

        self._children.append(new_child)

    def parent(self):
        """
        Returns the list of parents. If only one it returns a list of one element.
        :return:
        """
        return self._parent

    def get_children(self):
        """
        Returns the list of children of this node.
        """
        return self._children

    def position(self):
        """
        Returns the position of this node.
        """
        return self._position

    def goal_position(self):
        """
        Returns the position of the goal.
        """
        return self._goal

    def equal(self, other):
        """
        Return True if the state and the given state has the same position and the same time step.
        :param other: state to compare position.
        """
        assert isinstance(other, MDDNode)
        return self._position == other._position and self.time_step() == other.time_step()

    def time_step(self):
        """
        Returns the time step of this node.
        """
        return self._time_step

    def is_dummy(self):
        """
        Returns True if this node is a dummy node. (It means that it has been created only for fill the TotalMDDNode)
        """
        return self._dummy

    def is_blocking(self, solver_settings):
        """
        Return True if the node can block other nodes. It means that can be a normal node, or if it is a dummy node we
        have 2 cases:
        - stay_at_goal is True: in this case all dummy nodes are blocking.
        - stay_at_goal is False: in this case we've to look at the goal occupation time.
            the state is blocking if is dummy and the number of dummy predecessors is < GOAL_OCC_TIME-1
            example: GOAL_OCC_TIME=3 and the node is dummy and the number of dummy predecessors is 2. This node is not
                     a blocking node since behind him he has the goal node (1 TS) e due dummy nodes (TS 2). So, in the
                     goal, he has already been for the GOAL_OCC_TIME needed.
        :param solver_settings: settings of the solver.
        """
        if not self._dummy or solver_settings.stay_at_goal():
            return True
        else:
            return self._number_of_dummy_predecessors < solver_settings.get_goal_occupation_time() - 1

    def get_number_of_dummy_predecessors(self):
        """
        Return the number of dummy predecessors.
        """
        return self._number_of_dummy_predecessors

    def compute_number_of_dummy_predecessors(self):
        """
        Compute and return the number of dummy predecessors of this node.
        """
        if self._parent is None:
            return 0
        elif self._parent[0].is_dummy():
            return self._parent[0].get_number_of_dummy_predecessors() + 1
        else:
            return 0

    def __str__(self):
        string = 'Pos:' + str(self._position) + ' TS:' + str(self._time_step)
        if self._parent is not None:
            string += ' Parents pos:' + str([p.position() for p in self._parent])
        if self._children:
            string += ' Children pos:' + str([str(p.position()) + " " + str(p.time_step()) for p in self._children])
        return string
