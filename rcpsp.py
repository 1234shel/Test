from __future__ import print_function

import collections

# Import Python wrapper for or-tools CP-SAT solver.
from ortools.sat.python import cp_model


def MinimalRCPSP():
    """Minimal jobshop problem."""
    # Create the model.
    model = cp_model.CpModel()

    jobs_data = [  # task = (resource_req, processing_time).
        [2, 3], [2, 2], [2, 2],[3,4] ];
    job_pred=[[],[0],[0],[1,2]];

    jobs_count = len(jobs_data)
    all_jobs = range(jobs_count)
    resources=1;

    # Compute horizon.
    horizon = 100#sum(task[1]  for task in jobs_data)
    task_type = collections.namedtuple('task_type', 'start end interval')

    # Create jobs.
    all_tasks = {}
    for taskid, task  in enumerate(jobs_data):
        start_var = model.NewIntVar(1, horizon,'start_'+str(taskid))
        duration = task[1]-1
        end_var = model.NewIntVar(1, horizon, 'end_' +str(taskid))
        interval_var = model.NewIntervalVar(start_var, duration, end_var, 'interval_'+str(taskid))
        all_tasks[taskid] = task_type(start=start_var, end=end_var, interval=interval_var)

    intervals = []
    demands=[]

    for task_id, task in enumerate(jobs_data):
        intervals.append(all_tasks[task_id].interval)
        demands.append(task[0])
    model.AddCumulative(intervals,demands,3)

    # Add precedence contraints.
    for taskid in all_jobs:
        for pred_id in job_pred[taskid]:
            model.Add(all_tasks[taskid].start > all_tasks[pred_id].end)

    obj_var = model.NewIntVar(1, horizon, 'makespan')

    model.AddMaxEquality(
        obj_var,
        [all_tasks[taskid].end for taskid in all_jobs])
    model.Minimize(obj_var)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        # Print out makespan.
        print('Optimal Schedule Length: %i' % solver.ObjectiveValue())
        print()

        for taskid in all_jobs:
            print(str(taskid) + ': Start: ' + str(solver.Value(all_tasks[taskid].start)) + ' End:' + str(
                solver.Value(all_tasks[taskid].end)))

MinimalRCPSP()