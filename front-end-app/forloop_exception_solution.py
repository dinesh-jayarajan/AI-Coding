def FORLoop():
    n = int(input().strip())

    l1 = [int(input().strip()) for _ in range(n)]
    print(l1)

    iter1 = iter(l1)

    for _ in range(n):
        print(next(iter1))

    return iter1


if __name__ == '__main__':
    FORLoop()
