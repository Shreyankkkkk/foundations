# Python Certification Project 5 - Tower of Hanoi
'''
Implement the Tower of Hanoi Algorithm
In this lab, you will solve the mathematical puzzle known as the Tower of Hanoi. The puzzle consists of three rods and a number of disks of different diameters.

sequence of moves required to solve a 3-disks tower of Hanoi puzzle
The puzzle starts with the disks piled up on the first rod, in decreasing size, with the smallest disk on top and the largest disk on the bottom.

The goal of the Tower of Hanoi puzzle is moving all the disks to the last rod. To do that, you must follow three simple rules:

You can move only top-most disks.
You can move only one disk at a time.
You cannot place larger disks on top of smaller ones.
Objective: Fulfill the user stories below and get all the tests to pass to complete the lab.

User Stories:

You should have a function named hanoi_solver that takes an integer representing the total number of disks of the puzzle as the argument.
The hanoi_solver function should solve the puzzle following the given rules in 2n - 1 moves, where n is the total number of disks.
The hanoi_solver function should return a string with all the moves taken to solve the puzzle, including the starting arrangement, with each move on a new line. Rods should be represented as lists of integers, (the smallest disk is represented by the number 1) with each rod separated by a space. For example, hanoi_solver(3) should return the following:
Example Code
[3, 2, 1] [] []
[3, 2] [] [1]
[3] [2] [1]
[3] [2, 1] []
[] [2, 1] [3]
[1] [2] [3]
[1] [] [3, 2]
[] [] [3, 2, 1]
'''

def disks(number_of_disks, rods = 3):
    numbers_list = []
    return_list = []
    for value in range(number_of_disks, 0, -1):
        numbers_list.insert(len(numbers_list), value)
    return_list.append(numbers_list)
    for _ in range(rods - 1):
        return_list.append([])
    return return_list

def hanoi_solver(number_of_disks: int, rods = 3, start = 0, end = 2, history = None, rods_list = None) -> str:
    if history is None:
        history = []
    if rods_list is None:
        rods_list = disks(number_of_disks, rods)

    def return_format():
        return_string = ''
        for value in rods_list:
            return_string += str(value) + " "
        return return_string.strip()
    
    def move_disks(result_list, start_index, end_index, hist):
        disk = result_list[start_index].pop()
        result_list[end_index].append(disk)
        hist.append(return_format())
    if not history:
        history.append(return_format())

    if number_of_disks == 1:
        move_disks(rods_list, start, end, history)
    else:
        other = 3 - (start + end)
        hanoi_solver(number_of_disks - 1, rods, start, other, history, rods_list)
        move_disks(rods_list, start, end, history)
        hanoi_solver(number_of_disks -1, rods, other, end, history, rods_list)

    return_string = ''
    for value in history:
        return_string += str(value) + '\n'
    return return_string.rstrip('\n')
#print(hanoi_solver(5))

