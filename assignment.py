from ortools.linear_solver import pywraplp

def main():
  solver = pywraplp.Solver('SolveAssignmentProblemMIP',
                           pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

  #define data set--6 drivers divided into two teams, 4 customers
  cost = [[90, 76, 75, 70],
          [35, 85, 55, 65],
          [125, 95, 90, 105],
          [45, 110, 95, 115],
          [60, 105, 80, 75],
          [45, 65, 110, 95]]

  team1 = [0, 2, 4]
  team2 = [1, 3, 5]
  numDrivers=len(team1)+len(team2)
  numCustomers=len(cost[1]);
  team_max = 2

  #create decision variables x[i,j]=1 means driver i is attending to customer j
  x = {};
  for i in range(numDrivers):
      for j in range(numCustomers):
        x[i,j] = solver.IntVar(0, 1, 'assign driver' + str(i)+' to cust' +str(j));

  #constraint--each team can have max of two customers
  solver.Add(solver.Sum([x[i,j] for i in team1 for j in range(numCustomers)]) <= team_max)
  solver.Add(solver.Sum([x[i, j] for i in team2 for j in range(numCustomers)]) <= team_max)

  #constraint--each driver must have at max only one customer
  for i in range(numDrivers):
    solver.Add(solver.Sum([x[i, j] for j in range(numCustomers)]) <= 1)

  #each customer must have exactly one driver assigned
  for j in range(numCustomers):
      solver.Add(solver.Sum([x[i, j] for i in range(numDrivers)]) == 1)

  #objective--minimize cost
  solver.Minimize(solver.Sum([cost[i][ j] * x[i, j] for i in range(numDrivers)
                              for j in range(0, numCustomers)]))

  #solve and display solution
  solver.Solve();

  for i in range(0, numDrivers):
      for j in range(0,numCustomers):
          if x[i,j].solution_value()>0:
              print('Driver-Customer: '+ str(i) + ' '+str(j) );

if __name__ == '__main__':
  main()