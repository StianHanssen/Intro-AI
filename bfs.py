from board import Board
from time import time


def bfs(board):
    """Calculates shortest path on board using Breadth-First Search alogrithm.
    Args:
        board (Board): Board being the graph the alorithm will use

    Returns:
        Tuple of form (time, string representation of board with path)
    """
    start_time = time()  # Sets start checkpoint for time

    visited = set()  # A set with the closed nodes/cells
    queue = [board.START]  # A queue to keep the track of next cell

    while queue:  # As long as there are elements in queue
        cell = queue.pop(0)  # Pop first element from queue
        if cell == board.END:  # If we have reached B
            return time() - start_time, board.get_path_str(queue, visited)  # Return finish time and print the board
        for neighbour in board.get_neighbours(cell):  # Iterate over all neighbours
            if neighbour not in visited:  # If neighbour is not closed
                neighbour.set_parent(cell)
                visited.add(neighbour)
                queue.append(neighbour)
