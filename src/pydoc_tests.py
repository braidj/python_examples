
"""This is an example module to demonstrate the capabilities of pydoc
integrated with doctest
Note that the result within the interactive section is not prefixed
with >>
If no failures then there will be no output. If you need to see output then enable the 
verbose mode via a -v e.g.
python3 pydoc_tests.py -v"""


def multiply_by_two(a):

    """Multiply a number by two
    >>> [multiply_by_two(x) for x in range(7)]
    [0, 2, 4, 6, 8, 10, 12]
    """

    return a * 2


if __name__ == "__main__":

    import doctest
    doctest.testmod()
