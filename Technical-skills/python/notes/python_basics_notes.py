'''
To display all the methods / functions of any module

import module_name

dir(module_name) → gets all names inside the module
getattr(module, name) → turns name into real object
callable(obj) → checks if it's a function/method
not name.startswith("_") → removes internal stuff

def list_functions(module):
    for name in dir(module):
        obj = getattr(module, name)
        if callable(obj) and not name.startswith("_"):
            print(name)
'''

'''
TODO: — Something to do later.
FIXME: — A known bug or issue.
NOTE: — Additional information.
HACK: — A workaround or less-than-ideal solution.
BUG: — Indicates a bug.
XXX: — Marks something questionable or needing attention.
'''

#-------------------------------------------------------------------------------------------------------------------------------------------------------
'''
Python Basics--------------------------------

new methods / functions:

enumerate()

lambda arguments : expression
filter() 
map()
zip()
all()       # returns True if all the elements in a iterable are true.

set()
.add()              # to add an element to a set
.remove()           # for a set, raises keyError if the element in not present
.discard()          # does not raise KeyError if the element is not present, same function as .remove()
.issubset()         # return True if the set is  a subset of another set
.issuperset()       # returns True if the set is a superset of another set
.isdisjoint()       # return True if the two sets are disjoing
|                   # this is the union operator: set_1 | set_2 returns a set of union of both sets
&                   # this is the intersection operator: set_1 & set_2 returns a set of interseciont of both sets
-                   # this is subtraction: set_1 - set_2 returns a set, subtraction. Set where first set that are not present in set 2
^                   # symmetric difference: returns a new set with elements that are present in either set 1 or set 2, not both 

    subset means all elements of first set are present in second set
    superset means all elements of second set are present in first set
    disjoint means both sets have no elements in common

    example: subset {1, 2, 3} is a subset of {1, 2, 3, 4, 5}
    example: super set {1, 2, 3} is a superset of {1, 2}
    example: set 1 {1, 2, 3}, set 2 : {4, 5, 6} = no elements in common, therefore disjoint

import datetime

datetime.date(YYYY, MM, DD)

if __name__ == "__main__"       # this code only runs if the code is ran from the original file, if you import this to another file,
    # code                      # this block of code does not run.

import re                   # regular expression

re.IGNORECASE
re.search(object, iterable, re.IGNORECASE)  
    # checks if the object is a match in iterable,# if not, it returns None otherwise it returns <re.Match object...>, 
    # IGNORECASE ignores upper lower
    # backslashd+ passed as object checks if it has a decimal or not, can be passed after a str to check for a sequence
    # + checks for one or more digits
re.fullmatch(object, iterable)
    # The fullmatch function returns a match object when the regex pattern matches the entire string and None otherwise.
'''
