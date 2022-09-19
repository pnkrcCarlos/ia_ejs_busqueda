from typing import Dict, Tuple
from simpleai.search import (
    SearchProblem,
    breadth_first,
    iterative_limited_depth_first,
    astar,
    greedy,
)
from simpleai.search.viewers import BaseViewer, ConsoleViewer, WebViewer


GOAL = (0, 1, 2, 3, 4, 5, 6, 7, 8)


class EightPuzzleProblem(SearchProblem):
    def __init__(self, initial_state=None):
        super().__init__(initial_state)
        self.penalty: int = 2
        self.moves: Tuple[str] = ("▼", "▶", "◀", "▲")
        self.transformations: Dict[Tuple[int, str], Tuple[int, int]] = {
            (0, "◀"): (1, 0),
            (0, "▲"): (3, 0),
            (1, "▶"): (0, 1),
            (1, "◀"): (2, 1),
            (1, "▲"): (4, 1),
            (2, "▶"): (1, 2),
            (2, "▲"): (5, 2),
            (3, "▼"): (0, 3),
            (3, "◀"): (4, 3),
            (3, "▲"): (6, 3),
            (4, "▼"): (1, 4),
            (4, "▶"): (3, 4),
            (4, "◀"): (5, 4),
            (4, "▲"): (7, 4),
            (5, "▼"): (2, 5),
            (5, "▶"): (4, 5),
            (5, "▲"): (8, 5),
            (6, "▼"): (3, 6),
            (6, "◀"): (7, 6),
            (7, "▼"): (4, 7),
            (7, "▶"): (6, 7),
            (7, "◀"): (8, 7),
            (8, "▼"): (5, 8),
            (8, "▶"): (7, 8),
        }
        self.cartesian: Dict[int, Tuple(int, int)] = {
            0: (0, 0),
            1: (0, 1),
            2: (0, 2),
            3: (1, 0),
            4: (1, 1),
            5: (1, 2),
            6: (2, 0),
            7: (2, 1),
            8: (2, 2),
        }
        self.reversal_positions: Tuple(int, int) = (
            (0, 1),
            (1, 2),
            (3, 4),
            (4, 5),
            (6, 7),
            (7, 8),
            (0, 3),
            (3, 6),
            (1, 4),
            (4, 7),
            (2, 5),
            (5, 8),
        )

    def state_representation(self, state):
        return f"{state[0]} {state[1]} {state[2]}\n{state[3]} {state[4]} {state[5]}\n{state[6]} {state[7]} {state[8]}"

    def actions(self, state):
        act = []
        for move in self.moves:
            if (state.index(0), move) in self.transformations:
                act.append(f"{move}")
        return act

    def result(self, state, action):
        empty_index = state.index(0)
        # print(f"{empty_index=}")
        swap_indices = self.transformations[(empty_index, action)]
        new_state = list(state)
        new_state[swap_indices[1]] = state[swap_indices[0]]
        new_state[swap_indices[0]] = state[swap_indices[1]]
        return tuple(new_state)

    def is_goal(self, state):
        return state == GOAL

    def cost(self, state, action, state2):
        return 1

    def manhattan_sums(self, state) -> int:
        sum = 0
        for i in range(9):
            pos = self.cartesian[state.index(i)]
            goal = self.cartesian[i]
            sum += abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])
        return sum

    def reversals(self, state) -> int:
        count = 0
        for pair in self.reversal_positions:
            if state[pair[0]] == GOAL[pair[1]] and state[pair[1]] == GOAL[pair[0]]:
                count += 1
        return count

    def heuristic(self, state):
        # Cuando hay un par de posiciones que necesitan ser intercambiadas para estar en
        # su posición objetivo es necesario dar una vuelta al tablero. Esto se debería
        # penalizar.
        manhattan = self.manhattan_sums(state)
        penalty = self.penalty * self.reversals(state)
        return manhattan + penalty


initial = (7, 2, 4, 5, 0, 6, 8, 3, 1)
# initial = (4, 3, 2, 1, 0, 5, 6, 7, 8)

problem = EightPuzzleProblem(initial_state=initial)
result = astar(problem, graph_search=True, viewer=ConsoleViewer())

print(result.state)
print(f"Moves: {[m[0] for m in result.path()][1:]}")
# print(f"Time: {sum(times)/len(times)} ms")
