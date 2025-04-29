from collections import deque
import heapq



# Graph for BFS/DFS (Question 1)
graph = {
    'Addis Ababa': ['Ambo', 'Debre Berhan', 'Adama', 'Lalibela', 'Dire Dawa'],
    'Ambo': ['Addis Ababa', 'Nekemte'],
    'Debre Berhan': ['Addis Ababa', 'Debre Sina'],
    'Debre Sina': ['Debre Berhan', 'Kemise', 'Debre Markos'],
    'Adama': ['Addis Ababa', 'Mojo', 'Dire Dawa'],
    'Mojo': ['Adama', 'Dilla'],
    'Dire Dawa': ['Addis Ababa', 'Harar'],
    'Harar': ['Dire Dawa', 'Babile'],
    'Babile': ['Harar'],
    'Debre Markos': ['Debre Sina', 'Finote Selam'],
    'Finote Selam': ['Debre Markos', 'Bahir Dar'],
    'Bahir Dar': ['Finote Selam', 'Gonder', 'Azezo'],
    'Gonder': ['Bahir Dar', 'Metema', 'Lalibela'],
    'Lalibela': ['Addis Ababa', 'Gonder', 'Sekota', 'Woldia'],
    'Woldia': ['Lalibela', 'Samara'],
    'Samara': ['Woldia', 'Mekelle'],
    'Mekelle': ['Samara', 'Axum'],
    'Dilla': ['Mojo', 'Hawassa'],
    'Hawassa': ['Dilla', 'Arba Minch', 'Yabelo'],
    'Arba Minch': ['Hawassa', 'Basketo'],
    'Yabelo': ['Hawassa', 'Moyale'],
    'Moyale': ['Yabelo']
}

# Graph with costs for UCS (Question 2)
graph_with_costs = {
    'Addis Ababa': [('Ambo', 120), ('Debre Berhan', 130), ('Adama', 80), ('Lalibela', 300)],
    'Ambo': [('Addis Ababa', 120), ('Nekemte', 200)],
    'Debre Berhan': [('Addis Ababa', 130), ('Debre Sina', 90)],
    'Adama': [('Addis Ababa', 80), ('Mojo', 150), ('Dire Dawa', 280)],
    'Mojo': [('Adama', 150), ('Dilla', 180)],
    'Dire Dawa': [('Addis Ababa', 280), ('Harar', 100)],
    'Harar': [('Dire Dawa', 100), ('Babile', 120)],
    'Dilla': [('Mojo', 180), ('Hawassa', 90)],
    'Hawassa': [('Dilla', 90), ('Arba Minch', 200), ('Yabelo', 50)],
    'Yabelo': [('Hawassa', 50), ('Moyale', 80)],
    'Moyale': [('Yabelo', 80)]
}

# Heuristics for A* (Straight-line distance to Moyale)
heuristics = {
    'Addis Ababa': 750,
    'Ambo': 720,
    'Debre Berhan': 700,
    'Adama': 650,
    'Mojo': 600,
    'Dire Dawa': 580,
    'Harar': 550,
    'Dilla': 500,
    'Hawassa': 400,
    'Yabelo': 200,
    'Moyale': 0,
    'Lalibela': 600  # Example value
}


coffee_values = {
    'Addis Ababa': 2,
    'Harar': 9,
    'Gonder': 7,
    'Lalibela': 8,
    'Hawassa': 4
}



class GraphSearch:
    """Handles BFS and DFS"""
    def __init__(self, graph):
        self.graph = {k.lower(): [n.lower() for n in v] for k, v in graph.items()}
    
    def search(self, start, goal, strategy='bfs'):
        start = start.lower()
        goal = goal.lower()
        visited = set()
        queue = deque([(start, [start])])
        
        while queue:
            if strategy == 'bfs':
                current, path = queue.popleft()
            elif strategy == 'dfs':
                current, path = queue.pop()
            
            if current == goal:
                return path
            
            if current not in visited:
                visited.add(current)
                for neighbor in self.graph.get(current, []):
                    if neighbor not in visited:
                        queue.append((neighbor, path + [neighbor]))
        return None

class UniformCostSearch:
   
    @staticmethod
    def find_path(graph, start, goal):
        graph_lower = {k.lower(): [(n.lower(), c) for n, c in v] for k, v in graph.items()}
        start = start.lower()
        goal = goal.lower()
        priority_queue = [(0, start, [start])]
        visited = set()
        
        while priority_queue:
            cost, current, path = heapq.heappop(priority_queue)
            if current == goal:
                return path, cost
            if current in visited:
                continue
            visited.add(current)
            
            for neighbor, edge_cost in graph_lower.get(current, []):
                heapq.heappush(priority_queue, (cost + edge_cost, neighbor, path + [neighbor]))
        
        return None, float('inf')

class AStarSearch:
   
    @staticmethod
    def find_path(graph, heuristics, start, goal):
        graph_lower = {k.lower(): [(n.lower(), c) for n, c in v] for k, v in graph.items()}
        heuristics_lower = {k.lower(): v for k, v in heuristics.items()}
        start = start.lower()
        goal = goal.lower()
        priority_queue = [(heuristics_lower[start], 0, start, [start])]
        visited = set()
        
        while priority_queue:
            f_cost, g_cost, current, path = heapq.heappop(priority_queue)
            if current == goal:
                return path
            if current in visited:
                continue
            visited.add(current)
            
            for neighbor, edge_cost in graph_lower.get(current, []):
                new_g = g_cost + edge_cost
                new_f = new_g + heuristics_lower.get(neighbor, 0)
                heapq.heappush(priority_queue, (new_f, new_g, neighbor, path + [neighbor]))
        
        return None

class MiniMaxCoffee:
    
    @staticmethod
    def minimax(node, depth, maximizing_player, coffee_values, graph):
        node = node.lower()
        graph_lower = {k.lower(): [n.lower() for n in v] for k, v in graph.items()}
        coffee_lower = {k.lower(): v for k, v in coffee_values.items()}
        
        if depth == 0 or node not in graph_lower:
            return coffee_lower.get(node, 0)
        
        if maximizing_player:
            value = -float('inf')
            for neighbor in graph_lower.get(node, []):
                eval = MiniMaxCoffee.minimax(neighbor, depth-1, False, coffee_values, graph)
                value = max(value, eval)
            return value
        else:
            value = float('inf')
            for neighbor in graph_lower.get(node, []):
                eval = MiniMaxCoffee.minimax(neighbor, depth-1, True, coffee_values, graph)
                value = min(value, eval)
            return value


if __name__ == "__main__":
   
    print("=== BFS Path ===")
    bfs_solver = GraphSearch(graph)
    print(bfs_solver.search('Addis Ababa', 'Lalibela', 'bfs'))  
 
    print("\n=== UCS Path ===")
    ucs_path, ucs_cost = UniformCostSearch.find_path(graph_with_costs, 'Addis Ababa', 'Lalibela')
    print(f"Path: {ucs_path}, Cost: {ucs_cost}")  
    
    # Test A*
    print("\n=== A* Path ===")
    astar_path = AStarSearch.find_path(graph_with_costs, heuristics, 'Addis Ababa', 'Moyale')
    print(f"Path: {astar_path}")  
    
    print("\n=== MiniMax Result ===")
    best_score = MiniMaxCoffee.minimax('Addis Ababa', depth=4, maximizing_player=True, 
                                      coffee_values=coffee_values, graph=graph)
    print(f"Best Coffee Quality: {best_score}") 