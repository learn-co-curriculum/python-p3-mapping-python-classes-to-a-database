"""
pytest requires that all testing modules, classes, methods, and functions
contain the word "test" somewhere within them.

The conventions for naming tests in the Python curriculum are as follows:

    - One test module should be created for each class. If there are no classes
      to test, one test module should be created for each module being tested.
    - Test modules should be named {classname}_test.py, or {modulename}_test.py
      if necessary.
    - Test modules should be located at the base of the "testing" package.
    
    In {classname}_test.py:
        - There should be one testing class, named Test{Classname}.
        - The testing class should contain the following docstring:
            
            '''Class {Classname} in {modulename}.py'''

        - There should be at least one testing method for each instance, class,
          or static method belonging to the class being tested, including
          __init__.
        - Each testing method should be named test_{performs/does_behavior},
          where {performs/does_behavior} is a clear and concise description of
          the desired behavior.
        - Each testing method should only test one behavior.
        - Each testing method should contain the following docstring:

            '''performs/does behavior when {x} happens.'''

            ...where {x} describes the manipulation that takes place within
            the test.
"""

class TestClass:
    '''Class {Classname} in {modulename}.py'''

    def test_performs_behavior(self):
        '''performs behavior when something happens.'''
        assert(False)
