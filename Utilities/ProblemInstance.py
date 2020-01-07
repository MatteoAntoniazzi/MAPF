from Utilities.Visualize import Visualize
from Utilities.macros import *
from colorama import Fore, Back
from random import choice


class ProblemInstance:
    def __init__(self, map, agents):
        self._map = map
        self._agents = agents
        self._agents.sort(key=lambda x: x.get_id(), reverse=False)

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

    def get_agents_id_list(self):
        return [a.get_id() for a in self._agents]

    def get_agent_by_id(self, agent_id):
        for agent in self._agents:
            if agent.get_id() == agent_id:
                return agent
        return None

    def plot_on_gui(self, start_menu, frame, paths=None):
        window = Visualize(start_menu, frame, self._map, self._agents)
        window.draw_world()
        window.draw_agents()
        if paths is not None:
            # window.draw_paths(paths)
            window.draw_footsteps()
            window.start_animation(paths)
        window.do_loop()

    def plot_on_terminal(self, paths=None):
        grid = [[Fore.BLACK + Back.RESET + '·' for i in range(self._map.get_width())] for j in range(self._map.get_height())]
        for x, y in self._map.get_obstacles_xy():
            grid[y][x] = Fore.LIGHTWHITE_EX + Back.LIGHTWHITE_EX + '#'
        for a in self._agents:
            sx, sy = a.get_start()
            gx, gy = a.get_goal()
            agent_color = choice(FORES)
            grid[sy][sx] = agent_color + Back.RESET + '⚉'
            grid[gy][gx] = agent_color + Back.RESET + '⚇'
            if paths:
                for p in paths[a.get_id()][1:-1]:
                    grid[p[1]][p[0]] = agent_color + Back.RESET + '●'
        for i in range(len(grid)):
            print(*grid[i], Fore.BLUE + Back.RESET + '', sep='')
        print(Fore.RESET + Back.RESET + '')
