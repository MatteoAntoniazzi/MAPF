class Map:
    """
    This class represents a map.
    """

    def __init__(self, h, w, obstacles):
        """
        Initialize a map with his dimensions and the list of the obstacles.
        :param h: height of the map.
        :param w: width of the map.
        :param obstacles: list of obstacles in (x,y) coordinates.
        """
        self._h = h
        self._w = w
        self._obstacles_xy = obstacles

    def neighbours(self, xy):
        """
        Returns the positions of the neighbours in (x, y) Coordinates. It considers as neighbours only the horizontal
        and vertical neighbours, not the traversals ones, so it'll move left, right, up and down.
        :param xy: is a tuple (x, y) representing a position on the map.
        :return: a list of (x, y) positions.
        """
        x, y = xy
        neighbours = []

        if x > 0 and not (x-1, y) in self._obstacles_xy:
            neighbours.append((x-1, y))
        if x < self._w-1 and not (x+1, y) in self._obstacles_xy:
            neighbours.append((x+1, y))
        if y > 0 and not (x, y-1) in self._obstacles_xy:
            neighbours.append((x, y-1))
        if y < self._h-1 and not (x, y+1) in self._obstacles_xy:
            neighbours.append((x, y+1))

        return neighbours

    def get_height(self):
        """
        Returns the height of the map.
        """
        return self._h

    def get_width(self):
        """
        Returns the width of the map.
        """
        return self._w

    def get_obstacles_xy(self):
        """
        Return the list of obstacles positions.
        """
        return self._obstacles_xy

    def is_obstacle(self, pos):
        """
        Return True if in the position pos=(x,y) there's an obstacle.
        :param pos: position (x, y) that I want to analyze.
        :return: True if in the inserted position the is an obstacle.
        """
        return pos in self._obstacles_xy

    def __str__(self):
        return "Map(h=" + str(self._h) + ", w=" + str(self._w) + ", obstacles=" + str(self._obstacles_xy) + ")"
