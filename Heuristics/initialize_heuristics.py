from Heuristics.RRAStarHeuristics import RRAStarHeuristics
from Heuristics.ManhattanHeuristics import ManhattanHeuristics


def initialize_heuristics(heuristics_name, problem_instance):
    if heuristics_name == "Manhattan":
        return ManhattanHeuristics(problem_instance)
    if heuristics_name == "RRA":
        return RRAStarHeuristics(problem_instance)
