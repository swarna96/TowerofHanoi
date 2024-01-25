import heapq
import time
import SwarnaHeuristic as heuristic

def A_Star_Final(n, execution_time_limit):
# The starting state is a tuple representing rods; each rod is a tuple of discs in descending order of size.
    start_state = (tuple(range(n, 0, -1)), tuple(), tuple())
    nodes_generated = 0

    # The open list contains states to be evaluated, starting with the initial state.
    # The list is initiated with a tuple containing the heuristic value, the start state and an empty path
    open_list = [(heuristic.hanoi_heuristic(start_state), start_state, [], 0, ())]
    # Transform the open_list into a heap queue to efficiently get the state with the lowest heuristic value
    heapq.heapify(open_list)

    # A set to keep track of already evaluated states
    closed_list = []

    # Record the start time for time tracking
    start_time = time.time()

    while open_list:
        if time.time() > execution_time_limit:
            break # This breaks the while loop when time limit is exceeded

    # Continue processing states until there are no more states or the time limit is exceeded.
    # while open_list and total_time_elapsed <= execution_time_limit:
        # Remove and return the lowest heuristic value state from the heap queue.
        current_f_value, current_state, path, current_g_value, current_parent = heapq.heappop(open_list)

        # If the heuristic value of the current state is 0 (i.e., no discs on the first rod), a solution is found.
        # This is a check for the goal state. The function will return if the goal state is reached.
        if heuristic.hanoi_heuristic(current_state) == 0:
            return reconstruct_path(start_state, path), nodes_generated, len(closed_list)
        
        # Add the current state to the closed set to avoid reevaluation          
        closed_list.append((current_f_value, current_state, path, current_g_value, current_parent))

        # Generate all possible states from the current state by moving a disc from one rod to another
        for move_from in range(len(current_state)):
            for move_to in range(len(current_state)):
                # Check that we are not moving a disc to where it already is and that the move is legal
                if move_from != move_to and current_state[move_from]:
                    if not current_state[move_to] or current_state[move_from][-1] < current_state[move_to][-1]:
                        # Create a new state reflecting the move
                        new_state = list(map(list, current_state))
                        disc = new_state[move_from].pop()
                        new_state[move_to].append(disc)
                        new_state = tuple(map(tuple, new_state))                       
                        new_path = path + [(move_from, move_to)]
                        g_value = len(closed_list)
                        f_value = g_value + heuristic.hanoi_heuristic(new_state)
                        nodes_generated +=1
                                       
                        is_on_open_list = False
                        is_on_closed_list = False

                        #Check if it is already in the open list with a better g value     
                        for index, (existing_f, existing_state, existing_path, existing_g, existing_parent) in enumerate(open_list):
                            if existing_state == new_state:
                                is_on_open_list = True
                                if g_value < existing_g:
                                    open_list[index] = (f_value, new_state, new_path, g_value, current_state)
                                    heapq.heapify(open_list)  # Reorder the open list based on the new f value
                                break

                        #Check if it is already in the closed list with a better g value
                        if not is_on_open_list:
                            for index, (existing_f, existing_state, existing_path, existing_g, existing_parent) in enumerate(closed_list):
                                if existing_state == new_state:
                                    is_on_closed_list = True
                                    if g_value < existing_g:
                                        closed_list[index] = (f_value, new_state, new_path, g_value, current_state)
                                         
                                        heapq.heappush(open_list, (f_value, new_state, new_path, g_value, current_state))
                                        heapq.heapify(open_list)
                                    break
                        if (not is_on_open_list) & (not is_on_closed_list):                            
                            heapq.heappush(open_list, (f_value, new_state, new_path, g_value, current_state))
                            heapq.heapify(open_list) 

    # if no solution is found withint the time limit, return None for the path and the number of the nodes generated and expanded
    print(f"Execution time limit exceeded, could not find solution for {n} disks")
    return None, nodes_generated, len(closed_list)


def reconstruct_path(initial_state, moves):
    # Start with the initial state
    current_state = list(map(list, initial_state))
    # This will hold the sequence of states leading to the solution
    sequence_of_states = [initial_state]

    # Apply each move to the current state
    for move in moves:
        move_from, move_to = move
        # Pop the top disc from the move_from rod and append it to the move_to rod
        disc = current_state[move_from].pop()
        current_state[move_to].append(disc)
        # Append the new state to the sequence
        sequence_of_states.append(tuple(map(tuple, current_state)))

    return sequence_of_states
