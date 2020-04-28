def initialize_heuristics(heuristics_name, problem_instance):
    """
    Initialize the heuristic object.
    :param heuristics_name: name of the heuristic to use.
    :param problem_instance: instance of the problem.
    :return: the heuristic object.
    """
    if heuristics_name == "Manhattan":
        from .ManhattanDistanceHeuristic import ManhattanDistanceHeuristic
        return ManhattanDistanceHeuristic(problem_instance)

    if heuristics_name == "AbstractDistance":
        from .AbstractDistanceHeuristicWithRRAStar import AbstractDistanceHeuristicWithRRAStar
        return AbstractDistanceHeuristicWithRRAStar(problem_instance)
