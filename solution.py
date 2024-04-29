class Solution:
    def __init__(self, last_state, filename, solution_found):
        self.solution = []
        if solution_found:
            self.print_solution(self.extract_solution(last_state))
        self.write_solution_to_file(filename)

    def extract_solution(self, last_state):
        parent = last_state
        while parent:
            self.solution.append(parent)
            parent = parent.get_parent()
        self.solution.reverse()
        self.solution.pop(0)
        return self.solution

    def print_solution(self, solution):
        print(f"Total Steps: {len(solution)}")

    def write_solution_to_file(self, filename):
        # Implement your file writing logic here
        pass
    