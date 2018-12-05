from __future__ import print_function
from ortools.linear_solver import pywraplp


def main():
  # Create the solver.
  solver = pywraplp.Solver('SolveSimpleSystem',
                           pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
  #Define data set
  values = [360, 83, 59, 130, 431, 67, 230, 52, 93,
            125, 670, 892, 600, 38, 48, 147, 78, 256,
            63, 17, 120, 164, 432, 35, 92, 110, 22,
            42, 50, 323, 514, 28, 87, 73, 78, 15,
            26, 78, 210, 36, 85, 189, 274, 43, 33,
            10, 19, 389, 276, 312]

  weights = [7, 0, 30, 22, 80, 94, 11, 81, 70,
              64, 59, 18, 0, 36, 3, 8, 15, 42,
              9, 0, 42, 47, 52, 32, 26, 48, 55,
              6, 29, 84, 2, 4, 18, 56, 7, 29,
              93, 44, 71, 3, 86, 66, 31, 65, 0,
              79, 20, 65, 52, 13]

  capacities = [850]

  #create decision variables
  x = {};
  for i in range(0, len(values)):
      x[i] = solver.IntVar(0, 1, 'item' + str(i));

  #create capacity constraint
  solver.Add(solver.Sum([weights[i]*x[i] for i in range(len(weights))]) <= capacities[0])

  #create objective function which maximizes profit
  solver.Maximize(solver.Sum([values[i] * x[i] for i in range(len(values))]))

  #call solver and display obtained solution
  solver.Solve();
  packed_items = [i for i in range(0, len(weights))
                  if x[i].solution_value() == 1]
  print(packed_items)


if __name__ == '__main__':
  main()