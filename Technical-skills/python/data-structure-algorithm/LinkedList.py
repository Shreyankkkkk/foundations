'''
Data Structure:
    Linked Lists:
'''

class LinkedList:

    class Node:
        # Represents a single node in the linked list.
        def __init__(self, data):
            self.data = data
            self.next = None

    # ==========================
    # Constructor
    # ==========================

    def __init__(self):
        # Initialize an empty linked list.
        self.head = None
        self.tail = None
        self.length = 0

    # ==========================
    # String Representation
    # ==========================

    def __str__(self):
        # Return a readable representation of the linked list.
        temp = self.head
        return_string = f"Total Nodes: {self.length}\n"

        while temp:
            return_string += str(temp.data) + " -> "
            temp = temp.next

        return_string += "None"
        return return_string

    # ==========================
    # Basic Information
    # ==========================

    def is_empty(self):
        # Return True if the linked list contains no nodes.
        return self.length == 0

    def size(self):
        # Return the total number of nodes.
        return self.length

    # ==========================
    # Searching
    # ==========================

    def search(self, value):
        # Return True if the given value exists in the linked list.
        current_data = self.head

        while current_data:
            if current_data.data == value:
                print(f"Node Value = {value}, found!")
                return True

            current_data = current_data.next

        print(f"Node Value = {value}, not found")
        return False

    def get(self, index):
        # Take an index and return the value stored at that index.
        if index < 0 or index >= self.length:
            return None

        current_data = self.head

        for _ in range(index):
            current_data = current_data.next

        return current_data.data

    def index(self, value):
        # Take a value and return the index of its first occurrence.
        current_data = self.head
        current_index = 0

        while current_data:
            if current_data.data == value:
                return current_index

            current_data = current_data.next
            current_index += 1

        return -1

    # ==========================
    # Insertion
    # ==========================

    def add(self, data):
        # Append a new node to the end of the linked list.
        node = self.Node(data)

        if self.head is None:
            self.head = self.tail = node
            self.length += 1
        else:
            self.tail.next = node
            self.tail = node
            self.length += 1

    def prepend(self, data):
        # Insert a new node at the beginning of the linked list.
        if self.head is None:
            self.add(data)
            return

        node = self.Node(data)
        node.next = self.head
        self.head = node
        self.length += 1
        return

    # ==========================
    # Removal
    # ==========================

    def remove(self, data):
        # Remove the first node containing the given value.
        if self.is_empty():
            return f"The List is Empty"

        if self.head.data == data:
            self.head = self.head.next
            self.length -= 1

            if self.head is None:
                self.tail = None
                return f"The List is Empty after removing : Node = {data}"

            return f"The Node {data} has been removed."

        previous_data = self.head
        current_data = self.head.next

        while current_data:
            if current_data.data == data:
                # Skip over the node being removed.
                previous_data.next = current_data.next

                # Update the tail if the removed node was the last node.
                if current_data == self.tail:
                    self.tail = previous_data

                self.length -= 1
                return f"The Node {data} has been removed."

            previous_data = current_data
            current_data = current_data.next

        return f"The Node Value = {data}, not found!"

    def pop(self):
        # Remove the last node (tail).
        if self.is_empty():
            return "The list is empty"

        return self.remove(self.tail.data)

    def pop_first(self):
        # Remove the first node (head).
        if self.is_empty():
            return "The list is empty"

        return self.remove(self.head.data)

    def clear(self):
        # Remove every node from the linked list.
        while self.length != 0:
            self.remove(self.head.data)

        return "The linked list is empty"

    # ==========================
    # Utility
    # ==========================

    def reverse(self):
        # Reverse the linked list in-place.
        if self.size() == 0:
            return f"The LinkedList is empty"

        previous_node = self.head
        current_node = previous_node.next
        previous_node.next = None

        self.tail = self.head

        while current_node:
            next_node = current_node.next
            current_node.next = previous_node

            previous_node = current_node
            current_node = next_node

        self.head = previous_node

