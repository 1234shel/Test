from __future__ import print_function

import collections

# Import Python wrapper for or-tools CP-SAT solver.
from ortools.sat.python import cp_model


def MinimalRCPSP():
    """Minimal rcpsp problem."""
    # Create the model.
    model = cp_model.CpModel()

    #define instance data
    task_data = [  # task = (duration, resource_req).
        #[3,2], [1, 2], [2, 2],[4,3] ];
        [3,4],[6,3],[2,2],[4,3],[5,1],[3,2],[4,4],[1,6]]
    task_pred=[
        #[],[0],[0],[1,2]]; #predecessors
        [],[],[0],[0],[0],[1],[2,3,4],[5]]
    task_count = len(task_data)
    all_tasks = range(task_count)
    resourceCapacity=7;

    # Compute horizon.
    horizon = sum(task[0]  for task in task_data)

    #Define decision variables
    task_type = collections.namedtuple('task_type', 'start end interval')

    all_tasks = {}
    for taskid, task  in enumerate(task_data):
        start_var = model.NewIntVar(0, horizon,'start_'+str(taskid))
        duration = task[0]
        end_var = model.NewIntVar(0, horizon, 'end_' +str(taskid))
        interval_var = model.NewIntervalVar(start_var, duration, end_var, 'interval_'+str(taskid))
        all_tasks[taskid] = task_type(start=start_var, end=end_var, interval=interval_var)

    #resource constraints
    intervals = []
    demands=[]
    for taskid, task in enumerate(task_data):
        intervals.append(all_tasks[taskid].interval)
        demands.append(task[1])
    model.AddCumulative(intervals,demands,resourceCapacity)

    # Add precedence contraints.
    for taskid in all_tasks:
        for pred_id in task_pred[taskid]:
            model.Add(all_tasks[taskid].start >= all_tasks[pred_id].end)

    #Define objective function: minimize makespan
    obj_var = model.NewIntVar(0, horizon, 'makespan')
    model.AddMaxEquality(
        obj_var,
        [all_tasks[taskid].end for taskid in all_tasks])
    model.Minimize(obj_var)

    #solve and disply result
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        # Print out makespan.
        print('Optimal Schedule Length: %i' % solver.ObjectiveValue())
        print()

        for taskid in all_tasks:
            print(str(taskid+1) + ': Start: ' + str(solver.Value(all_tasks[taskid].start)) + ' End:' + str(
                solver.Value(all_tasks[taskid].end)))

MinimalRCPSP()