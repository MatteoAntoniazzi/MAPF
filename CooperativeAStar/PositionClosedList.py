class PositionClosedList:
    def __init__(self):
        self._close_set = []

    def __contains__(self, item):
        return item in self._close_set

    def add(self, position):
        self._close_set.append(position)

    def delete(self, position):
        if position in self._close_set:
            self._close_set.remove(position)

    def is_empty(self):
        return len(self._close_set) == 0
