#================================================================================================================================================================
#                                                                         Graphs and Trees
#================================================================================================================================================================
'''
Graphs:
    Graphs are data structures used to represent the connections or relationships between objects or entities. They're often used to model networks.
    The types of networks that you can model with a graph include social networks, 
    transportation networks, communications networks, and even recommendation systems.

    A graph is often represented as a collection of points or circles connected by lines.
    These circles and lines represent the two main components of a graph: nodes and edges.

    NOTE: Nodes, also known as vertices, represent the objects or entities that are part of the network modeled by the graph. 
    They could be users, products, stations, cities, or any other entities in the model.

    NOTE: Edges are the connections between the nodes. If two nodes are connected by an edge, that means that they're somehow connected in the network.

    Undirected Graphs:
        Undirected graphs are graphs where the edges don't have a specific direction. This type of edge is 
        usually represented with a straight line between the nodes.
        This means that, if there's an edge connecting nodes A and B, the connection works in both directions: from node A to node B and from node B to node A.

    Directed Graphs:
        In contrast, directed graphs are graphs where the edges do have a specific direction.
        If there is a connection from node A to node B, that doesn't necessarily imply that there is a connection from node B to node A.

    Vertex Labeled Graphs:
        A vertex labeled graph is a graph in which each node is associated with a label or identifier in addition to its data. 
        These labels are used to identify the nodes, represent them visually, and store additional information about them.

    Cyclic Graphs:
        Cyclic graphs are directed graphs with at least one cycle.
        A cycle is a path that you can follow through the edges of a graph that will take you back to the initial node where you started.

    Edge Labeled Graphs:
        In edge labeled graphs, edges are associated with labels. These labels are usually drawn next to their corresponding edges.

        Weighted Graphs:
            Weighted graphs are a specific type of edge labeled graph in which the labels on the edges represent values 
            that can be compared and used to perform arithmetic operations.

            This is an example of a weighted graph. We write each weight next to its corresponding edge. 
            The "cost" of going from node B to node D is 3, and since this is an undirected graph, that's the same cost of going from node D back to node B.

    Directed Acyclic Graphs:
        Another very common type of graph in computer science is the directed acyclic graph, which is a directed graph with no cycles.
        It's acyclic because it doesn't have any cycles. Why? Notice that, if you start at a specific node, you cannot go back to it 
        because of the direction of the edges.

    Disconnected Graphs:
        A disconnected graph is a graph with two or more groups of nodes that are not connected by any edges.

First Searches:
    Traversing:
        This process is known as "traversing" the data structure.
        Traversals are used to do something with every single node in the data structure, 
        like printing their values, finding a specific value, or performing certain operations on the nodes.
        By systematically visiting each node, you make sure that the process won't skip any nodes.
    
    Without a clear way to traverse the data structure, going through it would be like walking through a maze without a specific path to follow.

    That's where algorithms like NOTE: {breadth-first search (BFS)} and NOTE: {depth-first search (DFS)} become really important. 
    They are commonly used to traverse graphs and for finding a path between two nodes.

    NOTE: Breadth-First Search (BFS):
        Breadth-first search (BFS) is an algorithm that visits all neighboring nodes before moving to the next level in the graph.
        It can be used to find the shortest path between two nodes in an unweighted graph because it analyzes all the nodes at each level, 
        so it finds the path with fewest edges first.
        This algorithm is commonly implemented using a queue data structure to keep track of the nodes that have been visited. 
        Queues follow the FIFO (first in, first out) method, where the first node that was added to the queue is the first one to be removed.

        The algorithm works like this:

        - You start at a specific node.
        - That node is marked as visited and added to the queue.
        - While the queue is not empty, the current node is removed from the queue (dequeued). 
          Then, for each one of its neighbors, if the neighbor has not been visited, it is marked as visited and added to the queue.

        One important consideration is that, since breadth-first search (BFS) requires storing a queue in memory, and this queue may have a large number of nodes,
        the space requirements of this algorithm can be considerable. This is especially true for graphs with a large number of nodes on the same level.

    NOTE: Depth-First Search (DFS):
        While breadth-first search (BFS) first visits all the neighboring nodes at the same level, 
        depth-first search (DFS) follows each branch as deep as possible before it backtracks.
        Depth-first search (DFS) is commonly used to solve puzzles with a single solution, detecting cycles in a graph, and finding connected graph components.
        This algorithm can be implemented using recursion or a stack data structure to keep track of the visited nodes.
        Stacks follow the LIFO (last in, first out) method, where the last node that was added to the stack is the first one to be removed from the stack.

        The algorithm works like this:

        - Start at a specific node.
        - That node is marked as visited and added to the stack.
        - While the stack is not empty, the current node is popped (removed). This is when we "visit" or process it 
          (for example, by printing its value). Then, all of its unvisited neighbors are marked as visited and added to the stack.

Adjacent Matrices and Adjacent Lists:
    Graphs are very powerful data structures made by a set of nodes, also known as vertices, and edges that connect them.
    There are two common ways to implement graphs in your code:
        Adjacency matrices
        Adjacency lists
    
    NOTE: Adjacent Matrices:
        An adjacency matrix is a two-dimensional list in which the rows and columns represent the graph's vertices.
        For example, if you have a matrix stored in a variable named matrix, the value stored at matrix[i][j], where i is the row and j is the column, 
        represents the edge or connection between node i and node j.
        The values may have different meanings depending on whether the graph is weighted or unweighted:
            If the graph is unweighted, a value of 1 means that there is an edge connecting these nodes, while a value of 0 means there is no edge between them.
            If the graph is weighted, the value would represent the weight of the edge that connects the nodes.
        One of the great advantages of using an adjacency matrix is that checking if there is an edge between two nodes takes constant time O(1)

        However, this efficiency in finding the edges comes with a tradeoff. Adjacency matrices have a large quadratic space requirement O(V²), 
        where V is the number of nodes in the graph.
        This is inefficient for sparse graphs, which are graphs that only have a few edges. 
        if the graph is sparse, you will be storing many 0s in the matrix to represent the lack of edges between the nodes, 
        and these 0s will still take space in memory.
        Adjacency matrices are also inefficient for finding a node's neighbors because the program has to iterate over the entire row or column 
        to find the 0s and 1s that represent the edges. In the worst case, this process can take O(V) time, where V is the number of nodes in the graph.

    NOTE: Adjacent Lists:
        An adjacency list is an array or dictionary that stores all the neighbors of each node.
        There are two ways to implement adjacency lists:
            As an array, where each index represents a node and the list stored at that index contains its neighbors.
            As a dictionary, where each key represents a node and the value associated to that key (a list) contains its neighbors.
        Adjacency lists are more efficient than adjacency matrices in terms of space requirements. They have a O(V + E) space complexity, 
        where V is the number of vertices (nodes) and E is the number of edges.
        It's also efficient for finding all neighbor nodes, since this operation only requires accessing the list associated to the node.

        Adjacency lists are less efficient than adjacency matrices for determining if there is an edge between two nodes.
        The search process can take O(V) time in the worst-case, since it may have to search through a very long list of neighbors 
        if the node is connected to all the other nodes in the graph.

Trees and Tries:
    NOTE Trees:
    A tree is a specific type of graph.
    For a graph to be classified as a tree, it must:
        Have no loops or cycles (paths where the start and end nodes are the same).
        Be connected (every node can be reached from every other node).
    Trees are non-linear data structures that organize nodes in a hierarchy, where nodes may have children, siblings, and parent nodes.
    his is the node where you will start traversing the entire data structure, usually with algorithms like breadth-first search (BFS) or depth-first search (DFS).

    Tree nodes have three important properties
        Depth: the length of the path from the root to that node.
        Height: the length of the path from that node down to a leaf. 
        Degree: the number of child nodes each node has. 
    
    There are many different types of trees, including Binary Trees, Binary Search Trees, AVL trees, Red-Black Trees, and B-Trees.

    Binary Tree and Binary Search Tree:
        A binary tree is a type of tree in which each node can have at most two child nodes, a left child node and a right child node

        A binary search tree is a more specific version of a binary tree, with a very particular ordering property.
        To understand it, first you need to understand subtrees. A subtree is a section of a tree that is a tree itself.
        A Binary Search Tree (BST) is a binary tree data structure in which each node maintains an ordering property: 
        all values stored in the left subtree of a node are less than the node's value, and 
        all values stored in the right subtree of that node are greater than the node's value. This property must hold recursively for every node in the tree.

    NOTE Tries:
    Tries are tree data structures used to store a set of strings.
    The root node does not represent any particular character, so you can think of it as representing an empty string.

    Eg: Tea, Top, Ten 
    T - [o, e] 
        o - [p]
        e - [a, n]
    The worst-case time complexity for the search operation is O(L), where L is the length of the string that you are looking for.
    The great advantage of this data structure is that when multiple strings share the same prefix, their paths overlap, so the prefix itself is only stored once.
    This efficiency makes tries perfect for implementing features like autocomplete and spell checkers.

    They can be inefficient if the set of strings has many unique characters. This would require storing many unique characters as individual nodes. 
    These nodes would have to be traversed to find the words, which would not be optimal.

Priority Queues and Heaps:
    NOTE: Priority Queue
    A priority queue is an abstract data type (ADT) that works similarly to a queue or stack, but with one key difference.
    Queues follow FIFO and Stacks follow LIFO, queues and stacks only consider the order of insertion of the elemnets
    However, priority queues take the "priority" of the elements into account. Element with highest priority is removed first, but some implementations may prefer
    removing the lowest priority first
    Priority queues are very helpful for practical applications like finding the shortest path between two locations, scheduling tasks in operating systems, 
    simulating traffic, compressing data, and managing networks.

    NOTE: Heaps
    A heap is a tree data structure with a very specific property called the heap property. This property determines the relationship between each node 
    and its children, based on the type of heap.
    There are two primary types of heaps:
        Max-heap
        Min-heap
    In a max-heap, the value of each node is greater than or equal to the value of its children.
    In contrast, in a min-heap, the value of each node is less than or equal to the value of its children.
'''

