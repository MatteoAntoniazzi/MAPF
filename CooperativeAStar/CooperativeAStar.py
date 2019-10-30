"""
Cooperative A* (CA*) is a an algorithm for solving the Co-operative Path-finding problem.
The task is decoupled into a series of single agent searches. The individual searches
are performed in three dimensional space-time, and take account of the planned routes of other agents.
A wait move is included in the agent’s action set, to enable it to remain stationary.
After each agent’s route is calculated, the states along the route are marked into a reservation table.
Entries in the reservation table are considered impassable and are avoided during searches by subsequent agents.
The reservation table represents the agents’ shared knowledge about each other’s planned routes.
It is a sparse data structure marking off regions of space-time.
A simple implementation, used here, is to treat the reservation table as a 3-dimensional grid (two spatial dimensions
and one time dimension). Each cell of the grid that is intersected by the agent’s planned route is marked as impassable
for precisely the duration of the intersection, thus preventing any other agent from planning a colliding route. Only a
small proportion of grid locations will be touched, and so the grid can be efficiently implemented as a hash table,
hashing on a randomly distributed function of the (x, y, t) key.
"""
from Solver import Solver
from CooperativeAStar.AStar import AStar


class CooperativeAStar(Solver):
    def __init__(self, problem_instance):
        super().__init__(problem_instance)
        self._reservation_table = dict()

    def compute_paths(self):
        paths = []
        for agent in self._problem_instance.get_agents():
            # Compute AStar on every agent
            solver = AStar(self._problem_instance.get_map())
            path = solver.find_path_with_reservation_table(agent, self._reservation_table)
            paths.append(path)

            for i, pos in enumerate(path):
                if not self._reservation_table.get(i):
                    self._reservation_table[pos] = []
                self._reservation_table[pos].append(i)
                if pos == agent.get_goal():
                    # devo tenerlo occupato anche per i timestamp successivi se non voglio che vada sopra ai goals
                    for c in range(i+1, i+100):
                        self._reservation_table[pos].append(c)
                    print(self._reservation_table[pos])
        return paths
