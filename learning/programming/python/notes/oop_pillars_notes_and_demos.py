
# Object Oriented Programming
'''
Object-oriented programming, also known as OOP, is a programming style in which developers treat everything in their code like a real-world object.
A class is like a blueprint for creating objects. Every single object created from a class has attributes that define data and methods 
that define the behaviors of the objects.

Object-oriented programming has four key principles that help you organize and manage code effectively. 
They are encapsulation, inheritance, polymorphism, and abstraction.

TODO:
OOP Pillar	What it means	Common concepts ("branches")
1. Encapsulation	Bundle data and methods together while controlling access to the data.	• Public attributes/methods
• Protected attributes (_name, by convention)
• Private attributes (__name, name mangling)
• Getters
• Setters
• Validation of data

2. Inheritance	A class can inherit properties and methods from another class.	• Parent (Base) class
• Child (Derived) class
• super()
• Method overriding
• Code reuse

3. Polymorphism	The same interface or method name can have different behaviors.	• Method overriding
• Same method, different implementations
• Duck typing (Python concept)
• Operator overloading 

4. Abstraction	Hide implementation details and expose only what's necessary.	• Abstract classes
• Abstract methods
• ABC module
• Interfaces (concept)
• Focusing on what an object does rather than how it does it

Encapsulation:
With encapsulation, you can hide the internal state of the object behind a simple set of public methods and attributes 
that act like doors. Behind those doors are private attributes and methods that control how the data changes and who can see it.

NOTE: By convention, prefixing attribute and methods with a single underscore means they are meant for internal use.
      No one should directly access them from outside the class since it defies the principles of encapsulation, which can lead to bugs.

      "This is intended for internal use. Please don't access it directly."

      While a single underscore prefix is just a convention, prefixing attributes and methods with a double underscore effectively prevents 
      them to be accessed from the outside of their class, making those attributes and methods private.

      "This is intended for internal use. YOU can't access it directly."

'''
class Wallet:
   def __init__(self):
       self.__balance = 0

   def __validate(self, amount):
       if amount < 0:
           raise ValueError('Amount must be positive')

   def deposit(self, amount):
       self.__validate(amount)
       self.__balance += amount

   def withdraw(self, amount):
       self.__validate(amount)
       if amount > self.__balance:
           raise ValueError('Insufficient funds')
       self.__balance -= amount

   def get_balance(self):
       return self.__balance

acct_one = Wallet()
acct_one.deposit(3)
#print(acct_one.get_balance()) # 3

acct_one.deposit(50)
#print(acct_one.get_balance()) # 53

#acct_one.deposit(-4)  # ValueError: Amount must be positive
#acct_one.withdraw(-8) # ValueError: Amount must be positive
#acct_one.withdraw(58) # ValueError: Insufficient funds
#print(acct_one.__balance) # AttributeError: 'Wallet' object has no attribute '__balance'

'''
Encapsulation: 
    Getters and Setters 

    Getters and setters are methods that let you control how the attributes of a class are accessed and modified. 
    With getters you retrieve a value, and with setters you set a value.

    Properties act like attributes but work like methods
        This means you can access properties with dot notation instead of parentheses or round brackets.

        make the code cleaner and easier to read. its for readability and convention

        The main thing properties do is that they run extra logic behind the scenes when you get, set, or delete values with them. 
        This makes them the perfect choice when you want to access or manipulate data within objects.

        When you use a method, you always have to call it with parentheses. But with a property, you can access it just like a normal attribute using dot notation. 
        That makes your code look simple even when it is doing extra work behind the scenes.
    
    In Python, a decorator is a function that modifies the functionalities of other functions, or classes, without changing their original code.

    you define a method and place the @property decorator above it. 
    This turns the method into a property, so it can be accessed like an attribute while internally calling the decorated method.
'''
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self): # A getter to get the radius
        return self._radius

    @property
    def area(self):  # A getter to calculate area
        return 3.14 * (self._radius ** 2)
    
    @radius.setter
    def radius(self, value):
        if value <= 0:
            raise ValueError("Value must be greater than 0")
        self._radius = value

    @radius.deleter
    def radius(self):
        #print('Deleting Radius...')
        del self._radius

my_circle = Circle(3)
#print("Initial Radius :", my_circle.radius)

my_circle.radius = 10
#print("New Radius:", my_circle.radius)

del my_circle.radius
#print("Radius deleted")


# Without @property
# Output:
#        <bound method Circle.radius of <__main__.Circle object at 0x0000017877A1AF90>>
#        <bound method Circle.area of <__main__.Circle object at 0x0000017877A1AF90>>

''' to run without @property
print(my_circle.radius())
print(my_circle.area())
'''

'''
Different Decorators:

| Decorator            | Category            | Used on                  | What it does                                                    | Example use                                          |
| -------------------- | ------------------- | ------------------------ | --------------------------------------------------------------- | ---------------------------------------------------- |
| `@property`          | OOP / Encapsulation | Method inside a class    | Makes a method behave like an attribute                         | `account.balance` instead of `account.get_balance()` |
| `@<property>.setter` | OOP / Encapsulation | Method inside a class    | Controls changing a property value                              | `account.balance = 500` with validation              |
| `@classmethod`       | OOP                 | Class method             | Method receives the class (`cls`) instead of an object (`self`) | Alternative constructors, modifying class-level data |
| `@staticmethod`      | OOP                 | Method inside a class    | Method does not need `self` or `cls`                            | Utility functions related to a class                 |
| `@dataclass`         | OOP / Data modeling | Class                    | Automatically creates `__init__`, `__repr__`, etc.              | Storing structured data like trades                  |
| `@cache`             | Performance         | Function                 | Stores previous results to avoid recalculation                  | Faster repeated calculations                         |
| `@lru_cache`         | Performance         | Function                 | Limited-size cache                                              | Dynamic programming problems                         |
| `@wraps`             | Decorator creation  | Function wrapper         | Preserves original function information                         | Building your own decorators                         |
| `@abstractmethod`    | OOP / Abstraction   | Method in abstract class | Forces child classes to implement a method                      | Interfaces/design patterns                           |

'''
