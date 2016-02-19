class MyClass(object):
    a = '12'
    b = '34'
    def myfunc(self):
        return self.a

import inspect
inspect.getmembers(MyClass, lambda a:not(inspect.isroutine(a)))
