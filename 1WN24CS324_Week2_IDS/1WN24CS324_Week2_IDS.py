class EightPuzzleIDS:
    def __init__(self, start_state, goal_state):
        self.start_state = start_state
        self.goal_state = goal_state

    def get_neighbors(self, state):
        neighbors = []
        row, col = -1, -1
        for r in range(3):
            for c in range(3):
                if state[r][c] == 0:
                    row, col = r, c
                    break

        moves = [
            (-1, 0, "UP"),
            (1, 0, "DOWN"),
            (0, -1, "LEFT"),
            (0, 1, "RIGHT")
        ]

        for dr, dc, move_name in moves:
            new_r, new_c = row + dr, col + dc
            if 0 <= new_r < 3 and 0 <= new_c < 3:
                new_board = [list(r) for r in state]
                new_board[row][col], new_board[new_r][new_c] = new_board[new_r][new_c], new_board[row][col]
                neighbors.append((tuple(tuple(r) for r in new_board), move_name))

        return neighbors

    def _dls(self, state, limit, path):
        if state == self.goal_state:
            return path

        if limit <= 0:
            return "CUTOFF"

        cutoff_occurred = False

        for neighbor_state, move in self.get_neighbors(state):
            if neighbor_state in [node[0] for node in path]:
                continue

            result = self._dls(neighbor_state, limit - 1, path + [(neighbor_state, move)])

            if result == "CUTOFF":
                cutoff_occurred = True
            elif result is not None:
                return result

        return "CUTOFF" if cutoff_occurred else None

    def solve_ids(self, max_limit=20):
        for limit in range(max_limit + 1):
            result = self._dls(self.start_state, limit, [(self.start_state, "START")])

            if result != "CUTOFF" and result is not None:
                moves = [move for state, move in result if move != "START"]
                return moves, limit

        return None, max_limit


def print_board(board):
    for row in board:
        print(" ".join(str(tile) for tile in row))


start = (
    (1, 2, 3),
    (4, 5, 6),
    (0, 7, 8)
)

goal = (
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 0)
)

print("Initial State:")
print_board(start)

print("\nGoal State:")
print_board(goal)

puzzle = EightPuzzleIDS(start, goal)
moves, depth = puzzle.solve_ids(max_limit=10)

print("\n--- IDS Search Result ---")
print("Moves to reach goal:", moves)
print("Optimal depth found:", depth)