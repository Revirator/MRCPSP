# Project
This project contains the code used for my bachelor thesis as part of the 2023 Q4 [Research Project](https://github.com/TU-Delft-CSE/Research-Project) of [TU Delft](https://github.com/TU-Delft-CSE).

**Note:** The MaxSAT solver used during my research is provided by the Faculty of Electrical Engineering, Mathematics, and Computer Science. As it is still under development, it is not yet made public. Therefore, to reproduce the experiments, please refer to the *implementation details*, mentioned in Section 4.2 of [my thesis](https://repository.tudelft.nl/islandora/object/uuid:0c85f1d6-5471-42e7-9794-091ff7b40c40?collection=education).

# Abstract
The multi-mode resource-constrained project scheduling problem (MRCPSP) is an extension of the resource-constrained project scheduling problem (RCPSP), which allows activities to be executed in multiple modes. The state-of-the-art solutions for solving this NP-Hard problem are dedicated algorithms and (meta-)heuristics. However, this paper considers a more flexible approach using a MaxSAT solver. The idea is to replace the existing variable selection strategy of the solver, Variable State Independent Decaying Sum (VSIDS), with two scheduling heuristics, Earliest Starting Time (EST) and Shortest Feasible Mode (SFM). We examine that combining the three heuristics results in a more efficient solver. In contrast, scheduling rules alone lead to a solver that performs significantly worse on any of the chosen metrics and benchmarks.

# MRCPSP
The **M**ulti-mode **R**esource-**C**onstrained **P**roject **S**cheduling **P**roblem (MRCPSP) is a generalization of the RCPSP. It allows activities to be executed in multiple modes while using 2 types of resources, renewable and non-renewable. Renewable resources are limited at deterministic points in time, e.g., the number of machines/people available. In contrast, non-renewable resources are limited for the whole makespan. Each mode can have a distinct processing time and/or resource requirements. Furthermore, the activities in the MRPCSP are subject to precedence relations. Finally, the goal of the MRCPSP in most cases is to minimize the makespan (the time it takes to complete all activities).

The MRCPSP can also be modeled as a directed acyclic graph (DAG). An example of an MRCPSP instance with 5 non-dummy activities, 1 renewable, and 1 non-renewable resource is shown in the figure below. Each node represents an activity, each edge - a precedence relation, and each label under a node - a corresponding mode for that activity, defined as a triplet of the mode's processing time, and its demand for renewable and non-renewable resources.

![](mrcpsp_graph.png)

The optimal schedule for the example is shown in the figure below. Each square represents an activity and the selected mode. Note that the capacity for the renewable resource is 4 and for the non-renewable - 8.

![](mrcpsp_schedule.png)

# Poster

![](poster.png)
