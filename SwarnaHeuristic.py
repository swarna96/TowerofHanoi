hueristicSummary = "Moves needed to place the disks on the right peg"

def  hanoi_heuristic(state):
    """
    Calculates the heuristic for the Tower of Hanoi problem as the sum of distances
    each disc needs to move to get to the target peg. Assumes the target peg is the last peg.
    """
    goal_peg_index = len(state) - 1  # Target peg is the last peg
    heuristic_value = 0

    # Check each peg and each disc on the peg
    for peg_index, peg in enumerate(state):
        for disc in peg:
            # If the disc is not on the goal peg
            if peg_index != goal_peg_index:
                # If the disc is the smallest on its current peg and the target peg is empty or
                # the top disc on the target peg is larger than the current disc,
                # it can move directly to the target peg.
                if disc < min(peg, default=float('inf')) and \
                   (not state[goal_peg_index] or disc < state[goal_peg_index][-1]):
                    heuristic_value += 1
                else:
                    # Otherwise, it takes at least two moves
                    heuristic_value += 2

    return heuristic_value