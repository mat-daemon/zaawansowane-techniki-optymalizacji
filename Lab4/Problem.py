class SolutionNode:
    def __init__(self, solution, lower_bound):
        self.solution = solution
        self.children_solutions = []
        self.lower_bound = lower_bound


class Problem:
    def __init__(self, trivial_solution, init_solution, evaluation_function, generate_children_solutions, calculate_lower_bound):
        self.trivial_solution = SolutionNode(trivial_solution, None)
        self.init_solution = SolutionNode(init_solution, None)
        self.evaluation_function = evaluation_function
        self._generate_children_solutions = generate_children_solutions
        self.calculate_lower_bound = calculate_lower_bound

    def generate_children_solutions(self, solution):
        if len(solution.children_solutions) == 0:
            children_solutions = self._generate_children_solutions(solution.solution)
            for s in children_solutions:
                solution.children_solutions.append(SolutionNode(s, self.calculate_lower_bound(solution.solution)))