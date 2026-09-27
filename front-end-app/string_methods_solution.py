def stringmethod(para, special1, special2, list1, strfind):
    # Remove all characters present in special1 from para.
    word1 = para.translate(str.maketrans('', '', special1))

    # Take first 70 chars, reverse, and print.
    rword2 = word1[:70][::-1]
    print(rword2)

    # Remove all whitespace, join characters with special2, and print.
    no_space = ''.join(rword2.split())
    joined = special2.join(no_space)
    print(joined)

    # Check whether every string in list1 is present in para.
    if all(item in para for item in list1):
        print(f"Every string in {list1} were present")
    else:
        print(f"Every string in {list1} were not present")

    # Split word1 and print first 20 words.
    words = word1.split()
    print(words[:20])

    # Count in appearance order, take words with frequency < 3, print last 20.
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    less_freq_words = [w for w in freq if freq[w] < 3]
    print(less_freq_words[-20:])

    # Print last index of strfind in word1.
    print(word1.rfind(strfind))


if __name__ == '__main__':
    para = input().rstrip('\n')
    special1 = input().rstrip('\n')
    special2 = input().rstrip('\n')
    n = int(input().strip())
    list1 = [input().rstrip('\n') for _ in range(n)]
    strfind = input().rstrip('\n')

    stringmethod(para, special1, special2, list1, strfind)