if __name__ == '__main__':
    linkedlist = LinkedList()
    linkedlist.add(25)
    '''
    linkedlist = LinkedList()
    linkedlist.add(25)

    Background:
    linkedlist.head = None
    linkedlist.tail = None
    linkedlsit.length = 0
    data = 25
    linkedlist.node.data = 25 #line 336
    linkedlist.node.next = None #line 336
    if linkedlist.head is None -> True
    linkedlist.head = node <__main__.linkedlist.node object>
    linkedlist.tail = node <__main__.linkedlist.node object>
    linkedlist.lenght = 1
    '''
    linkedlist.add(50)
    '''
    linkedlist.add(50)

    Background:
    linkedlist.head = node <__main__.linkedlist.node object 1> (25, None)
    linkedlist.tail = node <__main__.linkedlist.node object 1> (25, None)
    linkedlist.node.data = 50 #line 336
    linkedlist.node.next = None #line 336
    if linkedlist.head is None -> False 
    else block:
    linkedlist.tail.next = <__main__.linedlist.node object 2> (50, None)
    linkedlist.tail = node <__main__.linkedlist.node object 2> (50, None)
        before the current tail (before connecting to the new node), self.tail.next = node, changes the next reference of the self.tail to the new object
        and then im changing the tail to the new object where the self.tail.next points to none. First make the arrow point to the new node
        and then make the tail, the new node
    linkedlist.length = 2
    '''
    linkedlist.add(75)
    '''
    linkedlist.add(75)

    Background:
    linkedlist.head = node <__main__.linkedlist.node object 1> (25, object 2)
    linkedlist.tail = node <__main__.linkedlist.node object 2> (25, None)
    linkedlist.node.data = 75 #line 336
    linkedlist.node.next = None #line 336
    if linkedlist.head is None -> False 
    else block:
    linkedlist.tail.next = <__main__.linedlist.node object 3> (50, None)
    linkedlist.tail = node <__main__.linkedlist.node object 3> (50, None)
    linkedlist.length = 3
    '''
    linkedlist.add(100)
    '''
    linkedlist.add(100)

    Background:
    linkedlist.head = node <__main__.linkedlist.node object 1> (25, object 2)
    linkedlist.tail = node <__main__.linkedlist.node object 3> (50, None)
    linkedlist.node.data = 100 #line 336
    linkedlist.node.next = None #line 336
    if linkedlist.head is None -> False 
    else block:
    linkedlist.tail.next = <__main__.linedlist.node object 4> (75, None)
    linkedlist.tail = node <__main__.linkedlist.node object 4> (75, None)
    linkedlist.length = 4
    '''
    #print(linkedlist)
    '''
    print statement --> goes to __str__ block
    temp = self.head (Create a temporary head copy because if not done, self.head value will change from object 1 to object 4 and we will lose reference to head)
    return_string = total nodes: 4\n 
    while temp: #until there is object, run the loop. temp value will go from object 1 -> object 2 -> object 3 -> object 4
    first iteration
    return_string = total nodes:\n25 -> 
        temp.data means object_1.data and that is 25
    temp = temp.next (temp is a copy of head, head is a node object, next works, and changes reference from object 1 to object 2)
    second iteration
    return_string = total nodes:\n25 -> 50 ->
        temp.data means object_2.data and that is 50
    temp = temp.next (temp is a copy of head, head is a node object, next works, and changes reference from object 2 to object 3)
    third iteration
    return_string = total nodes:\n25 -> 50 -> 75 -> 
        temp.data means object_3.data and that is 75
    temp = temp.next (temp is a copy of head, head is a node object, next works, and changes reference from object 3 to object 4)
    fourth iteration
    return_string = total nodes:\n25 -> 50 -> 75 -> 100 -> 
        temp.data means object_4.data and that is 100
    temp = temp.next (temp is a copy of head, head is a node object, next works, and changes reference from object 4 to None)

    return_string = total nodes:\n25 -> 50 -> 75 -> 100 -> None
    return return_string
    '''
    #print("Header : ", linkedlist.head.data)
    '''
    Header being a node object, .data works and it prints the value cause node.data refers to the number or wtv that was added and gets printed
    '''
    #print("Tail : ", linkedlist.tail.data)
    '''
    tail being a node object, .data works and it prints the value cause node.data refers to the number or wtv that was added and gets printed
    '''
    #print(linkedlist.remove(0))
    '''
    goes inside the remove method 
    linkedlist is (25, object2) (50, object3) (75, object4) (100, none), therefore it is not None
    self.head is (25, object2), 0 is not equal to 25, so therefore that if statement gets skipped 
    previous_data = object1 i.e, (25, object2)
    current_data = object2 i.e, (50, object3)

    now it loops through all the objects starting from current_data
    first iteration
    current_data.data = 50, that is not equal to 0
    so current_data gets updated to (75, object4) and previous_data gets updated to (50, object3)
    second iteration
    then current_data.data = 75, not equal to 0
    so current_data gets updated to (100, None) and previous_data gets updated to (75, object4)
    third iteration
    then current_data.data = 100, not equal to 0
    so current_data gets updated to object5 (but object 5 is None) so the loop breaks 

    returns "Node 0 not found"
    '''
    linkedlist.remove(100)
    '''
    goes inside the remove method
    goes inside the remove method 
    linkedlist is (25, object2) (50, object3) (75, object4) (100, none), therefore it is not None
    self.head is (25, object2), 0 is not equal to 25, so therefore that if statement gets skipped 
    previous_data = object1 i.e, (25, object2)
    current_data = object2 i.e, (50, object3)

    now it loops through all the objects starting from current_data
    first iteration
    current_Data.data = 50, not equal to 100
    current_Data.data gets updated to (75, object4) and previous_Data gets updated to (50, object3)
    second iteration
    current_Data.data = 75, not equal to 100
    current_Data.data gets updated to (100, object) and previous_data gets updated to (75, object4)
    third iteration
    current_Data.data = 100, which is equal to 100
    goes inside the if statement 
    now we are changing previous_data.next to current_data.next (i.e, object4 to object5, which is None in this case)
    basically changing (75, object4) to (75, None)
    now we check if its tail or not 
    since current_data is (100, None) and tail is (100, None), they are equal
    so now we have to update tail to the previous node: self.tail = previous_node (self.tail = object(75, None))
    and then we subtract 1 from the overall length
    and then we break the loop with return statement printing "Node 100 has been removed"
    '''
    #==============================================================
    # Test Code 
    #-=============================================================
    linkedlist.clear()

    print("Is the linkedlist empty?", linkedlist.is_empty())
    print("Size: ", linkedlist.size())
    for value in range(0, 325, 25):
        linkedlist.add(value)

    print(linkedlist)
    print("Header : ", linkedlist.head.data if linkedlist.head else None)
    print("Tail : ", linkedlist.tail.data if linkedlist.tail else None)
    print()

    print("Is the linkedlist empty?", linkedlist.is_empty())
    print("Size: ", linkedlist.size())
    print()

    print("Index 3: ", linkedlist.get(3))
    print()

    print("Value 75: ", linkedlist.index(75))
    print()

    print(linkedlist.remove(225))
    print(linkedlist)
    print("Header : ", linkedlist.head.data if linkedlist.head else None)
    print("Tail : ", linkedlist.tail.data if linkedlist.tail else None)
    print()

    print(linkedlist.remove(1))
    print(linkedlist)
    print("Header : ", linkedlist.head.data if linkedlist.head else None)
    print("Tail : ", linkedlist.tail.data if linkedlist.tail else None)
    print()

    print(linkedlist.pop())
    print(linkedlist)

    print("Header : ", linkedlist.head.data if linkedlist.head else None)
    print("Tail : ", linkedlist.tail.data if linkedlist.tail else None)
    print()

    print(linkedlist.pop_first())
    print(linkedlist)

    print("Header : ", linkedlist.head.data if linkedlist.head else None)
    print("Tail : ", linkedlist.tail.data if linkedlist.tail else None)
    print()

    print("Header : ", linkedlist.head.data if linkedlist.head else None)
    print("Tail : ", linkedlist.tail.data if linkedlist.tail else None)
    print()

    linkedlist.reverse()
    print(linkedlist)
    print()

    linkedlist.prepend(-20)
    print(linkedlist)
    print()

    print(linkedlist.clear())
    print("Is the linkedlist empty?", linkedlist.is_empty())
    print("Size: ", linkedlist.size())
