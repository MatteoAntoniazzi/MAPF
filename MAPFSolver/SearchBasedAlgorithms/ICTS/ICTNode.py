from MAPFSolver.SearchBasedAlgorithms.ICTS.TotalMDD import TotalMDD
from MAPFSolver.SearchBasedAlgorithms.ICTS.MDD import MDD
from MAPFSolver.Utilities.AStar import AStar
from time import time


class ICTNode:
    """
    This class represent a node of the Increasing Cost Tree.
    Every node s consists of a k-vector of individual path costs, s = [C 1 , C 2 , . . . C k ] one cost per agent. Node
    s represents all possible complete solutions in which the cost of the individual path of agent a i is exactly C i.
    """

    def __init__(self, problem_instance, solver_settings, path_costs_vector=None, parent=None):
        self._problem_instance = problem_instance
        self._solver_settings = solver_settings
        self._parent = parent
        self._path_costs_vector = path_costs_vector

        if parent is None:
            self.initialize_root()

        self._solution = None
        self._mdd_vector = None
        self._total_mdd = None

    def initialize_node(self, stop_event, verbose=False):
        """
        This function initialize the node computing the various MDDs, and verify if a solution exists.
        """
        if verbose:
            print("Initializing node: ", self._path_costs_vector)
        self._mdd_vector = self.compute_mdds(verbose)
        self.compute_solution(stop_event, verbose)

    def expand(self):
        """
        Expand the current state.
        Based on the objective function we're using we've two cases.
        When we're minimizing the sum of costs the children nodes will be all the possible path costs vector obtained
        incrementing by one the total cost, so only one of the path costs.
        Example: node._path_cost_vector = [C1, C2, C3, ..] -> child1: [C1+1, C2, C3, ..], child2: [C1, C2+1, C3, ..], ..
        When we're minimizing the makespan  the task is to minimize the number of time steps elapsed until all agents
        reach their final positions. For this case, there is no meaning to the individual cost of a single agent.
        All agents virtually use the same amount of time steps. Thus, the size of the ICT will be linear in ∆ instead of
        exponential.
        Example: node._path_cost = 10 -> node._path_cost = 11 -> node._path_cost = 12
        :return: the list of possible next states.
        """
        candidate_list = []

        if self._solver_settings.get_objective_function() == "SOC":
            for i, agent in enumerate(self._problem_instance.get_agents()):
                path_costs = self._path_costs_vector.copy()
                path_costs[i] += 1
                candidate_list.append(ICTNode(self._problem_instance, self._solver_settings,
                                              path_costs_vector=path_costs, parent=self))

        if self._solver_settings.get_objective_function() == "Makespan":
            path_costs = self._path_costs_vector.copy()
            for i, agent in enumerate(self._problem_instance.get_agents()):
                path_costs[i] += 1
            candidate_list.append(ICTNode(self._problem_instance, self._solver_settings, path_costs_vector=path_costs,
                                          parent=self))

        return candidate_list

    def compute_mdds(self, verbose=False):
        """
        Compute the mdd for each agents.
        """
        if verbose:
            print("Computing MDDs...", end=' ')
        mdd_vector = []
        for i, agent in enumerate(self._problem_instance.get_agents()):
            mdd_vector.append(MDD(self._problem_instance.get_map(), agent, self._path_costs_vector[i],
                                  self._solver_settings))

        if verbose:
            print("MDDs computed.")
        return mdd_vector

    def compute_solution(self, stop_event, verbose=False):
        """
        Compute the total mdd and check if a solution exists.
        """
        if verbose:
            print("Computing TotalMDD...", end=' ')

        start = time()

        self._total_mdd = TotalMDD(self._problem_instance.get_map(), self._solver_settings, self._mdd_vector, stop_event)
        self._solution = self._total_mdd.get_solution()

        # Complete solution paths with the goal occupation time if needed.
        if not self._solver_settings.stay_at_goal():
            for path in self._solution:
                goal = path[len(path) - 1]
                for i in range(self._solver_settings.get_goal_occupation_time() - 1):
                    path.append(goal)

        if verbose:
            print("Computation time:", time() - start)

        return self._solution

    def initialize_root(self):
        """
        Initialize the root node. The output of this function will be different based on the objective function we are
        using.
        """
        if self._solver_settings.get_objective_function() == "SOC":
            self._path_costs_vector = self.compute_optimal_costs_vector()

        if self._solver_settings.get_objective_function() == "Makespan":
            optimal_costs_vector = self.compute_optimal_costs_vector()
            max_value = max(optimal_costs_vector)
            for i, agent in enumerate(self._problem_instance.get_agents()):
                self._path_costs_vector[i] = max_value

    def compute_optimal_costs_vector(self):
        """
        Returns the the optimal costs vector. It will have all the optimal costs for each agent.
        """
        path_costs_vector = []
        solver = AStar(self._solver_settings)
        for agent in self._problem_instance.get_agents():
            path = solver.find_path(self._problem_instance.get_map(), agent.get_start(), agent.get_goal())
            if self._solver_settings.stay_at_goal():
                cost = len(path) - 1
            else:
                cost = len(path) - self._solver_settings.get_goal_occupation_time()
            path_costs_vector.append(cost)
        return path_costs_vector

    def goal_test(self):
        """
        Returns true if in the node a valid solution is found. Remember to call initialize_node() method before.
        """
        if self._solution:
            return True
        return False

    def solution(self):
        """
        Returns the solution found. It's better to check before if the solution exists with the is_goal() method,
        otherwise it can return None.
        """
        return self._solution

    def path_costs_vector(self):
        """
        Returns the vector of path costs.
        """
        return self._path_costs_vector

    def total_cost(self):
        """
        Returns the node cost. If we're minimizing SOC it'll return the sum of the path costs, otherwise if we're
        minimizing Makespan it'll return the max of the path costs.
        :return:
        """
        if self._solver_settings.get_objective_function() == "SOC":
            return sum(self._path_costs_vector)
        if self._solver_settings.get_objective_function() == "Makespan":
            return max(self._path_costs_vector)

    def __str__(self):
        return "{ NODE:" + str(self._path_costs_vector) + " }"


"""def compute_solution_2(self, verbose=False):
    Compute the combined mdd by iterate over all the possible combinations of paths. Then check if exists a valid
    solution and in that case it returns it.
    This version is slower than the one that used the total mdd
    
    if verbose:
        print("Computing total MDD...", end=' ')

    candidate_paths = []
    for mdd in self._mdd_vector:
        candidate_paths.append(mdd.get_paths())
    candidate_solutions = list(itertools.product(*candidate_paths))

    if verbose:
        print("Total MDD computed.")

    prefix = "Check validity of " + str(len(candidate_solutions)) + " number of solutions..."
    if verbose:
        print_progress_bar(0, len(candidate_solutions), prefix=prefix, suffix='Complete', length=50)

    for i, solution in enumerate(candidate_solutions):
        if self.check_validity(solution):
            self._solution = solution
            if verbose:
                print("\nSolution found!")
            return solution
        if verbose:
            print_progress_bar(i + 1, len(candidate_solutions), prefix=prefix, suffix='Complete', length=50)

    if verbose:
        print("Solution not found!")

    return None"""

"""def check_validity(self, solution):
    Check if a solution has no conflicts.
    Will be checked that:
        1. no agents occupy the same position in the same time step;
        2. no agent overlap (switch places).
        
    conflicts = check_conflicts(solution, self._solver_settings.stay_at_goal(),
                                self._solver_settings.is_edge_conflict())
    if conflicts is None:
        return True
    return False"""

