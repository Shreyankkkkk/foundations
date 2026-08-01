'''
Classes and Objects
'''

'''
class Book:
   """This class is for defining a book and its pages"""
   title: str
   pages: int

   def __init__(self, title, pages):
       self.title : str = title
       self.pages : int = pages

   def __len__(self):
       return self.pages

   def __str__(self):
       return f"'{self.title}' has {self.pages} pages"

   def __eq__(self, other):
       return self.pages == other.pages
  
book1 = Book("Built Wealth Like a Boss", 420)
book2 = Book("Be Your Own Start", 420)

print(book1.__dict__)
print(book2.__dict__)

print(book1.__class__)
print(book2.__class__)

print(book1.__doc__)
print(book2.__doc__)

print(book1.__module__) # doubt here
print(book2.__module__) # if i "import book" in other file in the same directory, this should give another output

print(Book.__bases__) # why does Book.__bases__ work, i dont understand this thing. Output: (<class 'object'>,) 

print(Book.__name__)    # both qualname and name give same output, and it is for class_name not attribute
print(Book.__qualname__)# doesnt make sense and its use

print(Book.__annotations__)
print(book1.__annotations__) 
print(book2.__annotations__)
print("__annotations__" in book1.__dict__)
print("__annotations__" in book2.__dict__)
print("__annotations__" in Book.__dict__)

print(Book.__weakrefoffset__) #Output: 16, why?
#__weakrefoffset__ does not work for objects, only classes
# why is vscode red underlining __weakref__, but not __weakrefoffset__. If its an error, why am i getting an output and not an Error

print(Book.__sizeof__("Book")) # Needs an argument, showcases use of __name__, Output: 80, why?
print(book1.__sizeof__()) # objects dont need arguments, Output: 24, why?
print(book2.__sizeof__()) # also returns 24, why?

print(Book.__dir__(book1)) # why does this need an argument if it lists methods and attributes
print(Book.__dir__(book2)) #both book1 and book2 returns the same thing
print()

#dir(Book)
# opens up a menu in terminal where i can type things, idk what to type

print(hash(Book)) #Output: 149794998663, why
# does not work for attributes, work for class 
print(format(Book)) # Output: <class '__main__.Book'>
print(format(book1)) # Output: 'Built Wealth Like a Boss' has 420 pages
# so this basically works like print(book1), same as book.__str__, this makes sense cause format is for printing 

#__getattribute__, __setattr__, __delattr__, __getattr__ makes sense 
# idk the differene between __getattribute__ and __getattr__
'''

'''
# Built-in Attribute Functions

getattr(obj, attr, default)
    Gets the value of an attribute.
    Returns 'default' if attribute doesn't exist.
Example:
    getattr(student, "name")
    getattr(student, "grade", "Not Found")


setattr(obj, attr, value)
    Creates a new attribute or updates an existing one.
Example:
    setattr(student, "age", 20)


hasattr(obj, attr)
    Returns True if the attribute exists, otherwise False.

Example:
    hasattr(student, "name")


delattr(obj, attr)
    Deletes an attribute from an object.
Example:
    delattr(student, "age")


Easy way to remember:
    get  -> Read an attribute
    set  -> Create/Update an attribute
    has  -> Check if an attribute exists
    del  -> Delete an attribute

These functions are useful when the attribute name is stored
in a variable rather than written directly.

Example:
    attr = "name"
    print(getattr(student, attr))
    instead of: student.name
'''

