from random import random

t = 1

for i in range(10):
    print(f'{t}, {random()}, {random()}')
    t += random()*2 + 1
