# MAPF
Implementation of some of the most famous search-based algorithms for solving the Multi-Agent Path Finding problem, with some variants of the problem and a graphic user interface for the visualization of the results.

### Implemented Algorithms
1. Hierarchical Cooperative A* (HCA*) [David Silver, 2005]
2. A*-Based Search
3. Standley's enhancement: Operator Decomposition (OD) [Trevor Standley, 2010]
4. Standley's enhancement: Independence Detection (ID) [Trevor Standley, 2010]
5. Increasing Cost Tree Search (ICTS) [Guni Sharon et al., 2013]
6. Conflict-Based Search (CBS) [Guni Sharon et al., 2015]
7. M* [Glenn Wagner and Howie Choset, 2011]

### Implemented Variants of the problem
Agents' behaviour at goal:
* Stay at goal;
* Disappear at goal after a choosable number of time steps;
      
Conflicts:
* Vertex conflicts: always checked;
* Edge conflicts: up to the user;
      
Objective functions:
* Sum of costs (SOC);
* Makespan

