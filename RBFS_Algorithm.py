import time
import SwarnaHeuristic
class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.g = 0 if parent is None else parent.g + 1
        self.h = SwarnaHeuristic.hanoi_heuristic(state)
        self.f = self.g + self.h

    def is_goal(self):
            # Assuming all discs need to be moved to the third peg.
            return not self.state[0] and not self.state[1]
    
def hanoi_successors(state):
    successors = []
    for i, rod in enumerate(state):
        if rod:
            disc = rod[-1]
            for j, target_rod in enumerate(state):
                if i != j and (not target_rod or disc < target_rod[-1]):
                    new_state = [list(r) for r in state]
                    new_state[i].pop()
                    new_state[j].append(disc)
                    successors.append(tuple(new_state))
    return successors
def rbfs(node, f_limit, execution_time_limit, metrics):
    successor_nodes = []
    
    if node.is_goal():
        return node, 0
    metrics['nodes_expanded'] += 1
    while time.time() < execution_time_limit:
        successors = hanoi_successors(node.state)
        if not successors:
            return None, float('inf')

        for s in successors:
            successor_node = Node(s, node)
            successor_node.f = max(successor_node.f, node.f)
            successor_nodes.append(successor_node)
            metrics['nodes_generated'] += 1

        while True:
            if time.time() >= execution_time_limit:                
                return None, float('inf')
            successor_nodes.sort(key=lambda x: x.f)
            best = successor_nodes[0]
            if best.f > f_limit:
                return None, best.f
            alternative = successor_nodes[1].f if len(successor_nodes) > 1 else float('inf')
            result, best.f = rbfs(best, min(f_limit, alternative), execution_time_limit, metrics)
            successor_nodes[0].f = best.f
            if result:
                return result, 0
          

def rbfs_tower_of_hanoi(num_discs, execution_time_limit):
    initial_config = (tuple(range(num_discs, 0, -1)), (), ())
    initial_state = Node(initial_config)
    metrics = {
            'nodes_generated': 0, # Number of nodes created
            'nodes_expanded': 0 # Number of nodes fully explored
        }
    solution, _= rbfs(initial_state, float('inf'), execution_time_limit, metrics)

    path = []
    while solution:
        path.append(solution.state)
        solution = solution.parent

    if not path:
        print(f"Execution time limit exceeded, could not find solution for {num_discs} disks")
    return reversed(path), metrics['nodes_generated'], metrics['nodes_expanded']

