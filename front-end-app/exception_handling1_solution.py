def Handle_Exc1():
    a = int(input().strip())
    b = int(input().strip())

    try:
        if a > 150 or b < 100:
            raise ValueError("Input integers value out of range.")
        elif a + b > 400:
            raise ValueError("Their sum is out of range")
        else:
            print("All in range")
    except ValueError as err:
        print(err)


if __name__ == '__main__':
    Handle_Exc1()
