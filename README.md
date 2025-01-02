# RLFA Constraint Satisfaction Solver

This project implements a **Constraint Satisfaction Problem (CSP)** solver for the **Resource Leveling in Frequency Assignment (RLFA)** problem. It uses advanced algorithms like **Domain Weighted Degree (dom/wdeg)**, **Forward Checking (FC)**, **Conflict-Directed Backjumping (CBJ)**, and **Maintaining Arc Consistency (MAC)** to efficiently solve complex CSPs.

---

## Features

- **Domain Weighted Degree (dom/wdeg)**: A heuristic to select variables for assignment by considering the ratio of domain size to constraint weights.
- **Forward Checking (FC)**: Prunes domains of neighboring variables after assigning a variable.
- **Conflict-Directed Backjumping (CBJ)**: Allows intelligent backtracking by jumping to the root cause of a failure.
- **Maintaining Arc Consistency (MAC)**: Ensures arc consistency through local constraint propagation.
- **Dynamic Constraint Weighting**: Adjusts weights of constraints dynamically based on conflicts.

---

## Project Structure

- **`rlfa` class**: Extends the `csp.CSP` class to model the RLFA problem.
- **Heuristics and Algorithms**:
  - **`dom_wdeg`**: Implements the domain/weighted-degree heuristic.
  - **`forward_checking`**: Implements the forward checking algorithm.
  - **`AC3`**: Maintains arc consistency for the CSP.
  - **`cbj_search`**: Executes the CBJ algorithm with dynamic conflict resolution.
  - **`backtracking_search`**: A classic backtracking search implementation for comparison.
- **Constraint Function**: Custom constraints based on neighbors and specific problem conditions.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/rlfa-csp-solver.git

## Usage

RUN:
```bash
$python solution.py <algorithm> <instance> 
   
    for fc_cbj:           >>python solution.py fc_cbj 2-f24
    for fc_bt:            >>  python solution.py fc_bt ...
    for mac_bt:           >> python solution.py mac_bt
    for min conflicts:    >> python solution.py min_conf ...

