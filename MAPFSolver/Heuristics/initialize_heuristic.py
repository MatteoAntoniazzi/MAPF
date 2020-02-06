def initialize_heuristics(heuristics_name, problem_instance):
    if heuristics_name == "Manhattan":
        from .ManhattanHeuristic import ManhattanHeuristic
        return ManhattanHeuristic(problem_instance)

    if heuristics_name == "RRA":
        from .RRAStarHeuristic import RRAStarHeuristic
        return RRAStarHeuristic(problem_instance)
