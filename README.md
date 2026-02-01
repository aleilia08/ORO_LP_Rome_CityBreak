# Rome City Break Optimization (Linear Programming)

This project models and solves a **3-day city break in Rome** as a **linear programming optimization problem** using **PuLP** in Python.

The goal is to **minimize the total trip cost** while respecting realistic constraints related to transport, accommodation, food, attractions, and a fixed student budget.

---

## Problem Description
The city break includes:
- Flight cost
- Airport transport (Uber or train)
- Accommodation (hotel, Airbnb, or hostel)
- Daily food expenses
- Paid tourist attractions

The optimization selects the best combination of options such that:
- exactly one transport method is chosen
- exactly one accommodation type is chosen
- minimum food costs are respected
- a minimum number of attractions is visited
- the total cost does not exceed the available budget

---

## Technologies
- Python
- PuLP (Linear & Integer Programming)
- CBC Solver

---

## How to run
1. Install dependencies:
```bash
pip install pulp

2. Run the optimization model:
python rome_citybreak_lp.py
