from collections import Counter, OrderedDict


def collectionfunc(text1, dictionary1, key1, val1, deduct, list1):
    # Count words in text1 and print dictionary sorted by key.
    word_count = Counter(text1.split())
    sorted_word_count = dict(sorted(word_count.items(), key=lambda item: item[0]))
    print(sorted_word_count)

    # Create counter from dictionary1, subtract deduct values, and print as dictionary.
    counter_obj = Counter(dictionary1)
    counter_obj.subtract(deduct)
    print(dict(counter_obj))

    # Build ordered dictionary using key1 and val1.
    ordered_obj = OrderedDict(zip(key1, val1))

    # Delete and reinsert the second key with corresponding second value.
    if len(key1) > 1:
        second_key = key1[1]
        if second_key in ordered_obj:
            del ordered_obj[second_key]
        ordered_obj[second_key] = val1[1]

    # Convert ordered dictionary to normal dictionary and print.
    print(dict(ordered_obj))

    # Group list1 values into odd/even buckets and print.
    grouped = {"odd": [], "even": []}
    for value in list1:
        num = int(value)
        if num % 2 == 0:
            grouped["even"].append(num)
        else:
            grouped["odd"].append(num)

    final_grouped = {}
    if grouped["odd"]:
        final_grouped["odd"] = grouped["odd"]
    if grouped["even"]:
        final_grouped["even"] = grouped["even"]
    print(final_grouped)
