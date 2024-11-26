# Design-and-Deployment-of-Resilient-Control-Execution-Patterns
This repository is an implementation of the paper in ICCPS'23 titled "Design and Deployment of Resilient Control Execution Patterns" by Ipsita Koley et al. [Course Project for CS637: Embedded and Cyber Physical Systems, Fall 2024]

The uploaded codes contain implementations for various stages in the pipeline mentioned in the paper.
## Dynamic Programming code

The DP_code.py replicates the P and M matrix generation example given in the paper

## Attack library

attack_vectors.m contains the implementation of attack library synthesis using matlab. Gurobi optimizer with YALMIP was used as described in the paper

## MLP and FDI

These perform classification and FDI prediction as mentioned in the paper

## Evaluation
The evaluation.py file verifies the observed method. Here, the predicted attack vector and the corresponding control synthesis are applied to observe system response.

