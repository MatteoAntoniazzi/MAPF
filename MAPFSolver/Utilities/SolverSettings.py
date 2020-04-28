from MAPFSolver.Heuristics.initialize_heuristic import initialize_heuristics


class SolverSettings:
    """
    This class contains all the settings of the solver. An instance of this object will be passed to the solver for his
    initialization.
    """

    def __init__(self, heuristic="Manhattan", objective_function="SOC", stay_at_goal=True, goal_occupation_time=1,
                 edge_conflict=True, time_out=None):
        """
        Initialization of the variables representing the solver settings.
        :param heuristic: heuristic used. ("Manhattan" or "Abstract Distance with RRA*")
        :param objective_function: objective function that the solver will minimize. ("SOC" or "Makespan")
        :param stay_at_goal: True if the agents never disappear once reach the goal.
        :param goal_occupation_time: if stay_at_goal is False, this variable tells how many time step the agents
        will stay in the goal before disappearing.
        :param edge_conflict: if True, also the edge conflicts will be considered in addition to the vertex
        conflicts.
        :param time_out: max time for computing the solution. If the time is over it returns an empty solution.
        The time is expressed in seconds.
        """
        self._heuristic_str = heuristic
        self._heuristic_obj = None
        self._objective_function = objective_function
        self._stay_at_goal = stay_at_goal
        self._goal_occupation_time = goal_occupation_time
        self._edge_conflict = edge_conflict
        if time_out is not None:
            self._time_out = time_out if time_out > 0 else None
        else:
            self._time_out = None

        assert self._goal_occupation_time > 0, "Goal occupation time must be greater than zero!"

    def initialize_heuristic(self, problem_instance):
        """
        Initialize the heuristic object which offer the compute_heuristic() method.
        :param problem_instance
        """
        self._heuristic_obj = initialize_heuristics(self._heuristic_str, problem_instance)

    def get_heuristic_str(self):
        """
        Return the heuristic used as string. ("Manhattan" or "Abstract Distance with RRA*")
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

    def stay_at_goal(self):
        """
        Return True if the agents never disappear once reached the goal.
        """
        return self._stay_at_goal

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
        return self._edge_conflict

    def set_time_out(self, time_out):
        """
        Return the time out value. How much the solver will run at max.
        """
        self._time_out = time_out

    def get_time_out(self):
        """
        Return the time out value. How much the solver will run at max.
        """
        return self._time_out

    def __str__(self):
        return "Heuristics: " + self._heuristic_str + ".\tObjective function: " + str(self._objective_function) + \
               ".\tGoal occupation time: " + str(self._goal_occupation_time)
