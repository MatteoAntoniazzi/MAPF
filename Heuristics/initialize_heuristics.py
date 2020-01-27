from Heuristics.RRAStarHeuristics import RRAStarHeuristic
from Heuristics.ManhattanHeuristics import ManhattanHeuristic


def initialize_heuristics(heuristics_name, problem_instance):
    if heuristics_name == "Manhattan":
        return ManhattanHeuristic(problem_instance)
    if heuristics_name == "RRA":
        return RRAStarHeuristic(problem_instance)
