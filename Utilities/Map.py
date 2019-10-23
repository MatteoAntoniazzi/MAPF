class Map:
    def __init__(self, h, w, obstacles):
        self._h = h
        self._w = w
        self._obstacles_xy = obstacles  # In (x, y) Coordinates

    def get_neighbours_xy(self, x, y):
        """
        Returns the positions of the neighbours in (x, y) Coordinates
        """
        neighbours = []

        # MOVE LEFT
        if x > 0 and not (x, y-1) in self._obstacles_xy:
            neighbours.append((x, y-1))
        # MOVE RIGHT
        if x < self._w-1 and not (x, y+1) in self._obstacles_xy:
            neighbours.append((x, y+1))
        # MOVE UP
        if y > 0 and not (x-1, y) in self._obstacles_xy:
            neighbours.append((x-1, y))
        # MOVE DOWN
        if y < self._h-1 and not (x+1, y) in self._obstacles_xy:
            neighbours.append((x+1, y))
        return neighbours

    def get_height(self):
        return self._h

    def get_width(self):
        return self._w

    def get_obstacles_xy(self):
        return self._obstacles_xy

    def is_obstacle(self, x, y):
        return (x, y) in self._obstacles_xy
