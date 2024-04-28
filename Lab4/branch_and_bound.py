from Problem import *


def branch_and_bound(problem: Problem):
    upper_bound = problem.evaluation_function(problem.init_solution.solution)
    stack = []
    best_solution = problem.init_solution.solution

    problem.generate_children_solutions(problem.trivial_solution)

    for s in problem.trivial_solution.children_solutions:
        stack.append(s)

    while len(stack) > 0:
        solution = stack.pop()
        problem.generate_children_solutions(solution)

        if len(solution.children_solutions) == 0:
            solution_evaluation = problem.evaluation_function(solution.solution)
            if solution_evaluation <= upper_bound:
                upper_bound = solution_evaluation
                best_solution = solution.solution

        else:
            for s in solution.children_solutions:
                if s.lower_bound < upper_bound:
                    stack.append(s)

    return best_solution, upper_bound
