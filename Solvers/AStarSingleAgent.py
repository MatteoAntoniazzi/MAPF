from Solvers.MAPFSolver import MAPFSolver
from AStar import AStar


class AStarSingleAgent(MAPFSolver):
    def __init__(self, heuristics_str):
        super().__init__(heuristics_str)

    def solve(self, problem_instance, verbose=False):
        paths = []
        for agent in problem_instance.get_agents():
            a_star = AStar(self._heuristics_str)
            path = a_star.find_path(problem_instance.get_map(), agent.get_start(), agent.get_goal())
            paths.append(path)
        print("Total time: ", max([len(path)-1 for path in paths]), " Total cost:", sum([len(path)-1 for path in paths]))
        return paths