import heapq
def list_functions(module):
    for name in dir(module):
        obj = getattr(module, name)
        if callable(obj) and not name.startswith("_"):
            print(name)
#list_functions(heapq)
'''
import heapq
    heapify         -> if you already have a data structure and want to turn it into a heap
    heappop         -> to remove an element of higher priority first heapq.heappop(heap_list)
    heappush        -> to add an element heapq.heappus(heap_list, value)
    heappushpop     -> combines both push and pop into one heapq.heappushpop(heap_list, value_to_be_added) returns highest priority element
    heapreplace
    merge
    nlargest
    nsmallest

    in the heap_list, left to right is highest priority to least priority

    The average and worst case time complexities for inserting and extracting the minimum or maximum value from a heap 
    (depending on the type of heap) are logarithmic, O(log n), because the number of swaps required is usually proportional 
    to the height of the heap, which is log(n).
    The average and worst case time complexity for the "peek" operation is constant time, O(1). Peeking involves getting 
    the minimum or maximum value (depending on the type of heap) without removing it.
    The "heapify" operation, where the heap is built from an unsorted list, has linear time complexity, O(n), in the average and worst cases.
    Similarly, both searching for and deleting an arbitrary element have linear average and worst case time complexities of O(n), 
    since they potentially require traversing the entire heap.

    The space complexity of the heap is linear, O(n), where n is the number of elements it contains.
'''
