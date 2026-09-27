def isPalindrome(x):
    """
    Check whether a positive integer is a palindrome.

    >>> isPalindrome(121)
    True
    >>> isPalindrome(344)
    False
    >>> isPalindrome(-121)
    Traceback (most recent call last):
    ...
    ValueError: x must be a positive integer
    >>> isPalindrome("hello")
    Traceback (most recent call last):
    ...
    TypeError: x must be an integer
    """
    if not isinstance(x, int):
        raise TypeError("x must be an integer")
    if x < 0:
        raise ValueError("x must be a positive integer")

    s = str(x)
    return s == s[::-1]


if __name__ == '__main__':
    import doctest

    doctest.testmod()
