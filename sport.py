from __future__ import print_function
from ortools.linear_solver import pywraplp
import random

def main():
  # Create the solver.
  solver = pywraplp.Solver('SolveSimpleSystem',
                           pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

  #generate data set
  random.seed(1001);
  numTeams=8;
  dist={}
  for i in range(0,numTeams):
      dist[i,i]=0
      for j in range(i+1,numTeams):
          dist[i,j]=random.randint(1,101);
          dist[j,i]=dist[i,j]

  #create decision variables x[i,j]=1 means match between i and j with i being home
  x = {};
  for i in range(0, numTeams):
      for j in range(0,numTeams):
          x[i,j] = solver.IntVar(0, 1, 'match' + str(i)+' '+str(j));

  #one home match only
  for i in range(0,numTeams):
      solver.Add(solver.Sum([x[i, j] for j in range(0,numTeams)]) == 1)

  #one away match only
  for i in range(0,numTeams):
      solver.Add(solver.Sum([x[j, i] for j in range(0,numTeams)]) == 1)

  #cant play against myself
  for i in range(0,numTeams):
      solver.Add(x[i, i] == 0)

  #cant play same team twice
  for i in range(0,numTeams):
      for j in range(i+1,numTeams):
          solver.Add(x[i,j]+x[j,i] <= 1)

  #create objective function which minimizes travel distance
  solver.Minimize(solver.Sum([dist[i,j] * x[i, j] for i in range(0,numTeams)
                              for j in range(0,numTeams)]))

  #solve problem and display solution
  solver.Solve()

  for i in range(0, numTeams):
      for j in range(0,numTeams):
          if x[i,j].solution_value()>0:
              print('match between: '+ str(i) + ' '+str(j) );


if __name__ == '__main__':
    main()

