# TODO
from cs50 import get_int


height = 0
height = get_int("Height: ")
while(height < 1 or height > 8):
    height = get_int("Height: ")
for i in range(height):
    j = height
    while(j >= 1):
        if(j > i + 1):
            print(" ", end="")
        else:
            print("#", end="")

        j = j - 1
    print("  ", end="")
    k = 1
    while(k <= i + 1):
        if(k <= i + 1):
            print("#", end="")
        else:
            print(" ", end="")

        k = k + 1
    print()