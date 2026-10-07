import pandas as pd

def list_functions(module):
    for name in dir(module):
        obj = getattr(module, name)
        if callable(obj) and not name.startswith("_"):
            print(name)
#list_functions(pd) -  to list out all the functions and methods in the module

# print(pd.__file__) - to open the file location of the module
print( pd.DataFrame( {'Yes': [50, 21], 'No': [131, 2]} ) )

# Not Limited to integers
print( pd.DataFrame( {'Bob': ['I liked it.', 'It was awful.'], 'Sue': ['Pretty good.', 'Bland.']} ) )

# To add row labels
print( pd.DataFrame( {
    "Bob" : ["I liked it.", "It was awful."],
    "Sue" : ['Pretty Good', 'Bland.']
    }, index = ['Product A', 'Product B']) )

# Creating a series: sequence of data values
print( pd.Series( [1, 2, 3, 4, 5] ) )

# Naming a series and adding row labels

print( pd.Series([30, 40, 50], index = ['2015 Sales', '2016 Sales', '2017 Sales'], name = "Product A") )