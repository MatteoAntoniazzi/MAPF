from Utilities.MAPFSolver import MAPFSolver
from Utilities.AStar import AStar
from Utilities.macros import *


class AStarSingleAgent(MAPFSolver):
    def __init__(self, heuristics_str):
        super().__init__(heuristics_str)

    def solve(self, problem_instance, verbose=False, print_output=True):
        paths = []
        for agent in problem_instance.get_agents():
            a_star = AStar(self._heuristics_str)
            path = a_star.find_path(problem_instance.get_map(), agent.get_start(), agent.get_goal())
            paths.append(path)
        if print_output:
            print("Total time: ", max([len(path)-1 for path in paths]),
                  " Total cost:", sum([len(path)-GOAL_OCCUPATION_TIME for path in paths]))
        return paths
