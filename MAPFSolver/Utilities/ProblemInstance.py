from .Agent import Agent


class ProblemInstance:
    """
    This class represents an instance of a problem. So, it has the problem Map and the scene which represents the
    set of Agents with their start and goal positions.
    """

    def __init__(self, problem_map, agents):
        """
        Initialize the problem with the map and the list of agents.
         _original_agents represents the list of agents with their universal id. It is used for the ID framework.
        _agents represents the new list of agents with the problem id, which has been set incrementally from 0 to the
        number of agents.
        :param problem_map: Map of the problem.
        :param agents: Set of agents in the problem.
        """
        self._map = problem_map
        self._original_agents = agents
        self._original_agents.sort(key=lambda x: x.get_id(), reverse=False)
        self._agents = []

        for i, a in enumerate(self._original_agents):
            self._agents.append(Agent(i, a.get_start(), a.get_goal()))

        assert not self._agents_outside_boundaries(), "An Agent is located outside the map."
        assert self._agents_not_overlap_obstacles(), "Agent initial or goal position overlaps an obstacle."
        assert not self._duplicate_goals_or_starts(), "Agent initial or goal positions duplicates."

    def _agents_outside_boundaries(self):
        """
        Check that no agent is outside the boundaries of the map.
        """
        for a in self._agents:
            xs, ys = a.get_start()
            xg, yg = a.get_goal()
            if xs >= self._map.get_width() or xs < 0 or xg >= self._map.get_width() or xg < 0 or \
                    ys >= self._map.get_height() or ys < 0 or yg >= self._map.get_height() or yg < 0:
                return True
        return False

    def _agents_not_overlap_obstacles(self):
        """
        Check that no agent initial or goal position overlaps an obstacle.
        """
        for a in self._agents:
            if self._map.is_obstacle(a.get_start()) or self._map.is_obstacle(a.get_goal()):
                return False
        return True

    def _duplicate_goals_or_starts(self):
        """
        Check that no agent goal/start position overlaps another agent goal/start position.
        It is possible to have a start position on another goal position.
        So, I just need to check that I have no duplicates in the start positions and in the goal positionsn instance
        """
        for i in range(len(self._agents)):
            for j in range(i+1, len(self._agents)):
                agent1 = self._agents[i]
                agent2 = self._agents[j]
                if agent1.get_start() == agent2.get_start() or agent1.get_goal() == agent2.get_goal():
                    return True
        return False

    def get_map(self):
        """
        Return the problem Map.
        """
        return self._map

    def get_agents(self):
        """
        Return the problem list of Agents, with their new problem id's.
        """
        return self._agents

    def get_original_agents(self):
        """
        Return the original list of Agents with their original id's.
        """
        return self._original_agents

    def get_original_agents_id_list(self):
        """
        Return the list of agents original id's in the problem.
        """
        return [a.get_id() for a in self._original_agents]

    def __str__(self):
        return "MAP: {" + self._map.__str__() + "}. AGENTS: {" + str([a.__str__() for a in self._agents]) + "}"
