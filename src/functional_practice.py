__author__ = 'Jason Braid'
import os
import sys
import datetime

# ----------------------------------------------------------------------------------------------------------------------
# Created: 20191227 by Jason Braid
# Purpose: to practice with functional programming concepts
# ----------------------------------------------------------------------------------------------------------------------

def do_twice(func):
    def wrapper_do_twice(*args, **kwargs):
        func(*args, **kwargs)
        func(*args, **kwargs)
    return wrapper_do_twice

@do_twice
def say_hello(name):
    print(f"Hello {name}")

def be_awesome(name):
    print( f"Yo {name}, together we are the awesomest!")

def greeting(passed_func,specific_name):
    return passed_func(specific_name)

if __name__ == "__main__":
 
    print(os.path.basename(__file__))
    print(datetime.datetime.now())

    greeting(say_hello,"Steve")
    greeting(be_awesome,"Jace")

    sys.exit(0)

