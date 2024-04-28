from RandomNumberGenerator import RandomNumberGenerator
import random
from branch_and_bound import *
from beam_search import *
import time


rd = RandomNumberGenerator(4367)
number_of_tasks = 7

execution_time = [rd.nextInt(1, 30) for _ in range(number_of_tasks)]
tasks_weights = [rd.nextInt(1, 30) for _ in range(number_of_tasks)]

execution_time_sum = sum(execution_time)

deadlines = [rd.nextInt(1, execution_time_sum) for _ in range(number_of_tasks)]

trivial_solution = [None for _ in range(number_of_tasks)]

init_solution = [i for i in range(number_of_tasks)]
random.shuffle(init_solution)


def generate_children_solutions(solution):
    ordered_tasks = [task for task in solution if task is not None]
    remaining_tasks = [task for task in range(number_of_tasks) if task not in ordered_tasks]

    next_solutions = []

    for task in remaining_tasks:
        next_solution = solution.copy()
        next_solution[len(ordered_tasks)] = task
        next_solutions.append(next_solution)

    return next_solutions


def evaluation_function(solution):
    waged_delayed_sum = 0
    finish_time = solution[0]

    for task in solution:
        finish_time += execution_time[task]
        delay = max(0, finish_time-deadlines[task])
        waged_delayed_sum += delay*tasks_weights[task]

    return waged_delayed_sum


# https://web-static.stern.nyu.edu/om/faculty/pinedo/scheduling/shakhlevich/handout06.pdf
# We use here an auxiliary result: an optimal schedule for problem 1| dj =d | ΣTj with equal due dates can be
# obtained by SPT-rule.
def calculate_lower_bound_latest_deadline(partial_solution):
    ordered_tasks = [task for task in partial_solution if task is not None]
    remaining_tasks = [task for task in range(number_of_tasks) if task not in ordered_tasks]
    latest_deadline = max([deadlines[i] for i in remaining_tasks])

    remaining_tasks_execution_time = [(task, execution_time[task]) for task in remaining_tasks]
    remaining_tasks_execution_time.sort(key=lambda x: x[1])

    lower_bound = 0
    finish_time = 0

    for task in partial_solution:
        if task is None:
            break
        finish_time += execution_time[task]
        delay = max(0, finish_time - deadlines[task])
        lower_bound += delay * tasks_weights[task]

    for task, exe_time in remaining_tasks_execution_time:
        finish_time += exe_time
        delay = max(0, finish_time - latest_deadline)
        lower_bound += delay * tasks_weights[task]

    return lower_bound


def calculate_lower_bound_weight_time_ratio(partial_solution):
    ordered_tasks = [task for task in partial_solution if task is not None]
    remaining_tasks = [task for task in range(number_of_tasks) if task not in ordered_tasks]

    remaining_tasks_execution_time = [(task, float(tasks_weights[task])/float(execution_time[task])) for task in remaining_tasks]
    remaining_tasks_execution_time.sort(key=lambda x: x[1], reverse=True)

    lower_bound = 0
    finish_time = 0

    for task in partial_solution:
        if task is None:
            break
        finish_time += execution_time[task]
        delay = max(0, finish_time - deadlines[task])
        lower_bound += delay * tasks_weights[task]

    for task, _ in remaining_tasks_execution_time:
        finish_time += execution_time[task]
        delay = max(0, finish_time - deadlines[task])
        lower_bound += delay * tasks_weights[task]

    return lower_bound


print("Single Machine Scheduling Problem")
print(f'Number of tasks     : {number_of_tasks}')
print(f'Tasks execution time: {execution_time}')
print(f'Tasks weights       : {tasks_weights}')
print(f'Tasks deadlines     : {deadlines}')
print(f'Trivial solution    : {trivial_solution}')
print(f'Init solution       : {init_solution}')
print(f'Init sol upper bound: {evaluation_function(init_solution)}')

start = time.time()
smsproblem = Problem(trivial_solution, init_solution, evaluation_function, generate_children_solutions, calculate_lower_bound_latest_deadline)
best_solution, upper_bound = branch_and_bound(smsproblem)
# best_solution, upper_bound = beam_search(smsproblem, 3)
end = time.time()

print(f'Best solution       : {best_solution}')
print(f'Upper bound         : {upper_bound}')
print(f'Time elapsed        : {end-start}')
