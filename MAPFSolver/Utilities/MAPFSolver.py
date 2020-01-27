import abc


class MAPFSolver:
    """
    Abstract class for any solver.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, solver_settings):
        self._solver_settings = solver_settings

    @abc.abstractmethod
    def solve(self, problem_instance, verbose=False):
        """
        Compute the paths
        """

    @staticmethod
    def generate_output_infos(soc, makespan, expanded_nodes, computation_time):
        return {
            "sum_of_costs": soc,
            "makespan": makespan,
            "expanded_nodes": expanded_nodes,
            "computation_time": computation_time
        }
