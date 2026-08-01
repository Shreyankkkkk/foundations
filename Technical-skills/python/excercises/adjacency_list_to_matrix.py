# Project: Build an Adjacency List to Matrix Converter

'''
In this lab, you will build a function that converts an adjacency list representation of a graph into an adjacency matrix. An adjacency list is a dictionary where each key represents a node, and the corresponding value is a list of nodes that the key node is connected to. An adjacency matrix is a 2D array where the entry at position [i][j] is 1 if there's an edge from node i to node j, and 0 otherwise.

For example, given the adjacency list:

Example Code
{
    0: [1, 2],
    1: [2],
    2: [0, 3],
    3: [2]
}
The corresponding adjacency matrix would be:

Example Code
[
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [1, 0, 0, 1],
    [0, 0, 1, 0]
]
Objective: Fulfill the user stories below and get all the tests to pass to complete the lab.

User Stories:

You should define a function named adjacency_list_to_matrix to convert an adjacency list to an adjacency matrix.
The function should take a dictionary representing the adjacency list of an unweighted (either undirected or directed) graph as its argument.
The function should:
Convert the adjacency list to an adjacency matrix.
Print each row in the adjacency matrix.
Return the adjacency matrix.
For example, adjacency_list_to_matrix({0: [2], 1: [2, 3], 2: [0, 1, 3], 3: [1, 2]}) should print:

Example Code
[0, 0, 1, 0]
[0, 0, 1, 1]
[1, 1, 0, 1]
[0, 1, 1, 0]
and return [[0, 0, 1, 0], [0, 0, 1, 1], [1, 1, 0, 1], [0, 1, 1, 0]].
'''

def adjacency_list_to_matrix(adjacent_list: dict) -> list:
    number_of_nodes = len(adjacent_list)
    adjacent_matrix = []
    for key in adjacent_list:
        nodes_connection = adjacent_list[key]
        appending_list = []
        for value in range(number_of_nodes):
            if value in nodes_connection:
                appending_list.append(1)
            else:
                appending_list.append(0)
        adjacent_matrix.append(appending_list)

    printing_string = ''
    for value in adjacent_matrix:
        printing_string += str(value) + "\n"
    print(printing_string)

    return adjacent_matrix

