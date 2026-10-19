import random

class Node:
    def __init__(self, state, value):
        self.STATE = state
        self.VALUE = value

class NQueensProblem:
    def __init__(self, N):
        self.N = N
        self.INITIAL_STATE = [random.randint(0, N - 1) for _ in range(N)]

    def calculate_value(self, state):
        max_pairs = (self.N * (self.N - 1)) // 2
        conflicts = 0
        for i in range(self.N - 1):
            for j in range(i + 1, self.N):
                if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                    conflicts += 1
        return max_pairs - conflicts

    def get_successors(self, current_node):
        successors = []
        state = current_node.STATE
        for col in range(self.N):
            original_row = state[col]
            for row in range(self.N):
                if row != original_row:
                    neighbor_state = list(state)
                    neighbor_state[col] = row
                    value = self.calculate_value(neighbor_state)
                    successors.append(Node(neighbor_state, value))
        return successors

def make_node(problem, state):
    value = problem.calculate_value(state)
    return Node(state, value)

def hill_climbing(problem, history):
    current = make_node(problem, problem.INITIAL_STATE)
    history.append(list(current.STATE))
    sideways_moves = 0
    max_sideways = 100
    
    while True:
        successors = problem.get_successors(current)
        if not successors:
            return current.STATE
        
        random.shuffle(successors) 
        neighbor = max(successors, key=lambda node: node.VALUE)
        
        if neighbor.VALUE < current.VALUE:
            return current.STATE
        
        if neighbor.VALUE == current.VALUE:
            if sideways_moves >= max_sideways:
                return current.STATE
            sideways_moves += 1
            
        current = neighbor
        history.append(list(current.STATE))

def random_restart_hill_climbing(N):
    target_value = (N * (N - 1)) // 2
    while True:
        history = []
        problem = NQueensProblem(N)
        state_solution = hill_climbing(problem, history)
        final_value = problem.calculate_value(state_solution)
        if final_value == target_value:
            return history

def print_board(state):
    N = len(state)
    print("State Array:", state)
    for row in range(N):
        line = ""
        for col in range(N):
            line += " Q " if state[col] == row else " . "
        print(line)
    print("-" * (N * 3))

if __name__ == "__main__":
    N = 4
    steps_history = random_restart_hill_climbing(N)
    
    for i, step_state in enumerate(steps_history):
        print(f"Step {i}:")
        print_board(step_state)