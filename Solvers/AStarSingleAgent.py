from MAPFSolver import MAPFSolver
from States.SingleAgentState import SingleAgentState
from AStar import AStar


class AStarSingleAgent(MAPFSolver):
    def __init__(self, heuristics_str):
        super().__init__(heuristics_str)

    def solve(self, problem_instance):
        paths = []
        for agent in problem_instance.get_agents():
            a_star = AStar(self._heuristics_str)
            path = a_star.find_path(problem_instance.get_map(), agent.get_start(), agent.get_goal())
            paths.append(path)
        return paths
