# Linear Data Structures
'''
Algorithms:
    An algorithm is a set of unambiguous instructions for solving a problem or carrying out a task.
    Algorithms have two key characteristics:
        They cannot continue indefinitely. They must finish in a finite number of steps.
        Each step must be precise and unambiguous.
    
    Efficiency:
        Algorithm efficiency can be measured in terms of how long they take to run and how much space they require in memory to complete the task.
        it gives you an idea of how well it will perform as the input size grows.
        As the process grows in size and complexity, if the algorithm is not efficient enough to handle it, 
        you might end up with a very slow computer program that may even crash the entire system.

    Big O Notation:
        Big O notation describes the worst-case performance, or growth rate, of an algorithm as the input size increases.
        Growth Rate:
            The growth rate of an algorithm refers to how the resources it requires increase as the input size grows.

        NOTE: Memory Space: can also be applied to the context of space requirements.

        In Big O notation, we usually denote input size with the letter n. 
        For example, if the input is a list, n would denote the number of elements in that list.

        O(1): Constant Time Complexity
            When an algorithm has constant time complexity, it takes the same amount of time to run, regardless of input size.
            For example, checking if a number is even or odd will always take the same amount of time, regardless of the number itself.

            NOTE: always require a constant amount of memory space, even as the input gets larger.
        
        O(log n): Logarithmic Time Complexity
            This means that the time required by the algorithm increases slowly as the input size grows.
            For example, a popular search algorithm called Binary Search has O(log n) worst-case time complexity. 
            This is because it eliminates half of the remaining elements in each comparison, which makes it more efficient overall.
        
        O(n): Linear Time Complexity
            The running time of algorithms with this time complexity increases proportionally to the input size.
            For example, a for loop that iterates over all the elements of a list will perform more iterations as the number of list elements increases. 
            If the list is doubled in size, the number of operations will approximately double as well.

            NOTE: space increases proportionally as the input size grows.
                An example of this would be an algorithm that creates and stores a copy of a list of length n.

        O(n log n): Linear-Log Time Complexity
            This is a common time complexity of efficient sorting algorithms, like Merge Sort and Quick Sort.

        O(n^2): Quadratic Time Complexity
            The running time of these algorithms increases quadratically relative to the input size, which is generally not efficient for real-world problems.
            For example, one single nested loop. The inner loop will perform n iterations for each of the n iterations of outer loop.
            Resulting in n^2 iterations. 

            NOTE: space increase quadratically as the input size grows.
                An example of this would be creating a 2D matrix, where the dimensions are determined by the input size, storing all possible pairs.
        
        O(2^n) / O(n!): Exponential Time Complexity / Factorial Time Complexity
            Both are inefficient for real world scenarios
    
    Algorithms are the building-blocks of computer programs, while Big O notation is a powerful framework for analyzing how efficient they are, 
    based on how their time and space requirements in the worst-case scenario scale as the input size grows.

    Pseudocode:
        Pseudocode is a high-level description of the algorithm's logic that is general in nature, and is not based on any specific programming language.
    Edge Cases:
        An edge case is a valid input that sits at the "edges" or boundaries of what your program should handle.

Arrays:
    Arrays are a fundamental data structure in computer science. 
    All arrays store ordered collections of data, but depending on their type, they may work differently behind the scenes.

    Static Arrays:
        Static arrays have fixed sizes. They store elements in adjacent memory locations. 
        The size of a static array is determined when the array is initialized
        Once that specific block of memory is allocated, it's fixed, and cannot be changed while the program is running. 
        This is a key characteristic of static arrays.

        Thanks to this, accessing the values of a static array takes constant time O(1), which is very efficient.
    
    Dynamic Arrays:
        Dynamic arrays are more flexible because they can grow or shrink automatically while the program is running.
        They work through an automatic resizing mechanism that copies the elements into a new array when the original array is full
        The process is done efficiently because the size of the new array is chosen in an efficient way 
        that makes these computationally expensive operations less frequent.

        Accessing the elements of a dynamic array takes constant time O(1), so this operation is very efficient.
        Inserting an element in the middle of the array takes linear time O(n) because the elements after it need to be relocated.
        Inserting an element at the end of the array takes constant time O(1) if there is still space available in the dynamic array, 
        but if the array is full and needs resizing, this operation has a O(n) complexity.

        Python's built-in list data structure works as a dynamic array. 
    
    In general, you should use static arrays when you know the number of elements in advance and you need to access them frequently, 
    and use dynamic arrays when the number of elements is unknown or variable over time.
    You should always consider the tradeoff between the simplicity of static arrays and the flexibility of dynamic arrays. 
    They are both helpful for specific use cases and scenarios

Stacks and queues are data structures used in computer science for organizing and managing elements. 
Understanding them is essential for building efficient algorithms in various programming applications.

Stacks:
    Last in, First out (LIFO)
    This means that the last element that was added to the stack is the first one to be removed.
    Stacks have two ends: top and bottom.
    Elements are added and removed from the top of the stack.

    NOTE: Push - Adding an element to a stack is known as a "push" operation. 
                 We say that we "push" an element onto the stack when we add it to the top of the stack.

    NOTE: Pop - Removing an element from a stack is known as a "pop" operation. 
                 We say that we "pop" an element from the stack when we remove it from the top of the stack.

    Time Complexity of Push and Pop is O(1), Space Complexity of Push and Pop is O(1)

Queues:
    First in, First Out (FIFO)
    This means that the first element added to the queue is the first one to be removed.
    Queues have two ends: front and back.
    Elements are added to the back of the queue and they are removed from the front of the queue.

    NOTE: Enqueue - Adding an element to the back of a queue is known as an "enqueue" operation. 
                    In an enqueue operation, the new element is added to the end of the queue, becoming the end of the line.
    
    NOTE: Dequeue - Removing an element from the front of the queue is known as a "dequeue" operation.
                    In the dequeue operation, the element at the front of the queue is removed, and the next element in line becomes the new front.
    
    Time Complexity of enqueue and dequeue is O(1), Space complexity of enqueue and dequeue is O(1)

Linked Lists:
    A linked list is a linear data structure in which each node is connected to the next node in the sequence.
    Linked lists are commonly used for implementing other data structures, such as stacks, queues, and deques.

    Singly Linked Lists:
        A singly linked list is a type of linked list in which each node is connected to the next node in the sequence.
        This single reference per node allows you to traverse the linked list in one direction, from start to end.
        The search can only move forward, not backward. 
        NOTE: Tail node - The tail node is the last node. It's used to determine when the process has reached the end of the linked list.

        Inserting Nodes:
            One of the great things about linked lists is that they do not have a fixed size. 
            They can be expanded or shrunk as needed by simply updating the connections between the nodes.
            Node can be inserted at the start, the middle or the end.
            
            Inserting a node at the beginning of the linked list has a constant time complexity O(1) 
            because it only requires updating the reference to the head node and the connection between the new head node and the next node in the sequence.
            
            To insert a node at the end of the linked list, first you need to reach the end and then add a connection to the new node to make it the new tail node.
            This operation has linear time complexity, O(n), where n is the number of nodes stored in the linked list, 
            because first you need to reach the end of the linked list to make the insertion and this would require going from one node to the next and so on until the end is reached.

        Removing Nodes:
            Just as you can insert nodes, you can also remove them from the start, middle, and end of the linked list.

            To remove a node from the start, you need to update the reference to the head node, which should be the next node in the sequence.
            This operation has a constant time complexity O(1), because it only requires updating the linked list's reference to the head node.

            To remove a node from the middle of the linked list, you need to update the reference of the previous node to connect it to the next node 
            in the sequence

            To remove a node from the end of the linked list, you need to remove the connection of the previous node and make this node the new tail node. 
            Now the linked list will end at the new tail node.
            This operation has a linear time complexity O(n), because first you have to reach the end of the linked list.
    
    Doubly Linked Lists:
        In a doubly linked list, each node stores two references: a reference to the next node and a reference to the previous node in the sequence.
        This means that doubly linked lists can be traversed in both directions.
        However, doubly linked lists do require more memory than singly linked lists because each node stores two references instead of one.
        
        The insertion and deletion operations work exactly the same. The only difference is that now you will need to update two references per node 
        and keep track of the reference to the tail node to insert elements at the end of the doubly linked list very efficiently 
        and start the traversal process from the back, if necessary.

Maps, Hash Maps and Sets:
    Abstract Data Type (ADT):       #Abstraction from OOP but for data structures
        An Abstract Data Type (ADT) is a conceptual representation of a data type, 
        including what operations can be performed on the data and the properties of that data.
        Abstract Data Types are like blueprints that describe what operations can be performed, not how they are performed. 
        They separate the interface from the actual implementation of the operations.
    
    Map:
        A map is an ADT that manages collections of key-value pairs and their operations in a very specific and efficient way.
        The map Abstract Data Type also defines important operations, such as inserting key-value pairs, getting the value associated with a key, 
        updating the value associated with a key, removing a key-value pair, and checking if a key exists in the map.
        It doesn't actually specify how these operations should be performed, it just lists them as part of the available operations of the data type

    Hash Map (Hash Tables):
        concrete implementation of the map Abstract Data Type.
        Hash maps use a technique called "hashing" to perform common operations very efficiently.
        Hashing essentially works by generating a hash value for each element using a hash function.

        The hash value is generated based on the key of the key-value pair and it's used to calculate an index in an underlying array, 
        the actual data structure where the key-value pairs are stored.

        NOTE:
        Basically, suppose you have 5 slots and 1000 students
        there is no way for each to student to have a different slot, all 1000 students will fit in 5 slots
        so each slot will have 200 students
        so all those 200 students share the same assigned slot: 1 - 200, 2 - 200, 3 - 200, 4 - 200, 5 - 200
        This is called "Collision"

        Pigeonhole Principle:
            The pigeonhole principle is a fundamental mathematical concept: if you put n items (pigeons) into m containers (pigeonholes) and n > m, 
            at least one container must contain more than one item. It is often used to prove the unavoidable overlap or collision of items in a restricted space.

            Eg: If there are 13 people in a room, at least two of them share a birth month.
            Eg: In computer science, it guarantees that if you have more unique data items than you have available buckets in a hash table, 
                collisions will occur
            Eg: Combinatorics:  It is widely used in competitive mathematics and probability to deduce properties within large datasets, 
                such as finding integers with identical remainders

        To solve Collisions:
            Chaining Strategy:
                each array index points to a linked list (another data structure), where all the elements with the same index are stored.
            Open Addressing:
                which involves searching for the next available index in the array based on a predefined search sequence.
        
        Average Case Time Complexity is O(1) for inserting, retrieving and deleting key-value pairs
        Worst Case Time Complexity is O(n), which happens when there are many hash collisions, so collion resolution strategy has to be implemented many times

        Average Case Space Complexity is O(1) 
        Worst Case Space Complexity is O(n) due to resizing operations of underlying array. 

        This turns the hash table into something similar to a linear data structure where n elements have to be scanned to find the target key. 
        However, this is relatively rare if the hash map is implemented properly.  
    
    Sets:
        Sets are unordered collection of unique elements. 
        Cannot be accessed using indices
        Sets contain unique values; if you try to add a value twice, only one copy will be kept
        Analogus to mathematical sets 
        One of the main advatange is that they guarentee uniqueness 
        They are dynamic. 

        Average Case Time Complexity is O(1) for adding, removing, getting the length, to check if element is in set 
        Sets are implemented as Hash Tables 
        Worst Case Time Complexity is O(n), when multiple hash collisions are present 

        Average Case Space Complexity is O(1) 
        Worst Case Space Complexity is O(n) - resizing operations, etc. 

        variable = set() / {a, b, c, d, ...} 
        variable.add(key)
        variable.remove(key) # Displays KeyError is key is not present
        variable.discard(key) # same thing as .remove(key) but does not throw error
        variable.pop() # returns arbitrary element from the set 
        variable.clear() # removes all elements from the set 
        
        set_a.union(set_b)                  set_a | set_b
        set_a.intersection(set_b)           set_a & set_b
        set_a.symmetric_difference(set_b)   set_a ^ set_b
        set_a.difference(set_b)             set_a - set_b 

        set_a.issubset(set_b)
        set_a.issuperset(set_b)
'''

'''
Array:
    "I need to access the 500th element instantly."
    Tradeoff:
        Fast indexing.
        Slow insertions in the middle.

Linked List:
    "I'm constantly inserting and deleting elements."
    Tradeoff:
        Fast insertion (once you're at the location).
        Slow searching.
        No random access.

Stack:
    "I only ever care about the most recent thing."
    Examples:
        Undo button.
        Browser history.
        Function calls.
        DFS. (Depth First Search)

Queue:
    "Things must be processed in arrival order."
    Examples:
        Print queue.
        Network packets.
        Task scheduling.
        BFS. (Breadth First Search) 

Hash maps:
    "I need to find information by key almost instantly."

Sets:
    "I only care whether something exists"
'''
