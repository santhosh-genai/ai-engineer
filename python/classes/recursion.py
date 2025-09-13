def recursion(x):
    print(x)
    if x == 0:
        return
    recursion(x-1)
recursion(5)