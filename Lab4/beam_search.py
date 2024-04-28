from Problem import *


# Beam search uses BFS - queue
# and adds max k nodes to the queue
def beam_search(problem: Problem, max_number_of_nodes):
    upper_bound = problem.evaluation_function(problem.init_solution.solution)
    queue = []
    best_solution = problem.init_solution.solution

    problem.generate_children_solutions(problem.trivial_solution)

    for s in problem.trivial_solution.children_solutions:
        queue.append(s)

    while len(queue) > 0:
        solution = queue.pop(0)
        problem.generate_children_solutions(solution)

        if len(solution.children_solutions) == 0:
            solution_evaluation = problem.evaluation_function(solution.solution)
            if solution_evaluation <= upper_bound:
                upper_bound = solution_evaluation
                best_solution = solution.solution

        else:
            children_solutions = []
            for s in solution.children_solutions:
                if s.lower_bound < upper_bound:
                    children_solutions.append(s)
            children_solutions.sort(key=lambda cs: cs.lower_bound)
            queue.extend(children_solutions[0:min(max_number_of_nodes, len(children_solutions))])


    return best_solution, upper_bound
