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

    def calculate_soc(self, paths):
        """
        Given the list of paths it return the sum of cost value. Time spent in goal is not considered.
        :param paths: list of paths.
        :return: Sum Of Cost value
        """
        soc = 0
        if self._solver_settings.stay_in_goal():
            for path in paths:
                soc += len(path) - 1
        else:
            for path in paths:
                soc += len(path) - self._solver_settings.get_goal_occupation_time()
        return soc

    def calculate_makespan(self, paths):
        """
        Given the list of paths it return the makespan value. Time spent in goal is not considered.
        :param paths: list of paths.
        :return: Makespan value
        """
        if self._solver_settings.stay_in_goal():
            makespan = max([len(path)-1 for path in paths])
        else:
            makespan = max([len(path) for path in paths]) - self._solver_settings.get_goal_occupation_time()
        return makespan

    @staticmethod
    def generate_output_infos(soc, makespan, expanded_nodes, computation_time):
        """
        Return a struct with the output infos.
        """
        return {
            "sum_of_costs": soc,
            "makespan": makespan,
            "expanded_nodes": expanded_nodes,
            "computation_time": computation_time
        }
