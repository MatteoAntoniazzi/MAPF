def get_solver(algorithm_str, solver_settings):
    """
    Return the Solver object for the specified algorithm and relative settings.
    """
    if algorithm_str == "Cooperative A*":
        from MAPFSolver.SearchBasedAlgorithms.CooperativeAStar.CooperativeAStarSolver import CooperativeAStarSolver
        return CooperativeAStarSolver(solver_settings)
    if algorithm_str == "A*":
        from MAPFSolver.SearchBasedAlgorithms.AStar.AStarSolver import AStarSolver
        return AStarSolver(solver_settings)
    if algorithm_str == "A* with Operator Decomposition":
        from MAPFSolver.SearchBasedAlgorithms.AStarOD.AStarODSolver import AStarODSolver
        return AStarODSolver(solver_settings)
    if algorithm_str == "Increasing Cost Tree Search":
        from MAPFSolver.SearchBasedAlgorithms.ICTS.ICTSSolver import ICTSSolver
        return ICTSSolver(solver_settings)
    if algorithm_str == "Conflict Based Search":
        from MAPFSolver.SearchBasedAlgorithms.CBS.CBSSolver import CBSSolver
        return CBSSolver(solver_settings)
    if algorithm_str == "M*":
        from MAPFSolver.SearchBasedAlgorithms.MStar.MStarSolver import MStarSolver
        return MStarSolver(solver_settings)
    raise ValueError('Algorithm string not exists!')


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', print_end="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print("\r", prefix, " |", bar, "| ", percent, "% ", suffix, end='', sep='')
    # Print New Line on Complete
    if iteration == total:
        print()
