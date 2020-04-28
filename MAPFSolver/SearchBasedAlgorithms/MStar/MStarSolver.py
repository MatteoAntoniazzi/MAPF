from MAPFSolver.SearchBasedAlgorithms.MStar.MStarStatesQueue import MStarStatesQueue
from MAPFSolver.Utilities.AbstractSolver import AbstractSolver
from MAPFSolver.Utilities.SingleAgentState import SingleAgentState
from MAPFSolver.Utilities.StatesQueue import StatesQueue
from MAPFSolver.Utilities.paths_processing import calculate_soc, calculate_makespan
from MAPFSolver.SearchBasedAlgorithms.MStar.MStarState import MStarState
from threading import Thread, Event
import time


class MStarSolver(AbstractSolver):
    """
    M* algorithm, a complete and optimal implementation of sub-dimensional expansion which uses A* as the
    underlying planner. The basic idea of the algorithm is the following:
    1. Find optimal path for each agent individually;
    2. Start the search. Generate only nodes on optimal paths;
    3. If conflict occurs – backtrack and consider all ignored actions;

    Implementation idea:
    The primary difference whit A* is that M* restricts the set of possible successors of a vertex based on the collision
    set. Here each node has his collision set which contains the agents that has a conflict in that node or in one of his
    successors.
    Only robots in the collision set are allowed to consider any possible action. All other robots must obey their
    individual policies
    """

    def __init__(self, solver_settings):
        """
        Initialize the A* solver.
        :param solver_settings: settings used by the A* solver.
        """
        super().__init__(solver_settings)
        self._frontier = None
        self._closed_list = None
        self._n_of_generated_nodes = 0
        self._n_of_expanded_nodes = 0
        self._solution = []

        self._stop_event = None

    def solve(self, problem_instance, verbose=False, return_infos=False):
        """
        Solve the given MAPF problem using the M* algorithm  and it returns, if exists, a solution.
        :param problem_instance: instance of the problem to solve.
        :param verbose: if True, infos will be printed on terminal.
        :param return_infos: if True in addition to the paths will be returned also a structure with output infos.
        :return the solution as list of paths, and, if return_infos is True, a tuple composed by the solution and a
        struct with output information.
        """
        self._stop_event = Event()
        start = time.time()

        thread = Thread(target=self.solve_problem, args=(problem_instance, verbose,))
        thread.start()
        thread.join(timeout=self._solver_settings.get_time_out())
        self._stop_event.set()

        soc = calculate_soc(self._solution, self._solver_settings.stay_at_goal(),
                            self._solver_settings.get_goal_occupation_time())
        makespan = calculate_makespan(self._solution, self._solver_settings.stay_at_goal(),
                                      self._solver_settings.get_goal_occupation_time())

        output_infos = self.generate_output_infos(soc, makespan, self._n_of_generated_nodes, self._n_of_expanded_nodes,
                                                  time.time() - start)
        if verbose:
            print("Problem ended: ", output_infos)

        return self._solution if not return_infos else (self._solution, output_infos)

    def solve_problem(self, problem_instance, verbose=False):
        """
        Solve the MAPF problem using the M* algorithm.
        It start following the optimal policy and each time a conflict occur it updates the collision set and back
        propagate it to the ancestors. So, when the collision set is not empty it will considers for those agents all
        the possible moves.
        :param problem_instance: problem instance to solve
        :param verbose: if True will be printed some computation infos on terminal.
        """
        self.initialize_problem(problem_instance)

        while not self._frontier.is_empty():
            self._frontier.sort_by_f_value()
            cur_state = self._frontier.pop()

            if self._stop_event.is_set():
                break

            if cur_state.is_completed():
                self._solution = cur_state.get_paths_to_root()
                return

            self._closed_list.add(cur_state)
            expanded_nodes = cur_state.expand(verbose=verbose)
            self._n_of_generated_nodes += len(expanded_nodes)
            self._n_of_expanded_nodes += 1

            for node in expanded_nodes:
                if self._closed_list.contains_position_and_time_step(node):
                    n = self._closed_list.get_node(node)
                else:
                    n = node
                self.back_propagate(cur_state, n)
                if len(n.get_collisions_set()) == 0:
                    self._frontier.add(n)

    def back_propagate(self, vk, vl):
        """
        Takes the parent node vk and the expanded node vl and back propagate the collision set of the expanded node vl
        to his ancestors recursively.
        :param vk: previous state
        :param vl: expanded state
        """
        ck = vk.get_collisions_set().copy()
        cl = vl.get_collisions_set().copy()

        if not cl.issubset(ck):
            vk.set_collisions_set(ck.union(cl))

            if not self._frontier.contains_state(vk):
                self._frontier.add(vk)

            for vm in vk.get_back_propagation_set():
                self.back_propagate(vm, vk)

    def initialize_problem(self, problem_instance):
        """
        Initialize the frontier and the heuristic for the given problem.
        """
        self._solver_settings.initialize_heuristic(problem_instance)
        self._frontier = StatesQueue()
        self._closed_list = MStarStatesQueue()
        self._n_of_generated_nodes = 1
        self._n_of_expanded_nodes = 0

        single_agents_states = []
        for agent in problem_instance.get_agents():
            s = SingleAgentState(problem_instance.get_map(), agent.get_goal(), agent.get_start(), self._solver_settings)
            single_agents_states.append(s)

        starter_state = MStarState(single_agents_states, self._solver_settings)
        self._frontier.add(starter_state)

    def __str__(self):
        return "M* Solver using " + self._solver_settings.get_heuristic_str() + " heuristics minimazing " + \
               self._solver_settings.get_objective_function()
