# generators and yield
# http://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do-in-python?rq=1
"""
The first time the for calls the generator object created from your function, it
will run the code in your function from the beginning until it hits yield, then
it'll return the first value of the loop. Then, each other call will run the
loop you have written in the function one more time, and return the next value,
until there is no value to return.
"""
mylist = [x*x for x in range(3)]
for i in mylist:
    print(i)
   
mygenerator = (x*x for x in range(3))
for i in mygenerator:
    print(i)
   
def createGenerator():
   mylist = range(3)
   for i in mylist:
       yield i*i

mygenerator = createGenerator() # create a generator
print(mygenerator) # mygenerator is an object!
for i in mygenerator:
    print(i)

# this time values are exhausted, none will be returned
for i in mygenerator:
    print(i)

# create a new generator
thenextgen = createGenerator()
for i in thenextgen:
    print(i)
