import networkx as nx
import matplotlib.pyplot as plt
class UserJourneyGraph:
    def __init__(self, start_url):
        self.start_url = start_url
        self.graph = nx.DiGraph()

    def add_interaction(self, source_url, destination_url, interaction_type,*args,**kwargs):
        """
        Add an interaction between two pages in the user journey graph.

        :param source_url: The URL of the page where the interaction originated.
        :param destination_url: The URL of the page where the interaction leads to.
        :param interaction_type: Type of interaction (e.g., click, scroll, etc.).
        """
        self.graph.add_edge(source_url, destination_url, interaction_type=interaction_type,*args,**kwargs)

    def visualize_graph(self):
        """
        Visualize the user journey graph.
        """
        import matplotlib.pyplot as plt

        # pos = nx.spring_layout(self.graph)  # Layout for the graph
        pos = nx.spring_layout(self.graph, seed=42)  # Layout for the graph with seed for determinism
        # labels = {node: node for node in self.graph.nodes()}  # Labels for nodes (using URLs)
            # Custom labels for nodes
        labels = {}
        for node in self.graph.nodes():
            if node == self.start_url:
                labels[node] = f"{node}\n(Start URL)"
            else:
                labels[node] = node
        nx.draw(self.graph, pos, with_labels=True, labels=labels, font_weight='bold', node_size=1500, node_color='skyblue')
        edge_labels = {(u, v): d['interaction_type'] for u, v, d in self.graph.edges(data=True)}  # Edge labels
        
        
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)  # Draw edge labels
        
         # Draw edges with red color
        nx.draw_networkx_edges(self.graph, pos, edge_color='red', arrows=True)
        
        plt.savefig('file_name.png')
        plt.close()
        # plt.show()
    
    def dfs_traversal(self, start_node=None):
        """
        Perform depth-first search traversal of the user journey graph.
        
        :param start_node: The starting node for the traversal. If None, uses the start_url.
        """
        if start_node is None:
            start_node = self.start_url

        visited = set()

        def dfs_util(node):
            visited.add(node)
            print(node)
            for neighbor in self.graph.neighbors(node):
                if neighbor not in visited:
                    dfs_util(neighbor)

        dfs_util(start_node)

    def bfs_traversal(self, start_node=None):
        """
        Perform breadth-first search traversal of the user journey graph.
        
        :param start_node: The starting node for the traversal. If None, uses the start_url.
        """
        if start_node is None:
            start_node = self.start_url

        visited = set()
        queue = [start_node]

        while queue:
            node = queue.pop(0)
            if node not in visited:
                print(node)
                visited.add(node)
                for neighbor in self.graph.neighbors(node):
                    if neighbor not in visited:
                        queue.append(neighbor)

    def find_paths_dfs(self, start_node):
        """
        Find all possible paths from the start node to leaf nodes using depth-first search (DFS).

        :param start_node: The start node from which to begin the DFS.
        :return: A list of all possible paths.
        """
        def dfs_util(node, path, paths):
            path.append(node)
            if self.graph.out_degree(node) == 0:  # Leaf node
                paths.append(list(path))
            else:
                for neighbor in self.graph.successors(node):
                    dfs_util(neighbor, path, paths)
            path.pop()

        paths = []
        dfs_util(start_node, [], paths)
        return paths

# Example usage:
if __name__ == "__main__":
    start_url = "https://example.com/home"
    user_journey = UserJourneyGraph(start_url)

    # Adding interactions
    user_journey.add_interaction("https://example.com/home", "https://example.com/about", "click")
    user_journey.add_interaction("https://example.com/about", "https://example.com/contact", "click")
    user_journey.add_interaction("https://example.com/home", "https://example.com/products", "click")
    user_journey.add_interaction("https://example.com/products", "https://example.com/product-details", "click")
    user_journey.add_interaction("https://example.com/product-details", "https://example.com/add-to-cart", "click")
    user_journey.add_interaction("https://example.com/add-to-cart", "https://example.com/checkout", "click")

    
    
        # Depth-first search traversal
    print("Depth-first search traversal:")
    user_journey.dfs_traversal()

    # Breadth-first search traversal
    print("\nBreadth-first search traversal:")
    user_journey.bfs_traversal()
    
    # Find all possible paths using DFS
    paths = user_journey.find_paths_dfs(start_url)
    print("All possible paths from root node to leaf nodes:")
    for path in paths:
        print(path)
        
    
    # Visualizing the graph
    user_journey.visualize_graph()
