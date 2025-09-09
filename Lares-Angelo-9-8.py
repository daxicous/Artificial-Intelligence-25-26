
import math

# 1.
# A. Define a class ‘Circle’ that stores the radius and has a method that can return the circumference and area.
# Test your class.
# B. Make your methods return precision to the nearest hundredth (don't multiply by 100 floor and divide).
# C. Make sure that when you print your ‘Circle’ objects, it prints “This is a circle with radius {x} and area {y}.”

class Circle:
    def __init__(self, radius):
        self.r = radius
    def circum(self):
        return round(2*math.pi*self.r, 2)
    def area(self):
        return round(math.pi*self.r*self.r, 2)
    def __repr__(self):
        return f"This is a circle with radius {self.r} and area {self.area()}."

# 2. Define a class ‘Ball’ that inherits from Circle and also has a bounce level attribute and a bounciness()
# method to return five times the bounce level.

class Ball(Circle):
    def __init__(self, radius, bounciness, *args, **kwargs):
        super().__init__(radius, *args, **kwargs)
        self.b = bounciness
    def bounciness(self):
        return 5*self.b
    def __repr__(self):
        return f"this is a ball of radius {self.r} and bounce level of {self.b}"

# 3.
# A. Define a class ‘Planet’ that inherits from Circle and also has a mass attribute and a name attribute and
# a method to return each.
# B. Create a static instance variable (attribute) of Planet that holds the universal gravitational constant G.
# BB. Define a method that takes in another ‘Planet’ object and a distance and calculates the gravitational
# attraction force between the two (assume they are point masses).
# C. Define a method that returns the average density of your planet. The planet is 2D, so for density use mass
# divided by area.
# D. Make it so that printing a ‘Planet’ object prints “Planet {name} has a density of {x}”

class Planet(Circle):
    G = 6.6743 * math.pow(10, -11)
    def __init__(self, radius, mass, name, *args, **kwargs):
        super().__init__(radius, *args, **kwargs)
        self.m = mass
        self.name = name
    def attraction(self, other, distance):
        return self.G*self.m*other.m/(distance*distance)
    def density(self):
        return round(self.m/self.area(), 2)
    def __repr__(self):
        return f"Planet {self.name} has a density of {self.density()}"

# 4. Define a class SuperBall that extends Ball. Override the bounciness() to return twice the bounciness given by
# the Ball method. Do this like a good AP CS A student by calling the superclass bounciness() method.

class SuperBall(Ball):
    def __init__(self, radius, bounciness, *args, **kwargs):
        super().__init__(radius, bounciness, *args, **kwargs)
    def bounciness(self):
        return(super().bounciness()*2)

# 5. Calling the superclass constructor. Learn the incantation to pass on unrecognized keyword arguments. Use it
# in your super.__init__() calls.Calling the superclass constructor. Learn the incantation to pass on unrecognized 
# keyword arguments. Use it in your super.__init__() calls. ChatGPT explanation. Use this in #2, 3.

# 6. (Learn how to use a keyword argument.) 
# A. Create a MyData class that takes in a list of numbers and has a keyword max that specifies the maximum number 
# of items allowed in the list. The default value for the max should be 10. Store the numbers in an attribute called 
# data.
# B. A more(list of numbers) method appends the numbers to the data list. Prune the list so only the last max items 
# are retained.
# C. An average() method returns the average value of the items in the list.
# D. (Advanced.) Learn how to use the @data.setter method so that directly assigning to the data attribute still gets 
# pruned. Look up @setter for an example. 

class MyData:
    def __init__(self, xs, max=10):
        self._data = xs[-max:]
        self.m = max
    @property
    def data(self):
        return self._data
    @data.setter
    def data(self, value):
        self._data = value[-self.m:]
    def more(self, ys):
        self.data = self.data + ys
    def average(self):
        return round(sum(self.data)/len(self.data), 2)
    def __repr__(self):
        return f"this object contains the data {self.data} with a max index length of {self.m}"

# 7. Create a subclass of MyData called MyTinyData that ignores the max keyword and always makes the max = 3. Test the 
# MyTinyData constructor with and without the keyword argument for max. Both should work.

class MyTinyData(MyData):
    def __init__(self, xs, *args, **kwargs):
        super().__init__(xs, max=3)

Q1 = Circle(5)
print("Q1:")
print(Q1)
Q2 = Ball(3, 4)
print("Q2:")
print(Q2)
print(f"this ball has bounciness {Q2.bounciness()}")
Q3 = Planet(5, 10, "Bob")
Q3_2 = Planet(4, 12, "Mary")
print("Q3:")
print(Q3)
print(Q3_2)
print(f"Bob has an attraction to mary of {Q3.attraction(Q3_2, 12)}")
Q4 = SuperBall(4, 2)
print("Q4:")
print(Q4)
print(f"this ball has bounciness {Q4.bounciness()}")
Q6 = MyData([1, 2, 3, 4, 5], 4)
print("Q6:")
print(Q6)
print(f"this data has an average of {Q6.average()}")
Q6.more([4, 2, 3])
print(f"the updated version of Q6 is {Q6}")
print("Q7:")
Q7 = MyTinyData([1, 3, 2, 4, 5])
print(Q7)
Q7_2 = MyTinyData([2, 3, 4, 1, 2], 2)
print(Q7_2)



