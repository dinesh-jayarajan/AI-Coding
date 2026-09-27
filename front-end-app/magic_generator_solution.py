def generator_Magic(n):
    """Yield magic constants for square sizes from 3 to n."""
    for size in range(3, n + 1):
        # Magic constant formula: M = n * (n^2 + 1) / 2
        yield size * (size * size + 1) // 2


if __name__ == '__main__':
    n = int(input().strip())
    gen1 = generator_Magic(n)

    for value in gen1:
        print(value)

    # Recreate generator to show its type for sample-style output.
    gen1 = generator_Magic(n)
    print(type(gen1))
