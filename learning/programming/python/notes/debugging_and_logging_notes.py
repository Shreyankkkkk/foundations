'''
Python Basics--------------------------------

import pdb # pdb = Python De-Bugger
    pdb lets you pause a running program, inspect variables, execute python code interactively, step through the code line by line 
    and fix bugs.

pdb.set_trace()
    lets you create a breakpoint. When python runs and comes across this, it stops the programming and opens the pdb terminal
    where you can input different values and test the code

    in the pdb terminal, write "p" (printing)/ "pp" (pretty-printing) - tells the terminal that this is python code not debugger command.
    
    Note: when you are in the pdb terminal, type "h"/ "help" (that is, "(pdb) h / help"), lists out all the commands in pdb

if you do not want to import pdb, just f = open('demofile.txt', 'a')
breakpoint()
    same function as pdb.set_trace() but its built-in python.
    note: in VSCode, left of the line of code, you can add a red dot which is a breakpoint.
---------------------------------------------------------------------------------------------------------------------------
except _____Error as e:
    # Catches a specific exception.
    # Stores the exception object in the variable e.
    # e is just a variable name, you can use any valid name.

assert conditions 
    # basically helps you implement a condition, if its false, raises AssertionError
    # its basically shortened versin of

    # if not conditions:
    #       raise AssertionError

    # Like lambda and def

Re-raising Error:
    # in the except block, if you write "raise" in the end 
    # it re-raises the error (basically shows you the default error message that you always get)
----------------------------------------------------------------------------------------------------------------------------
import logging # used to record messages from program. Helps in debugging, monitoring and error tracking

logger = logging.getlogger(__name__) # __name__ identifies the current file name, .getlogger(__name__) creates a logger for this file
logger.function_name(value)
    # Functions that can be used are 
    debug - detailed info for debugging
    info - general program events
    warning - something unexpected which is not fatal
    error - a serious problem
    critical - severe failure

'''
