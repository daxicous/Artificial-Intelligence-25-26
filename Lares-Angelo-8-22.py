
import collections
import random
import math

#1. A list of the first 20 Fibonacci numbers. So [1, 1, 2, 3, 5...]
q1 = [1, 1]
for i in range(18):
    q1.append(q1[-1]+q1[-2])

print(f"q1: {q1}")

#2. A list with the partial sums of the first 20 perfect fourth powers. 
q2 = [1]
for i in range(2, 21):
    q2.append(q2[-1]+i ** 4)

print(f"q2: {q2}")

#3. Write a function some_words that 
#takes in a list of strings someWords and outputs a list of the strings in someWords that come after “grapefruit” 
#in the dictionary and have at least 5 letters.
# Ex: someWords ["apple","mango","papaya","blueberry","juju"] == ["mango","papaya"]
someWords = ["apple","mango","papaya","blueberry","juju"]
def some_words(words):
    ans = []
    for word in words:
        if len(word)>=5 and word>"grapefruit":
            ans.append(word)
    return ans

q3 = some_words(someWords)

print(f"q3: {q3}")

#4.(Function: q4) Ask the person to type a number, use input(). Print 20 times that number.
print("q4: ")
readin = input("Give me a number human: ")
for i in range(20):
    print(readin)

#5.(Function: numpair) Given a string containing some integers separated by spaces, output a list of pairs
# (number, position), where position is the index of the number in the list - counting from zero.
# Ex: numpair "10 50 30 70" == [(10,0), (50,1), (30,2), (70,3)]
def numpair(readin):
    nums = readin.split()
    ans = []
    for i, num in enumerate(nums):
        ans.append((int(num), i))
    return ans

print(f"q5: {numpair("10 50 30 70")}")

#6.(Function: largeRem) Given two integers, output the one with the largest remainder when divided by 1397.
# Ex: largeRem 2000 2800 == 2000
def largeRem(num1, num2):
    rem1 = num1%1397
    rem2 = num2%1397
    if rem1 > rem2:
        return num1
    else:
        return num2

print(f"q6: {largeRem(2000, 2800)}")

#7.(Function: myConcat) Given two lists, return the list made by joining all of the items from each, in order.
# Ex: myConcat [3,1,2] [50,60,70,80] == [3,1,2,50,60,70,80]
def myConcat(list1, list2):
    ans = []
    for i in list1:
        ans.append(i)
    for i in list2:
        ans.append(i)
    return ans

print(f"q7: {myConcat([3, 1, 2], [50, 60, 70, 80])}")

#8.(Function: lastPrint) Given a list of positive integers, modify the list by repeatedly removing the last 
#item and printing it. Stop after you hit a four digit integer. Return the modified list.
print("q8:")
def lastPrint(list):
    for x in reversed(list):
        print(list)
        if x>999:
            break
        list = list[:-1:]

lastPrint([5, 65, 2903, 403, 23, 100])

#9.Make a deque with 10000 random integers in the range [-500,800]. Remove numbers from the start of the list 
#stopping after you hit a number above 700. Add in 1000 more random numbers at the start.
q9 = collections.deque()
for i in range(10000):
    q9.append(random.randint(-500, 800))
while q9[0] <= 700:
    q9.popleft()
for i in range(1000):
    q9.appendleft(random.randint(-500, 800))

#im not ruining my printout with this question
#print(f"q9: {q9}")

#10.Create a list containing all of the Pythagorean triples (a, b, c) with a<100 and b<100
q10 = []
for a in range(1, 100):
    for b in range(a+1, 100):
        if math.isqrt(a**2+b**2)**2 == a**2+b**2:
            q10.append((a, b, math.isqrt(a**2+b**2)))

print(f"q10: {q10}")

#11.Remove the duplicates from your list, so you end up with a<b<c. Sort them based on a and then b
q11 = list(set(q10))
print(f"q11: {sorted(q11)}")