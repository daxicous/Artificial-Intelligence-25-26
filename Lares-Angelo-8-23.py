
import random
from collections import defaultdict
from collections import Counter

# 1. Create a dictionary that that lets you look up “red” to get 2, “yellow” to get 10, and “green” to get 50.
q1 = {"red":2, "yellow":10, "green":50}

print(f"q1: {q1}")

# 2. Add “blue” with a value of 90 to your dictionary.
q2 = q1.copy()
q2["blue"] = 90

print(f"q2: {q2}")

# 3. Remove “red” from your dictionary.
q3 = q2.copy()
del q3["red"]

print(f"q3: {q3}")

# 4. Read about defaultdict – the examples are enough – and create one that holds the items in your dictionary 
# above, but gives 0 when you ask for a color that is not in the dictionary.
q4 = defaultdict(int)
for k,v in q3.items():
    q4[k] = v

readout = ""
for i, (k,v) in enumerate(q4.items()):
    if i == 0:
        readout+=f"({k}, {v})"
    else:
        readout+=f", ({k}, {v})"
print(f"q4: {readout}")
print(f"purple: {q4["purple"]}")

# 5. Create a default dictionary that takes in a number and gives a list. When the number is 0 give [1,2,3], 
# when the number is 2, give [1,3], and when the number is 3 give [1,2]. Other numbers should give the empty list.
q5 = defaultdict(list)
temp = {0:[1, 2, 3], 2:[1, 3], 3:[1, 2]}
for k,v in temp.items():
    q5[k] = v

readout = ""
for i, (k,v) in enumerate(q5.items()):
    if i == 0:
        readout+=f"({k}, {v})"
    else:
        readout+=f", ({k}, {v})"
print(f"q5: {readout}")
print(f"1: {q5[1]}")

# Here is a list of ten different colors:
colors = ["Red", "Blue", "Green", "Yellow", "Orange", "Purple", "Pink", "Brown", "Gray", "Teal"]

# 6. Print a single random color from the list above.
q6 = colors[random.randint(0, len(colors)-1)]

print(f"q6: {q6}")

# 7. Make a dictionary with a random number from 1 to 1000 mapping to a random color.
q7 = defaultdict(list)
q7[random.randint(1, 1000)] = [colors[random.randint(0, len(colors)-1)]]

readout = ""
for i, (k,v) in enumerate(q7.items()):
    if i == 0:
        readout+=f"({k}, {v})"
    else:
        readout+=f", ({k}, {v})"
print(f"q7: {readout}")

# 8. Add 200 items to the dictionary above — just more random numbers matching to random colors.
q8 = q7.copy()
for i in range(200):
    q8[random.randint(1, 1000)].append(colors[random.randint(0, len(colors)-1)])

readout = ""
for i, (k,v) in enumerate(q8.items()):
    if i == 0:
        readout+=f"({k}, {v})"
    else:
        readout+=f", ({k}, {v})"
print(f"q8: {readout}")

# 9. Repeat this ten times: pick a random number from 1 to 1000 and print either the matching color from your 
# dictionary or “transparent” if there is no matching color.
print("q9: ")
for i in range(10):
    num = random.randint(1, 1000)
    if q8[num] == []:
        print("transparent")
        continue
    else:
        print(f"({num}, {q8[num]})")
        continue

# 10. Create another dictionary that maps color name to the number of items that match that color in the list 
# from 3 above. (“No technology”, just base Python.)
values = q8.values()
pcolors = []
for xs in values:
    pcolors.extend(xs)
pcolors.sort()

q10 = {}
last = pcolors[0]
counter = 0
for color in pcolors:
    if color == last:
        counter+=1
        continue
    else:
        q10[color] = counter
        counter = 1
        last = color
        continue
q10[pcolors[-1]] = counter

print(f"q10: {q10}")

# 11. Print out a report from most common to least common, showing a single COLOR and COUNT on each line.
q11 = []
q11 = list(q10.items())
q11.sort(key = lambda x: x[1], reverse=True)

print("q11: ")
for k, v in q11:
    print(f"{k}: {v}")

# 12. Ask the user for a number and if that number is in the dictionary print out the matching color.
# Otherwise print out “never heard of it”.
print("q12:")
readin = input("give me a number human: ")
if q8[readin] != []:
    print(q8[int(readin)])
else:
    print("never heard of it")

# 13. Read about the Counter class and write another solution to the exercises 5 and 6 above 
# (the color counting and report).
values = q8.values()
pcolors = []
for xs in values:
    pcolors.extend(xs)
q13a = Counter(pcolors)

print(f"q13a: {q13a}")

q13b = list(q13a.items())
q13b.sort(key = lambda x: x[1], reverse=True)

print("q13b: ")
for k, v in q13b:
    print(f"{k}: {v}")