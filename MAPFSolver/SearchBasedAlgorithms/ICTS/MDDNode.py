class MDDNode:
    """
    This class represent a node of the MDD diagram.
    Every node s represent a position and a time step. Remember that a node here can have multiple parents.
    """

    def __init__(self, problem_map, position, time_step=0, parent=None):
        self._problem_map = problem_map
        self._parent = parent
        self._position = position
        self._time_step = time_step

    def expand(self):
        """
        Expand the current state. It computes all the possible moves from that position.
        :return: the list of possible next states.
        """
        possible_moves = self._problem_map.get_neighbours_xy(self._position)
        possible_moves.insert(0, self._position)   # Wait move

        expanded_nodes_list = []
        for pos in possible_moves:
            expanded_nodes_list.append(MDDNode(self._problem_map, pos, time_step=self._time_step+1, parent=[self]))

        return expanded_nodes_list

    def get_paths_to_parent(self, solver_settings):
        """
        Return a list of all the possible paths from the start to the goal. It builds the paths starting from the goal
        and going up following all the possible parents alternatives.
        """
        paths = self.get_paths_to_parent_fun()

        for path in paths:
            path.reverse()

            if not solver_settings.stay_in_goal():
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

    def parent(self):
        """
        Returns the list of parents. If only one it returns a list of one element.
        :return:
        """
        return self._parent

    def position(self):
        """
        Returns the position of this node.
        """
        return self._position

    def time_step(self):
        """
        Returns the time step of this node.
        """
        return self._time_step

