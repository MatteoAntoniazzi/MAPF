from CooperativeAStar.AStar import AStar
from Solver import Solver


class HierarchicalCooperativeAStar(Solver):
    def __init__(self):
        self._reservation_table = dict()

    def solve(self, problem_instance):
        paths = []

        for agent in problem_instance.get_agents():
            print("AGENT N:", agent.get_id(), "OF ", len(problem_instance.get_agents()))
            # Compute AStar on every agent
            rra = RRAStar(problem_instance.get_map(), agent)
            solver = AStar(problem_instance.get_map(), heuristic="RRA", rra=rra)
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
