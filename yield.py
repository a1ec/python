class MyClass:
    x = 0    
    def inc_x(self):
        self.x += 1
        
c = MyClass()
c.inc_x()
c.inc_x()

l = [1,2,3]

def f1():
    x = 0
    
    for i in l:
        yield f2(i)

    x += 1
    print(x)
    
def f2(i):
    return i*i
    
    a = MyClass()
    a.inc_x()    

