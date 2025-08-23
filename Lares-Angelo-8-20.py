
import math

#A list of the first 1000 integers.
q1 = [n for n in range(1, 1001)]

# A list of the first 1000 perfect squares.
q2 = [n**2 for n in range(1, 1001)]

# The sum of the first 100 perfect cubes.
q3 = sum([n**3 for n in range(1, 101)])

# A list of all of the perfect cubes between 1000 and 20000.
q4 = [n**3 for n in range(10, 30) if (n**3 >= 1000 and n**3 <= 20000)]

# The product of the numbers in the previous list, computed using a for loop.
q5 = 1
for x in q4:
    q5 *= x

# Compute sin(pi/12).
q6 = math.sin(math.pi/12)

# Find the greatest common divisor of 1558853167347433739 and 10062552685783700385249011.
def euclid(num1, num2):
    if num1 == num2:
        return num1
    if num1 < num2:
        temp = num2//num1
        if temp!=1:
            temp = math.ceil(temp - 1)
        dif = num2 - num1*temp
        return euclid(num1, dif)
    else:
        temp = num1//num2
        if temp!=1:
            temp = math.ceil(temp - 1)
        dif = num1 - num2*temp
        return euclid(num2, dif)
#euclid no workie :(
    
q7 = euclid(1558853167347433739, 10062552685783700385249011)

# The last 20 characters of the string "A dolphin likes the water. A snake slithers in the sand."
input = "A dolphin likes the water. A snake slithers in the sand."
q8 = input[-20::]

# What is the difference between 5**3, 5^3, and math.pow(5,3)? Ask about 5^3 if it is hard to understand.

#5**3 is the standard way to do exponents and outputs a type that makes sense, math.pow always outputs a float, 
# and 5^3 is a bitwise operator that does not make sense with 5 and 3

# Print this part of a poem:

# i carry your heart with me(i carry it in
# my heart)i am never without it(anywhere
# i go you go,my dear;and whatever is done
# by only me is your doing,my darling)
#                                                       i fear

print(f"q1 = {q1}")
print(f"q2 = {q2}")
print(f"q3 = {q3}")
print(f"q4 = {q4}")
print(f"q5 = {q5}")
print(f"q6 = {q6}")
print(f"q7 = {q7}")
print(f"q8 = {q8}")
print("""i carry your heart with me(i carry it in
my heart)i am never without it(anywhere
i go you go,my dear;and whatever is done
by only me is your doing,my darling)
                                                      i fear""")