import math

def oval(a=2,b=2,z=" ",u="."):
    for i in range(a):
        for j in range(b):
            if abs(math.hypot((i-(a/2))/(a/2), (j-(b/2))/(b/2))) < 1:
                print(u, "", "")
            else:
                print(z, "", "")
        print()

oval(20,20)