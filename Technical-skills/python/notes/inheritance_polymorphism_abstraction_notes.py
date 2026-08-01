'''
Inheritance: 
    With inheritance, a subclass (or child class) can use the attributes and methods of a base class (or parent class). 
    This allows you to reuse code, create clear class hierarchies, and customize behavior without rewriting everything.
    You can customize by extending existing methods or overriding them in the child class.

    class Parent:
        # Parent attributes and methods

    class Child(Parent):
        # Child inherits, extends, and/or overrides where necessary
    
    This style is called single inheritance, since a child class inherits from exactly one parent class.

    super():
        "Find the next implementation in the inheritance chain while keeping the same object."
        the method passed, it checks the classes above (parent / grandparent) to run the method.
'''
class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Dog(Animal):
    def __init__(self, name, age, breed):
        super().__init__(name, age)
        self.breed = breed

jack = Dog("Jack", 23, "golden retriever")
#print(jack.name)
#print(jack.age)
#print(jack.breed)

'''
Polymorphism:
    With polymorphism, you have access to an interface where you can interact with many objects of the same kind.
    Polymorphism allows methods in different classes to share the same name but perform different tasks. 
    You call the same method name on different objects, and each responds in its own way.


'''
class Parent:
    def __init__(self):
        self.__data = 'Parent data'

class Child(Parent):
    def __init__(self):
        super().__init__()
        self.__data = 'Child data'
c = Child()

'''
Abstraction:
    Abstraction is the process of hiding complex implementation details and showing only the essential features of an object or system. 
    Think of it as focusing on what something does rather than how it does it.
    Abstraction is not limited to Python. It's a programming concept that can be implemented in many languages that support object-oriented programming.

    As for how Python implements abstraction, it does so through the abc module.
        This module provides the ABC class (standing for “abstract base class”) and the @abstractmethod decorator.
    
'''
'''
import abc # Abstract Base Class (ABC)
import inspect
for name in dir(abc):
    obj = getattr(abc, name)
    if callable(obj) and not name.startswith("_"):
        print(name)
for name in dir(inspect):
    obj = getattr(inspect, name)
    if callable(obj) and not name.startswith("_"):
        #print(name)
        pass
print()
'''
'''
abc module
    ABC (Abstract Class Method)
        an abstract method is a method declared in an Abstract Base Class (ABC) using the @abstractmethod decorator. 
        It may have no implementation or a basic default one. 
        However, any subclass must override it to be considered concrete and instantiable, even if a default implementation is provided.
'''
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Project 4: Build a Player Interface
'''
Objective: Fulfill the user stories below and get all the tests to pass to complete the lab.

User Stories:

You should define an abstract class named Player that inherits from the abc.ABC class.

The Player class should have an __init__ method that sets:

The moves attribute to an empty list.
The position attribute to (0, 0).
The path attribute to a list containing the initial position.
The Player class should have a method named make_move that:

Uses random.choice to get a random move from the moves attribute (defined in the concrete class).
Adds the values from the selected move to the current position and updates the position attribute.
Appends the new position tuple to the path attribute.
Returns the new position.
The Player class should have an abstract method named level_up to be implemented in concrete classes.

You should define a Pawn class that inherits from the Player class.

The Pawn class should use super() to call the parent's __init__ method and then set the moves attribute to a list of tuples representing x, y coordinates.

Each coordinate tuple should represent a movement of 1 unit in the following directions: up, down, left, right.

The Pawn class should implement a concrete level_up method by adding more moves to the moves attribute. The added moves should represent the four diagonal movements (for example, 1 unit down plus 1 unit left).

Note: Standard library modules should be imported without using aliases. Tests related to the Player class will fail until the Pawn class becomes instantiable.
'''

