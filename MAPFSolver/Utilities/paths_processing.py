def check_conflicts(paths, stay_at_goal, is_edge_conflict):
    """
    Return the two agents ids that has a conflict. In order to identify the conflicts correctly we need to normalize
    the paths lengths. If stay in goal is True I need to normalized the vector since the agents will stay in the goal
    even the next time steps.
    :param paths: paths where check conflicts.
    :param stay_at_goal: True if the agents stays in the goal after arrived. The paths should stay in goal at the end
    one time step
    :param is_edge_conflict: if True also the edge conflicts are checked.
    :return: the two conflicting agents.
    """
    reservation_table = dict()
    if stay_at_goal:
        paths = normalize_paths_lengths(paths)

    for ag_i, path in enumerate(paths):
        for ts, pos in enumerate(path):
            if reservation_table.get((pos, ts)) is not None:
                return reservation_table[(pos, ts)], ag_i
            reservation_table[(pos, ts)] = ag_i

    if is_edge_conflict:
        for ag_i, path in enumerate(paths):
            for ts, pos in enumerate(path):
                ag_j = reservation_table.get((pos, ts - 1))
                if ag_j is not None and ag_j != ag_i:
                    if len(paths[ag_j]) > ts:   # To be sure that the ag_j will still exists in the next time step.
                        if paths[ag_j][ts] == path[ts - 1]:
                            return ag_i, ag_j

    return None


def check_conflicts_with_type(paths, stay_in_goal, is_edge_conflict):
    """
    Returns a couple (type of constraint, new children constraints) or None if the state has no conflicts:
    - In case a vertex conflict is found it will returns the two child conflicts:
    Example: (ai, aj, v, t) -> as [(ai, v, t), (aj, v, t)]
    - In case an edge conflict is found it will returns the two child conflicts:
    Example: [(ai, pos_i, pos_f, ts_f), (aj, pos_i, pos_f, ts_f)]
    """
    reservation_table = dict()
    if stay_in_goal:
        paths = normalize_paths_lengths(paths)

    for ag_i, path in enumerate(paths):
        for ts, pos in enumerate(path):
            if reservation_table.get((pos, ts)) is not None:
                return 'vertex_conflict', [(reservation_table[(pos, ts)], pos, ts), (ag_i, pos, ts)]
            reservation_table[(pos, ts)] = ag_i

    """max_t = max([len(path)-1 for path in paths])

    for ts in range(max_t):
        for ag_i, path in enumerate(paths):
            pos = path[ts]
            if reservation_table.get((pos, ts)) is not None:
                return 'vertex_conflict', [(reservation_table[(pos, ts)], pos, ts), (ag_i, pos, ts)]
            reservation_table[(pos, ts)] = ag_i"""

    if is_edge_conflict:
        for ag_i, path in enumerate(paths):
            for ts, pos in enumerate(path):
                ag_j = reservation_table.get((pos, ts - 1))  # Agent in the pos position at the previous time step.
                if ag_j is not None and ag_j != ag_i:
                    if len(paths[ag_j]) > ts:  # To be sure that the ag_j will still exists in the next time step.
                        if paths[ag_j][ts] == path[ts - 1]:
                            return 'edge_conflict', [(ag_j, paths[ag_j][ts-1], paths[ag_j][ts], ts),
                                                     (ag_i, path[ts-1], path[ts], ts)]
    return None


def calculate_soc(paths, stay_in_goal, goal_occupation_time):
    """
    Given the list of paths it return the sum of cost value. Time spent in goal is not considered.
    :param paths: list of paths.
    :param stay_in_goal: True if the agents stays in the goal after arrived. The paths should stay in goal at the end
    one time step
    :param goal_occupation_time: time that the agent will spent in the goal before disappear. Have sense only if stay in
    goal is false.
    :return: Sum Of Cost value
    """
    if not paths:
        return None

    soc = 0
    if stay_in_goal:
        for path in paths:
            soc += len(path) - 1
    else:
        for path in paths:
            soc += len(path) - goal_occupation_time
    return soc


def calculate_makespan(paths, stay_in_goal, goal_occupation_time):
    """
    Given the list of paths it return the makespan value. Time spent in goal is not considered.
    :param paths: list of paths.
    :param stay_in_goal: True if the agents stays in the goal after arrived. The paths should stay in goal at the end
    one time step
    :param goal_occupation_time: time that the agent will spent in the goal before disappear. Have sense only if stay in
    goal is false.
    :return: Makespan value
    """
    if not paths:
        return None

    if stay_in_goal:
        makespan = max([len(path)-1 for path in paths])
    else:
        makespan = max([len(path) for path in paths]) - goal_occupation_time
    return makespan


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