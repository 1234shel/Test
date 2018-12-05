from ortools.sat.python import cp_model
import random

def main():
  model = cp_model.CpModel()
  numRounds=4;
  numTeams=8;
  dist = {}
  random.seed(1001)
  for i in range(0, numTeams):
      dist[i, i] = 0
      for j in range(i + 1, numTeams):
          dist[i, j] = random.randint(1, 101);
          dist[j, i] = dist[i, j]

  home = {};
  # set variable range
  for i in range(0, numTeams):
      for j in range(0, numRounds):
          home[i, j] = model.NewIntVar(0, 1, 'Team' + str(i) + ' is Home in Round' + str(j));

  opponent={}
  for i in range(numTeams):
      for j in range(numRounds):
          opponent[i,j] = model.NewIntVar(0, numTeams-1, "matches")

  for i in range(numTeams):
    model.AddAllDifferent([opponent[(i,j)] for j in range(numRounds)])
    model.Add(sum([home[(i,j)] for j in range(numRounds)])==2)
    model.Add((home[i, j]+home[i,j+1] for j in range(numRounds-1)) == 1)
    for j in range(numRounds):
        for k in range(numTeams):
            model.Add(home[i,j]+home[i,k]==1).OnlyEnforceIf(opponent[i,j]==1)






  model.Minimize(sum([dist[i,opponent[i, j]] for j in range(0,numRounds)]for i in range(0,numTeams)))
  # Create the decision builder.
  solver = cp_model.CpSolver()
  status = solver.Solve(model)

if __name__ == '__main__':
  main()