from MAPFSolver.Heuristics.initialize_heuristic import initialize_heuristics


class SolverSettings:
    """
    This class contains all the settings of the solver. An instance of this object will be passed to the solver for his
    initialization.
    """

    def __init__(self, heuristic="Manhattan", objective_function="SOC", stay_in_goal=False,  goal_occupation_time=1,
                 is_edge_conflict=True):
        """
        Initialization of the variables representing the solver settings.
        :param heuristic: heuristic used. ("Manhattan" or "RRA")
        :param objective_function: objective function that the solver will minimize. ("SOC" or "Makespan")
        :param stay_in_goal: True if the agents never disappear once reach the goal.
        :param goal_occupation_time: if disappear_at_goal is True, this variable tells how many time step the agents
        will stay in the goal before disappearing.
        :param is_edge_conflict: if True, also the edge conflicts will be considered in addition to the vertex
        conflicts.
        """
        self._heuristic_str = heuristic
        self._heuristic_obj = None
        self._objective_function = objective_function
        self._stay_in_goal = stay_in_goal
        self._goal_occupation_time = goal_occupation_time
        self._is_edge_conflict = is_edge_conflict

        assert self._goal_occupation_time > 0, "Goal occupation time must be greater than zero!"

    def initialize_heuristic(self, problem_instance):
        """
        Initialize the heuristic object which offer the compute_heuristic() method.
        :param problem_instance
        """
        self._heuristic_obj = initialize_heuristics(self._heuristic_str, problem_instance)

    def get_heuristic_str(self):
        """
        Return the heuristic used as string. ("Manhattan" or "RRA")
        """
        return self._heuristic_str

    def get_heuristic_object(self):
        """
        Return the heuristic object which offer the compute_heuristic() method.
        """
        assert self._heuristic_obj is not None, "The heuristic need to be initialized"
        return self._heuristic_obj

    def get_objective_function(self):
        """
        Return the objective function used. ("SOC" or "Makespan")
        """
        return self._objective_function

    def stay_in_goal(self):
        """
        Return True if the agents never disappear once reached the goal.
        """
        return self._stay_in_goal

    def get_goal_occupation_time(self):
        """
        Return the time the agents will stay in the goal before disappearing. Useful only when disappear_at_goal is
        True.
        """
        return self._goal_occupation_time

    def set_goal_occupation_time(self, time):
        """
        Modify the goal_occupation_time variable.
        """
        self._goal_occupation_time = time

    def is_edge_conflict(self):
        """
        Return True if the edge conflicts are considered in addition to the vertex conflicts.
        """
        return self._is_edge_conflict

    def __str__(self):
        return "Heuristics: " + self._heuristic_str + ".\tObjective function: " + str(self._objective_function) + \
               ".\tGoal occupation time: " + str(self._goal_occupation_time)
