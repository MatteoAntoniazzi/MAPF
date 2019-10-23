from Utilities.Visualize2 import Visualize2
from Utilities.macros import *
from colorama import Fore, Back
from random import choice


class ProblemInstance:
    def __init__(self, map, agents):
        self._map = map
        self._agents = agents
        assert not self._duplicate_goals_or_starts(), "Agent initial or goal positions duplicates."

    def _duplicate_goals_or_starts(self):
        """
        Check if have duplicates
        """
        for i in range(len(self._agents)):
            for j in range(i+1, len(self._agents)):
                agent1 = self._agents[i]
                agent2 = self._agents[j]
                if agent1.get_start() == agent2.get_start() or agent1.get_goal() == agent2.get_goal():
                    return True
        return False

    def get_map(self):
        return self._map

    def get_agents(self):
        return self._agents

    def plot_on_gui(self, paths=None):
        window = Visualize2(self._map, self._agents)
        window.draw_world()
        window.draw_agents()
        if paths is not None:
            window.draw_paths()
            # window.start_animation()
        window.do_loop()

    def plot_on_terminal(self):
        grid = [[Fore.BLACK + Back.RESET + '·' for i in range(self._map.get_width())] for j in range(self._map.get_height())]
        for x, y in self._map.get_obstacles_xy():
            grid[y][x] = Fore.LIGHTWHITE_EX + Back.LIGHTWHITE_EX + '#'
        for a in self._agents:
            sx, sy = a.get_start()
            gx, gy = a.get_goal()
            agent_color = choice(FORES)
            grid[sy][sx] = agent_color + Back.RESET + '⚉'
            grid[gy][gx] = agent_color + Back.RESET + '⚇'
            # if self.paths:
            #     for p in self.paths[i][1:-1]:
            #         grid[p[0]][p[1]] = color + Back.RESET + '●'
        for i in range(len(grid)):
            print(*grid[i], Fore.BLUE + Back.RESET + '', sep='')
        print(Fore.RESET + Back.RESET + '')
