def initialize_heuristics(heuristics_name, problem_instance):
    if heuristics_name == "Manhattan":
        from .ManhattanDistanceHeuristic import ManhattanDistanceHeuristic
        return ManhattanDistanceHeuristic(problem_instance)

    if heuristics_name == "AbstractDistance":
        from .AbstractDistanceHeuristicWithRRAStar import AbstractDistanceHeuristicWithRRAStar
        return AbstractDistanceHeuristicWithRRAStar(problem_instance)
