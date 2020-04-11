from .Visualize import Visualize
from MAPFSolver import *


def prepare_simulation(reader, frame, algorithm_str, independence_detection, solver_settings, n_of_agents):
    """
    Solve the MAPF problem and visualize the simulation on the frame.
    :param reader: Reader object for the loading of the map and the scen
    :param frame: Frame where the simulation will be displayed
    :param algorithm_str: String of the algorithm choose
    :param independence_detection: True if Independence Detection will be used with the algorithm
    :param solver_settings: Settings of the solver (heuristics, goal_occupation_time)
    :param n_of_agents: Number of Agents on the map
    """
    problem_map = load_map(reader)
    agents = load_agents(reader, problem_map, n_of_agents)
    problem_instance = ProblemInstance(problem_map, agents)

    if independence_detection:
        solver = IDFramework(algorithm_str, solver_settings)
    else:
        solver = get_solver(algorithm_str, solver_settings)
    print("Solver --> ", solver, "\nSolving...")
    paths, output_infos = solver.solve(problem_instance, verbose=True, return_infos=True)
    print("Solved.")

    plot_on_gui(problem_instance, solver_settings, frame, paths, output_infos)


def plot_paths(problem_instance, solver_settings, paths):
    from tkinter import Tk, Frame
    root = Tk()
    frame = Frame(root)
    frame.pack()
    plot_on_gui(problem_instance, solver_settings, frame, paths)

    root.mainloop()


def plot_on_gui(problem_instance, solver_settings, frame, paths=None, output_infos=None):
    """
    Plot the result on GUIdd.
    :param problem_instance: instance of the problem.
    :param solver_settings: settings of the solver.
    :param frame: tkinter frame where display the result.
    :param paths: resulting paths.
    :param output_infos: problem solving results.
    """
    window = Visualize(problem_instance, solver_settings, frame, paths, output_infos)
    window.initialize_window()


