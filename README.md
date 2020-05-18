# MAPF
Implementation of some of the most famous search-based algorithms for solving the Multi-Agent Path Finding problem, with some variants of the problem and a graphic user interface for the visualization of the results.

### Implemented Algorithms
1. Hierarchical Cooperative A* (HCA*) [David Silver, 2005]
2. A*
3. Standley's enhancements: [Trevor Standley, 2010]
      3.1. Operator Decomposition (OD)
      3.2. Independence Detection (ID)
4. Increasing Cost Tree Search (ICTS) [Guni Sharon, 2013]
5. Conflict-Based Search (CBS) [Guni Sharon, 2015]
6. M* [Glenn Wagner, 2011]

### Implemented Variants of the problem
Agents' behaviour at goal:
      - Stay at goal;
      - Disappear at goal after a choosable number of time steps;
      
Conflicts:
      - Vertex conflicts: always checked;
      - Edge conflicts: up to the user;
      
 Objective functions:
      - Sum of costs (SOC);
      - Makespan

