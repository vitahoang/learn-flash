def multiply(*args):
    print(args)
    total = 1
    for arg in args:
        total = total * arg
    print(total)
    return total


multiply(1, 3, 5)
