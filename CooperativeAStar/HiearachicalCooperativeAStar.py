from CooperativeAStar import CooperativeAStar
from CooperativeAStar.AStar import AStar
from CooperativeAStar.RRAStar import RRAStar
from Solver import Solver


class HierarchicalCooperativeAStar(Solver):
    def __init__(self, problem_instance):
        super().__init__(problem_instance)
        self._reservation_table = dict()

    def compute_paths(self):
        paths = []

        for agent in self._problem_instance.get_agents():
            print("AGENT N:", agent.get_id(), "OF ", len(self._problem_instance.get_agents()))
            # Compute AStar on every agent
            rra = RRAStar(self._problem_instance.get_map(), agent)
            solver = AStar(self._problem_instance.get_map(), heuristic="RRA", rra=rra)
            path = solver.find_path_with_reservation_table(agent, self._reservation_table)
            paths.append(path)

            for i, pos in enumerate(path):
                if not self._reservation_table.get(pos):
                    self._reservation_table[pos] = []
                self._reservation_table[pos].append(i)
                if pos == agent.get_goal():
                    # I need to keep the place busy also after the agent reach his goal
                    for c in range(i + 1, i + 100):
                        self._reservation_table[pos].append(c)
        return paths
