def check_conflicts(paths, is_edge_conflict):
    """
    Return the two agents ids that has a conflict. In order to identify the conflicts correctly we need to normalize
    the paths lengths.
    """
    reservation_table = dict()
    normalized_paths = normalize_paths_lengths(paths)

    for i, path in enumerate(normalized_paths):
        for ts, pos in enumerate(path):
            if reservation_table.get((pos, ts)) is not None:
                return reservation_table[(pos, ts)], i
            reservation_table[(pos, ts)] = i

    if is_edge_conflict:
        for ag_i, path in enumerate(normalized_paths):
            for ts, pos in enumerate(path):
                ag_j = reservation_table.get((pos, ts - 1))
                if ag_j is not None and ag_j != ag_i:
                    if len(normalized_paths[ag_j]) > ts:
                        if normalized_paths[ag_j][ts] == path[ts - 1]:
                            return ag_i, ag_j

    return None


def normalize_paths_lengths(paths):
    """
    It receives a list of paths of different lengths. It normalize all this lengths by adding goal state to all the
    short paths.
    :param paths: paths to update.
    :return: return the updated paths.
    """
    import copy
    max_length = max([len(path) for path in paths])
    new_paths = copy.deepcopy(paths)  # deep copy of the paths

    for path in new_paths:
        while len(path) < max_length:
            path.append(path[len(path)-1])

    return new_paths


"""
example_paths = [[(1,2), (2,2)], [(1,3), (2,3), (2,4), (2,5), (2,6)], [(3,3), (4,3), (5,3)]]
new_example_paths = normalize_paths_lengths(example_paths)
print(example_paths)
print(new_example_paths)
"""